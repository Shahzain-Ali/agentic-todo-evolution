# OpenAI Agents Skill - Phase 3 AI Chatbot

## Purpose
Complete guide for building AI chatbot using OpenAI Agents SDK in Phase 3. This skill covers MCP tools integration, conversation memory management, and natural language-based todo management.

## What is OpenAI Agents SDK?
OpenAI Agents SDK is a Python library that enables you to create AI agents. These agents:
- Understand natural language
- Use external tools (via MCP)
- Maintain conversation context
- Handle multi-turn conversations

## Technology Stack
- **OpenAI Agents SDK**: `agents` package
- **MCP Integration**: MCPServerStreamableHttp
- **Session Management**: SQLiteSession / OpenAIConversationsSession
- **Database**: SQLite for conversation history
- **Authentication**: JWT tokens passed to MCP tools

---

## Architecture Overview

```
┌─────────────────────┐
│  User Input         │
│  "Add buy milk"     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  OpenAI Agent       │
│  - Understands NL   │
│  - Decides tool     │
└──────────┬──────────┘
           │ MCP Protocol
           ▼
┌─────────────────────┐
│  MCP Server         │
│  - add_task()       │
│  - list_tasks()     │
│  - complete_task()  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Database (Neon)    │
│  - Tasks            │
│  - Users            │
└─────────────────────┘
```

---

## Latest OpenAI Agents SDK Patterns

### 1. Basic Agent Creation

```python
from agents import Agent, Runner

# Simple agent without tools
agent = Agent(
    name="Todo Assistant",
    instructions="You are a helpful todo list manager. Be concise and friendly.",
    model="gpt-4"  # or "gpt-3.5-turbo"
)

# Run agent (async)
result = await Runner.run(
    agent,
    "Hello! What can you help me with?"
)

print(result.final_output)
# Output: "I can help you manage your todo list..."
```

**Key Components:**
- `name`: Agent's identifier
- `instructions`: System prompt / personality
- `model`: Which OpenAI model to use

---

### 2. Integrating MCP Server (HTTP)

```python
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async def create_todo_agent():
    # Connect to our Phase 3 MCP server
    async with MCPServerStreamableHttp(
        name="TodoMCP",
        params={
            "url": "http://localhost:8001/mcp",  # Your MCP server URL
            "headers": {
                # Optional: Add headers if needed
                "Content-Type": "application/json"
            },
        },
        cache_tools_list=True  # Cache tool definitions for performance
    ) as mcp_server:

        # Create agent with MCP server
        agent = Agent(
            name="Todo Assistant",
            instructions="""
            You are a todo list manager assistant.
            Help users manage their tasks using natural language.

            Available tools:
            - add_task: Create new tasks
            - list_tasks: Show all tasks (with filters)
            - complete_task: Mark tasks as done
            - delete_task: Remove tasks
            - update_task: Modify task details

            Always be concise and helpful.
            """,
            mcp_servers=[mcp_server]  # Connect MCP tools
        )

        # Agent now has access to all 5 MCP tools!
        result = await Runner.run(
            agent,
            "Add a task to buy groceries"
        )

        print(result.final_output)
```

**Important Notes:**
- `MCPServerStreamableHttp` for HTTP-based MCP servers
- `cache_tools_list=True` improves performance
- MCP server must be running before agent starts
- Agent automatically discovers all tools from MCP server

---

### 3. Session Management - SQLiteSession

```python
from agents import Agent, Runner, SQLiteSession

async def chat_with_memory():
    agent = Agent(
        name="Todo Assistant",
        instructions="You are a helpful assistant. Be concise."
    )

    # Create session for user
    user_id = "user_123"
    session = SQLiteSession(user_id)

    # Turn 1
    result = await Runner.run(
        agent,
        "Add a task to buy milk",
        session=session
    )
    print(result.final_output)  # "Task added!"

    # Turn 2 - Agent remembers context!
    result = await Runner.run(
        agent,
        "Also add eggs to the list",
        session=session
    )
    print(result.final_output)  # "Added eggs task!"

    # Turn 3
    result = await Runner.run(
        agent,
        "Show me what I need to buy",
        session=session
    )
    print(result.final_output)  # Lists both milk and eggs
```

**Why SQLiteSession?**
- ✅ Automatic conversation history
- ✅ Context preservation across turns
- ✅ No manual message management
- ✅ Works offline
- ✅ Fast and simple

---

### 4. Session Management - OpenAI Conversations API

```python
from agents import Agent, Runner, OpenAIConversationsSession

async def server_managed_chat():
    agent = Agent(
        name="Todo Assistant",
        instructions="You are a helpful assistant."
    )

    # Server-managed conversation
    session = OpenAIConversationsSession()

    # Or resume existing conversation
    # session = OpenAIConversationsSession(conversation_id="conv_abc123")

    # First turn
    result = await Runner.run(
        agent,
        "What tasks do I have?",
        session=session
    )
    print(result.final_output)

    # Get conversation ID for later
    conv_id = session.conversation_id
    print(f"Conversation ID: {conv_id}")
```

**When to use OpenAIConversationsSession vs SQLiteSession?**

| Feature | SQLiteSession | OpenAIConversationsSession |
|---------|---------------|----------------------------|
| Storage | Local SQLite DB | OpenAI servers |
| Offline | ✅ Yes | ❌ No |
| Multi-device sync | ❌ No | ✅ Yes |
| Privacy | ✅ Local | ⚠️ Server-side |
| Setup | Simple | Requires API key |

**Recommendation for Phase 3**: Use **SQLiteSession** for simplicity.

---

### 5. Complete Phase 3 Integration

```python
import asyncio
from agents import Agent, Runner, SQLiteSession
from agents.mcp import MCPServerStreamableHttp

class TodoChatbot:
    def __init__(self, mcp_url: str = "http://localhost:8001/mcp"):
        self.mcp_url = mcp_url
        self.agent = None
        self.mcp_server = None

    async def initialize(self):
        """Initialize MCP connection and agent"""
        self.mcp_server = MCPServerStreamableHttp(
            name="TodoMCP",
            params={"url": self.mcp_url},
            cache_tools_list=True
        )

        await self.mcp_server.__aenter__()

        self.agent = Agent(
            name="Todo Assistant",
            instructions="""
            You are a friendly todo list manager.

            Guidelines:
            1. Always confirm after adding/updating/deleting tasks
            2. When listing tasks, format them clearly
            3. Ask for clarification if the request is ambiguous
            4. Be concise but helpful

            Remember: All operations require the user's JWT token for security.
            """,
            mcp_servers=[self.mcp_server],
            model="gpt-4"
        )

    async def chat(self, user_id: str, message: str, jwt_token: str) -> str:
        """
        Handle a chat message

        Args:
            user_id: Unique user identifier
            message: User's message
            jwt_token: User's authentication token

        Returns:
            Assistant's response
        """
        # Create/resume session
        session = SQLiteSession(user_id)

        # Inject JWT token into context
        # (Agent will use this when calling MCP tools)
        enhanced_message = f"[JWT: {jwt_token}]\n{message}"

        result = await Runner.run(
            self.agent,
            enhanced_message,
            session=session
        )

        return result.final_output

    async def cleanup(self):
        """Cleanup resources"""
        if self.mcp_server:
            await self.mcp_server.__aexit__(None, None, None)

# Usage
async def main():
    chatbot = TodoChatbot()
    await chatbot.initialize()

    try:
        # Simulate conversation
        user_id = "user_123"
        jwt_token = "eyJ..."  # From Better Auth

        response = await chatbot.chat(
            user_id,
            "Add a task to prepare presentation",
            jwt_token
        )
        print(f"Bot: {response}")

        response = await chatbot.chat(
            user_id,
            "What tasks do I have?",
            jwt_token
        )
        print(f"Bot: {response}")

    finally:
        await chatbot.cleanup()

asyncio.run(main())
```

---

### 6. Streaming Responses (Real-time)

```python
from agents import Agent, Runner, StreamEventType

async def stream_response(agent: Agent, message: str):
    """Stream agent response in real-time"""

    async for event in Runner.stream(agent, message):
        if event.type == StreamEventType.TEXT_DELTA:
            # Print each chunk as it arrives
            print(event.data, end="", flush=True)

        elif event.type == StreamEventType.TOOL_CALL_START:
            print(f"\n[Calling tool: {event.data.tool_name}]")

        elif event.type == StreamEventType.TOOL_CALL_END:
            print(f"[Tool completed]")

        elif event.type == StreamEventType.COMPLETED:
            print("\n[Done]")

# Usage
agent = Agent(name="Assistant", instructions="Be helpful")
await stream_response(agent, "Add task to buy milk")
```

**Output:**
```
[Calling tool: add_task]
[Tool completed]
I've added "buy milk" to your todo list!
[Done]
```

---

### 7. Error Handling

```python
from agents import Agent, Runner, RunError

async def safe_chat(agent: Agent, message: str):
    try:
        result = await Runner.run(agent, message)
        return result.final_output

    except RunError as e:
        # Agent execution error
        print(f"Agent error: {e}")
        return "Sorry, I couldn't process that. Please try again."

    except Exception as e:
        # Unexpected error
        print(f"Unexpected error: {e}")
        return "An error occurred. Please contact support."
```

---

### 8. Custom Tool Approval (Security)

```python
from agents import Agent, HostedMCPTool

# Require approval for sensitive operations
agent = Agent(
    name="Todo Assistant",
    tools=[
        HostedMCPTool(
            tool_config={
                "type": "mcp",
                "server_label": "TodoMCP",
                "server_url": "http://localhost:8001/mcp",
                "require_approval": "always"  # or "never", "on_sensitive"
            }
        )
    ]
)
```

**Approval Levels:**
- `"never"`: Auto-execute all tools (fastest)
- `"on_sensitive"`: Ask for sensitive operations
- `"always"`: Ask before every tool call (safest)

**Phase 3 Recommendation**: Use `"never"` since we handle auth via JWT.

---

## Phase 3 Implementation Checklist

### Step 1: Install Dependencies
```bash
pip install agents openai sqlalchemy
```

### Step 2: Environment Setup
```python
# .env
OPENAI_API_KEY=sk-...
MCP_SERVER_URL=http://localhost:8001/mcp
```

### Step 3: Create Agent Service
```python
# services/agent_service.py
from agents import Agent, Runner, SQLiteSession
from agents.mcp import MCPServerStreamableHttp
import os

class AgentService:
    def __init__(self):
        self.mcp_url = os.getenv("MCP_SERVER_URL")
        self.agent = None

    async def init_agent(self):
        mcp_server = MCPServerStreamableHttp(
            name="TodoMCP",
            params={"url": self.mcp_url}
        )
        await mcp_server.__aenter__()

        self.agent = Agent(
            name="Todo Assistant",
            instructions="You are a helpful todo manager.",
            mcp_servers=[mcp_server]
        )

    async def process_message(self, user_id: str, message: str, jwt: str):
        session = SQLiteSession(user_id)
        result = await Runner.run(
            self.agent,
            f"[JWT:{jwt}] {message}",
            session=session
        )
        return result.final_output
```

### Step 4: Create API Endpoint (FastAPI)
```python
# routers/chat.py
from fastapi import APIRouter, Depends
from services.agent_service import AgentService
from auth.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])
agent_service = AgentService()

@router.post("/message")
async def chat_message(
    message: str,
    user = Depends(get_current_user)
):
    response = await agent_service.process_message(
        user_id=str(user.id),
        message=message,
        jwt=user.jwt_token
    )
    return {"response": response}
```

---

## Natural Language Processing Examples

Agent will interpret these inputs:

| User Input | Agent Understanding | MCP Tool | Parameters |
|------------|---------------------|----------|------------|
| "Add groceries task" | Create new task | `add_task` | `title="Groceries"` |
| "I need to buy milk and eggs" | Create task with description | `add_task` | `title="Buy milk and eggs"` |
| "Show my tasks" | List all tasks | `list_tasks` | `filter="all"` |
| "What do I need to do today?" | List pending tasks | `list_tasks` | `filter="pending"` |
| "Mark task 5 as done" | Complete specific task | `complete_task` | `task_id=5` |
| "I finished the presentation" | Complete task by name | `complete_task` | (finds task by title) |
| "Remove the meeting task" | Delete task | `delete_task` | (finds task by title) |
| "Change task 3 to Call John" | Update task title | `update_task` | `task_id=3, title="Call John"` |

**Key Insight**: The agent doesn't need explicit tool names - it understands from context!

---

## Database Schema for Conversations

```sql
-- Conversation table (managed by SQLiteSession)
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    tool_calls TEXT,  -- JSON array of tool calls
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

**Note**: SQLiteSession handles this automatically!

---

## Performance Optimization

### 1. Connection Pooling
```python
# Reuse agent instance
class AgentPool:
    _instance = None

    @classmethod
    def get_agent(cls):
        if cls._instance is None:
            cls._instance = Agent(...)
        return cls._instance
```

### 2. Caching Tool Definitions
```python
mcp_server = MCPServerStreamableHttp(
    name="TodoMCP",
    params={"url": "..."},
    cache_tools_list=True  # ✅ Faster subsequent calls
)
```

### 3. Async Everything
```python
# DON'T: Blocking call
result = Runner.run_sync(agent, message)

# DO: Async call
result = await Runner.run(agent, message)
```

---

## Testing

### Unit Test Example
```python
import pytest
from services.agent_service import AgentService

@pytest.mark.asyncio
async def test_add_task():
    service = AgentService()
    await service.init_agent()

    response = await service.process_message(
        user_id="test_user",
        message="Add task to test the agent",
        jwt="test_token"
    )

    assert "added" in response.lower()
```

### Integration Test
```python
@pytest.mark.asyncio
async def test_conversation_flow():
    service = AgentService()
    await service.init_agent()

    # Add task
    resp1 = await service.process_message(
        "test_user", "Add buy milk", "token"
    )

    # List tasks
    resp2 = await service.process_message(
        "test_user", "What are my tasks?", "token"
    )

    assert "milk" in resp2.lower()
```

---

## Common Pitfalls & Solutions

### ❌ Pitfall 1: Forgetting to pass JWT token
```python
# WRONG - MCP tools will fail authentication
result = await Runner.run(agent, "Add task")

# CORRECT - Include JWT in message context
result = await Runner.run(
    agent,
    f"[JWT:{user_jwt}] Add task"
)
```

### ❌ Pitfall 2: Not handling async context managers
```python
# WRONG - MCP server connection leaked
mcp_server = MCPServerStreamableHttp(...)
agent = Agent(mcp_servers=[mcp_server])  # Won't work!

# CORRECT - Use async context manager
async with MCPServerStreamableHttp(...) as server:
    agent = Agent(mcp_servers=[server])
```

### ❌ Pitfall 3: Blocking the event loop
```python
# WRONG - Blocks async execution
result = Runner.run_sync(agent, message)

# CORRECT - Use async
result = await Runner.run(agent, message)
```

---

## Debugging Tips

### 1. Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Inspect Tool Calls
```python
result = await Runner.run(agent, message)

# See what tools were called
for tool_call in result.tool_calls:
    print(f"Tool: {tool_call.name}")
    print(f"Args: {tool_call.arguments}")
    print(f"Result: {tool_call.result}")
```

### 3. Test MCP Connection
```python
async def test_mcp_connection():
    async with MCPServerStreamableHttp(
        name="Test",
        params={"url": "http://localhost:8001/mcp"}
    ) as server:
        tools = await server.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
```

---

## When to Use This Skill

- ✅ Creating AI chatbot for Phase 3
- ✅ Integrating MCP tools with AI agent
- ✅ Managing conversation sessions
- ✅ Handling natural language input
- ✅ Debugging agent behavior

## When to Use Context7 Instead

- 🔍 Need latest Agents SDK API reference
- 🔍 Exploring new agent features
- 🔍 Checking breaking changes in SDK

## When to Use MCP Tools Skill Instead

- 🔧 Creating/debugging MCP server
- 🔧 Defining new tools
- 🔧 Database integration issues

---

## Version
**Last Updated**: 2026-02-04
**OpenAI Agents SDK**: Latest (via Context7)
**Status**: Active for Phase 3 Development
