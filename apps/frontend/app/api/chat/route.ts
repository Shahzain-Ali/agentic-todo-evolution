import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// MCP Server URL (deployed on Render)
const MCP_SERVER_URL =
  process.env.MCP_SERVER_URL || "https://mcp-todo-server.onrender.com";

// Tool definitions for OpenAI function calling (matching MCP server tools)
const tools: OpenAI.Chat.Completions.ChatCompletionTool[] = [
  {
    type: "function",
    function: {
      name: "add_task",
      description: "Add a new todo task",
      parameters: {
        type: "object",
        properties: {
          title: {
            type: "string",
            description: "The task title",
          },
          description: {
            type: "string",
            description: "Optional task description",
          },
        },
        required: ["title"],
      },
    },
  },
  {
    type: "function",
    function: {
      name: "list_tasks",
      description: "List all todo tasks",
      parameters: {
        type: "object",
        properties: {
          filter: {
            type: "string",
            enum: ["all", "pending", "completed"],
            description: "Filter tasks by status",
          },
        },
      },
    },
  },
  {
    type: "function",
    function: {
      name: "complete_task",
      description: "Mark a task as completed",
      parameters: {
        type: "object",
        properties: {
          task_id: {
            type: "string",
            description: "The task ID to complete",
          },
        },
        required: ["task_id"],
      },
    },
  },
];

// MCP session management
let mcpSessionId: string | null = null;

async function initMCPSession(): Promise<string> {
  const res = await fetch(`${MCP_SERVER_URL}/mcp`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "initialize",
      params: {
        protocolVersion: "2025-03-26",
        capabilities: {},
        clientInfo: { name: "todo-frontend", version: "1.0" },
      },
      id: 1,
    }),
  });

  const sessionId = res.headers.get("mcp-session-id");
  if (!sessionId) {
    throw new Error("Failed to get MCP session ID");
  }

  // Send initialized notification
  await fetch(`${MCP_SERVER_URL}/mcp`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
      "Mcp-Session-Id": sessionId,
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "notifications/initialized",
    }),
  });

  return sessionId;
}

async function getMCPSessionId(): Promise<string> {
  if (mcpSessionId) {
    return mcpSessionId;
  }
  mcpSessionId = await initMCPSession();
  return mcpSessionId;
}

function parseMCPResponse(text: string): any {
  // MCP returns SSE format: "event: message\ndata: {...}\n\n"
  const lines = text.split("\n");
  for (const line of lines) {
    if (line.startsWith("data: ")) {
      return JSON.parse(line.slice(6));
    }
  }
  // Try parsing as plain JSON
  return JSON.parse(text);
}

async function callMCPTool(
  toolName: string,
  args: any,
  jwtToken: string
): Promise<any> {
  console.log(`🔧 Calling MCP tool: ${toolName}`, args);

  const sessionId = await getMCPSessionId();

  // Inject jwt_token into the tool arguments
  const mcpArgs = { ...args, jwt_token: jwtToken };

  const res = await fetch(`${MCP_SERVER_URL}/mcp`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
      "Mcp-Session-Id": sessionId,
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "tools/call",
      params: {
        name: toolName,
        arguments: mcpArgs,
      },
      id: Date.now(),
    }),
  });

  const responseText = await res.text();
  console.log(`🔧 MCP response for ${toolName}:`, responseText);

  const parsed = parseMCPResponse(responseText);

  if (parsed.error) {
    // Session expired - reinitialize and retry
    if (
      parsed.error.message?.includes("session") ||
      parsed.error.code === -32600
    ) {
      console.log("🔄 MCP session expired, reinitializing...");
      mcpSessionId = null;
      const newSessionId = await getMCPSessionId();

      const retryRes = await fetch(`${MCP_SERVER_URL}/mcp`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json, text/event-stream",
          "Mcp-Session-Id": newSessionId,
        },
        body: JSON.stringify({
          jsonrpc: "2.0",
          method: "tools/call",
          params: {
            name: toolName,
            arguments: mcpArgs,
          },
          id: Date.now(),
        }),
      });

      const retryText = await retryRes.text();
      const retryParsed = parseMCPResponse(retryText);

      if (retryParsed.error) {
        throw new Error(`MCP tool error: ${retryParsed.error.message}`);
      }

      // Extract content from MCP result
      return extractMCPContent(retryParsed.result);
    }
    throw new Error(`MCP tool error: ${parsed.error.message}`);
  }

  return extractMCPContent(parsed.result);
}

function extractMCPContent(result: any): any {
  // MCP tools/call returns { content: [{ type: "text", text: "..." }] }
  if (result?.content && Array.isArray(result.content)) {
    for (const item of result.content) {
      if (item.type === "text" && item.text) {
        try {
          return JSON.parse(item.text);
        } catch {
          return { success: true, message: item.text };
        }
      }
    }
  }
  return result;
}

export async function POST(request: NextRequest) {
  try {
    // Get JWT token from session cookie (set during sign-in)
    const sessionToken = request.cookies.get("session")?.value;

    if (!sessionToken) {
      return NextResponse.json(
        {
          success: false,
          message:
            "Please sign in first to use the AI assistant. Go to /login to sign in.",
        },
        { status: 401 }
      );
    }

    const body = await request.json();
    const { message, conversationHistory = [] } = body;

    console.log("📨 Received message:", message);

    // Build conversation with system prompt
    const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
      {
        role: "system",
        content:
          "You are a helpful AI todo assistant. You help users manage their tasks using the available tools. Be friendly and concise. IMPORTANT: When a user wants to complete/mark a task as done, you MUST first call list_tasks to get the task IDs, then call complete_task with the correct task_id UUID. Never guess task IDs.",
      },
      ...conversationHistory,
      {
        role: "user",
        content: message,
      },
    ];

    // Call OpenAI with function calling
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages,
      tools,
      tool_choice: "auto",
    });

    const responseMessage = completion.choices[0].message;

    // Check if tool calls are needed
    if (responseMessage.tool_calls && responseMessage.tool_calls.length > 0) {
      console.log(
        "🛠️  Tool calls detected:",
        responseMessage.tool_calls.length
      );

      // Execute tool calls via MCP server
      const toolResults = await Promise.all(
        responseMessage.tool_calls.map(async (toolCall: any) => {
          const toolName = toolCall.function.name;
          const toolArgs = JSON.parse(toolCall.function.arguments);

          const result = await callMCPTool(toolName, toolArgs, sessionToken);

          return {
            tool_call_id: toolCall.id,
            role: "tool" as const,
            content: JSON.stringify(result),
          };
        })
      );

      // Send tool results back to OpenAI
      const finalCompletion = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [...messages, responseMessage, ...toolResults],
      });

      const finalResponse = finalCompletion.choices[0].message.content;
      console.log("✅ Final response:", finalResponse);

      return NextResponse.json({
        success: true,
        message: finalResponse,
      });
    }

    // No tool calls needed, return direct response
    const directResponse = responseMessage.content;
    console.log("✅ Direct response:", directResponse);

    return NextResponse.json({
      success: true,
      message: directResponse,
    });
  } catch (error: any) {
    console.error("❌ Chat API error:", error);
    return NextResponse.json(
      {
        success: false,
        message: "Error: " + error.message,
      },
      { status: 500 }
    );
  }
}
