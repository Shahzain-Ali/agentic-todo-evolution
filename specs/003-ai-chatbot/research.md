# Research: AI-Powered Todo Chatbot (Phase 3)

**Feature Branch**: `003-ai-chatbot`
**Date**: 2026-02-04
**Status**: Complete

## Research Tasks Completed

### 1. MCP SDK Python Integration

**Question**: How to create MCP server with HTTP/SSE transport for web-based agents?

**Decision**: Use FastMCP with lifespan management pattern

**Rationale**:
- FastMCP provides simplified server setup with decorators
- Lifespan pattern enables proper database connection management
- HTTP/SSE transport works with OpenAI Agents SDK via `MCPServerStreamableHttp`

**Implementation Pattern**:
```python
from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(server):
    # Startup: Initialize database
    engine = create_engine(settings.database_url)
    yield
    # Shutdown: Cleanup
    engine.dispose()

mcp = FastMCP("todo-mcp-server", lifespan=lifespan)

@mcp.tool()
async def add_task(jwt_token: str, title: str) -> str:
    """Tool docstring for AI understanding"""
    return json.dumps({"success": True, ...})
```

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Raw MCP SDK Server class | More boilerplate, less ergonomic |
| WebSocket transport | SSE is simpler, sufficient for request-response |
| gRPC transport | Overkill for this use case, adds complexity |

---

### 2. OpenAI Agents SDK Setup

**Question**: How to connect Agents SDK to MCP server and manage sessions?

**Decision**: Use `MCPServerStreamableHttp` for connection, `SQLiteSession` for conversation history

**Rationale**:
- MCPServerStreamableHttp connects to HTTP-based MCP servers
- SQLiteSession provides simple, local conversation persistence
- No need for server-side conversation management (OpenAI handles it)

**Implementation Pattern**:
```python
from agents import Agent, Runner, SQLiteSession
from agents.mcp import MCPServerStreamableHttp

async with MCPServerStreamableHttp(
    name="TodoMCP",
    params={"url": "http://localhost:8001/mcp"},
    cache_tools_list=True
) as mcp_server:
    agent = Agent(
        name="Todo Assistant",
        instructions="Help users manage todos via natural language.",
        mcp_servers=[mcp_server]
    )

    session = SQLiteSession(user_id)
    result = await Runner.run(agent, message, session=session)
```

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| OpenAIConversationsSession | Requires server-side state on OpenAI, less control |
| Custom session storage | Unnecessary, SQLiteSession works well |
| HostedMCPTool | Requires hosting MCP on OpenAI infra, we self-host |

---

### 3. ChatKit React Integration

**Question**: How to integrate ChatKit with Next.js 16 App Router and Better Auth?

**Decision**: Use `useChatKit` hook with custom `getClientSecret` that creates OpenAI sessions

**Rationale**:
- useChatKit provides all necessary controls (sendMessage, control, etc.)
- getClientSecret handles session creation and refresh
- Can pass JWT token to backend for user identification

**Implementation Pattern**:
```typescript
'use client';
import { ChatKit, useChatKit } from '@openai/chatkit-react';

function TodoChatbot() {
  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        if (existing) {
          // Refresh
          const res = await fetch('/api/chatkit/refresh', {
            method: 'POST',
            body: JSON.stringify({ token: existing }),
          });
          return (await res.json()).client_secret;
        }
        // Create new session
        const res = await fetch('/api/chatkit/session', { method: 'POST' });
        return (await res.json()).client_secret;
      },
    },
    theme: 'dark',
  });

  return <ChatKit control={control} className="h-full" />;
}
```

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Custom chat UI | More work, ChatKit is production-ready |
| Vercel AI SDK | Different architecture, not MCP-based |
| Direct OpenAI Chat API | No built-in UI, need to build from scratch |

---

### 4. JWT Token Flow

**Question**: How to pass Better Auth JWT from ChatKit → OpenAI Agent → MCP Tools?

**Decision**: Inject JWT in session metadata, extract in MCP tools via parameter

**Rationale**:
- ChatKit session API receives JWT from Better Auth
- Session metadata passes to Agent context
- Agent includes JWT as parameter when calling MCP tools
- Each MCP tool validates JWT and extracts user_id

**Token Flow Diagram**:
```
1. User logs in via Better Auth → JWT stored in httpOnly cookie
2. User opens /chat → ChatKit calls /api/chatkit/session
3. Session API reads JWT from cookie → passes to OpenAI session creation
4. OpenAI Agent receives JWT in context/metadata
5. Agent calls MCP tool with jwt_token parameter
6. MCP tool validates JWT → extracts user_id → performs operation
```

**Implementation**:
```python
# MCP Tool
@mcp.tool()
async def add_task(jwt_token: str, title: str) -> str:
    # Validate JWT using existing Phase 2 auth
    user = await get_user_from_token(jwt_token)
    if not user:
        return json.dumps({"error": "Unauthorized"})

    # Create task for authenticated user
    task = Task(title=title, user_id=user.id)
    ...
```

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Pass user_id directly | Security risk, user could impersonate others |
| Server-side session lookup | Adds complexity, JWT is self-contained |
| API key per user | Overkill, JWT already identifies user |

---

### 5. Tool Invocation Patterns

**Question**: How does OpenAI Agent decide which tool to call based on natural language?

**Decision**: Use clear, descriptive docstrings; let GPT-4 handle intent recognition

**Rationale**:
- OpenAI's GPT-4 is excellent at intent recognition
- Tool docstrings provide context for correct tool selection
- No need for custom NLU or intent classification

**Best Practices for Tool Definitions**:

1. **Clear tool names**: `add_task` not `create_new_todo_item`
2. **Descriptive docstrings**: Include what the tool does, parameters, return format
3. **Sensible defaults**: `filter="all"` for list_tasks
4. **Type hints**: Help agent understand parameter types
5. **Example usage**: Can include in docstring for edge cases

**Example Tool Definition**:
```python
@mcp.tool()
async def list_tasks(
    jwt_token: str,
    filter: str = "all"
) -> str:
    """
    List user's tasks with optional filter.

    Use this when user wants to see their tasks, todo list,
    or asks "what do I need to do?".

    Args:
        jwt_token: Authentication token (always required)
        filter: One of:
            - "all": Show all tasks (default)
            - "completed": Show only finished tasks
            - "pending": Show only unfinished tasks

    Returns:
        JSON with {"tasks": [...], "count": N} or {"error": "message"}

    Examples of user intents that trigger this tool:
        - "Show me my tasks"
        - "What do I need to do?"
        - "List completed tasks"
        - "What's on my todo list?"
    """
```

**Intent Mapping** (handled by GPT-4):
| User Input | Detected Intent | Tool Called |
|------------|-----------------|-------------|
| "Add buy milk" | Create task | add_task |
| "Show my tasks" | List tasks | list_tasks |
| "What's left to do?" | List pending | list_tasks(filter="pending") |
| "Mark task 3 done" | Complete task | complete_task |
| "Delete the meeting" | Delete task | delete_task |
| "Rename task 5 to X" | Update task | update_task |

---

## Technology Decisions Summary

| Decision | Choice | Confidence |
|----------|--------|------------|
| MCP Server Framework | FastMCP with lifespan | High |
| MCP Transport | HTTP/SSE | High |
| Agent Session | SQLiteSession | High |
| Frontend Chat UI | ChatKit React | High |
| Auth Token Flow | JWT in tool parameters | High |
| NLU/Intent Recognition | GPT-4 built-in | High |
| Conversation Storage | SQLite (Agents SDK managed) | High |
| Database Reuse | Phase 2 PostgreSQL | High |

---

## Open Questions (Resolved)

All research questions resolved. No open questions remain.

---

## References

- **MCP SDK Docs**: Retrieved via Context7 (`/modelcontextprotocol/python-sdk`)
- **OpenAI Agents SDK**: Retrieved via Context7 (`/openai/openai-agents-python`)
- **ChatKit Docs**: Retrieved via Context7 (`/openai/chatkit-js`)
- **Skills Created**:
  - `.claude/skills/mcp-tools-skill.md`
  - `.claude/skills/openai-agents-skill.md`

---

**Research Status**: ✅ Complete
**Next Step**: Proceed to Phase 1 (Data Model & Contracts)
