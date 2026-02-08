# MCP Tools Skill - Phase 3 AI Chatbot

## Purpose
Complete guide for creating MCP (Model Context Protocol) server for Phase 3. This skill will teach you how to create todo management tools for AI chatbot using latest MCP SDK patterns.

## What is MCP?
MCP is a protocol that allows AI agents to connect to external tools. In Phase 3, our AI chatbot will have 5 tools that interact with the todo database.

## Technology Stack
- **MCP SDK**: Official Python SDK (`mcp` package)
- **Database**: SQLModel ORM with Neon PostgreSQL
- **Authentication**: Better Auth JWT tokens
- **Framework**: FastAPI backend integration

---

## Architecture Overview

```
┌─────────────────┐
│  AI Agent       │
│ (OpenAI Agents) │
└────────┬────────┘
         │ MCP Protocol
         ▼
┌─────────────────┐
│  MCP Server     │
│  (5 Tools)      │
└────────┬────────┘
         │ SQLModel
         ▼
┌─────────────────┐
│  Database       │
│  (Neon PG)      │
└─────────────────┘
```

**Key Point**: MCP server is stateless - all state is stored in the database.

---

## Latest MCP SDK Patterns

### 1. Server Initialization with Lifespan Management

```python
from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session

# Database engine (shared resource)
engine = None

@asynccontextmanager
async def lifespan(server):
    """Startup/shutdown lifecycle management"""
    global engine
    # Startup: Initialize database connection
    engine = create_engine(
        settings.database_url,
        echo=True,
        pool_pre_ping=True  # Connection health check
    )
    print("✅ Database connected")

    yield  # Server runs

    # Shutdown: Cleanup
    engine.dispose()
    print("🔌 Database disconnected")

# Initialize MCP server with lifespan
mcp = FastMCP("todo-mcp-server", lifespan=lifespan)
```

**Why Lifespan?**
- Properly manage database connections
- Graceful startup/shutdown
- Resource cleanup guaranteed

---

### 2. Tool Definition Pattern

MCP SDK uses `@server.tool()` decorator for tool definitions:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.tool()
async def tool_name(
    param1: str,
    param2: int = 10  # Optional parameter with default
) -> str:
    """
    Tool description in docstring.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2

    Returns:
        Result description
    """
    # Tool logic here
    return "Tool result"
```

**Best Practices**:
- Clear docstrings (AI agent reads these!)
- Type hints for all parameters
- Return type annotation
- Optional parameters with sensible defaults

---

### 3. Database Integration Pattern

```python
from sqlmodel import Session, select
from app.database import engine
from app.models.task import Task
from app.auth.dependencies import get_user_from_token

@server.tool()
async def get_user_tasks(jwt_token: str) -> str:
    """
    Get all tasks for authenticated user.

    Args:
        jwt_token: Better Auth JWT token

    Returns:
        JSON string of tasks
    """
    try:
        # 1. Authenticate user
        user = await get_user_from_token(jwt_token)
        if not user:
            return json.dumps({"error": "Invalid authentication"})

        # 2. Query database
        with Session(engine) as session:
            statement = select(Task).where(Task.user_id == user.id)
            tasks = session.exec(statement).all()

        # 3. Format response
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]

        return json.dumps({"tasks": task_list, "count": len(task_list)})

    except Exception as e:
        return json.dumps({"error": str(e)})
```

**Pattern Steps**:
1. **Authenticate**: Verify JWT token
2. **Query**: Use SQLModel session
3. **Format**: Return JSON string
4. **Error Handle**: Catch exceptions

---

## Phase 3: 5 Required MCP Tools

### Tool 1: add_task

```python
@server.tool()
async def add_task(
    jwt_token: str,
    title: str,
    description: str = ""
) -> str:
    """
    Add a new task for the authenticated user.

    Args:
        jwt_token: Better Auth JWT token
        title: Task title (required)
        description: Optional task description

    Returns:
        JSON with created task or error
    """
    try:
        # Authenticate
        user = await get_user_from_token(jwt_token)
        if not user:
            return json.dumps({"error": "Unauthorized"})

        # Create task
        with Session(engine) as session:
            new_task = Task(
                title=title,
                description=description,
                user_id=user.id,
                completed=False
            )
            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            return json.dumps({
                "success": True,
                "task": {
                    "id": new_task.id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "completed": new_task.completed
                }
            })

    except Exception as e:
        return json.dumps({"error": str(e)})
```

---

### Tool 2: list_tasks

```python
@server.tool()
async def list_tasks(
    jwt_token: str,
    filter: str = "all"  # "all", "completed", "pending"
) -> str:
    """
    List tasks with optional filter.

    Args:
        jwt_token: Better Auth JWT token
        filter: Filter type - "all", "completed", or "pending"

    Returns:
        JSON with task list or error
    """
    try:
        user = await get_user_from_token(jwt_token)
        if not user:
            return json.dumps({"error": "Unauthorized"})

        with Session(engine) as session:
            # Base query
            statement = select(Task).where(Task.user_id == user.id)

            # Apply filter
            if filter == "completed":
                statement = statement.where(Task.completed == True)
            elif filter == "pending":
                statement = statement.where(Task.completed == False)

            tasks = session.exec(statement).all()

            task_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat()
                }
                for task in tasks
            ]

            return json.dumps({
                "tasks": task_list,
                "count": len(task_list),
                "filter": filter
            })

    except Exception as e:
        return json.dumps({"error": str(e)})
```

---

### Tool 3: complete_task

```python
@server.tool()
async def complete_task(
    jwt_token: str,
    task_id: int
) -> str:
    """
    Mark a task as completed.

    Args:
        jwt_token: Better Auth JWT token
        task_id: ID of task to complete

    Returns:
        JSON with updated task or error
    """
    try:
        user = await get_user_from_token(jwt_token)
        if not user:
            return json.dumps({"error": "Unauthorized"})

        with Session(engine) as session:
            # Find task
            task = session.get(Task, task_id)

            if not task:
                return json.dumps({"error": "Task not found"})

            # Verify ownership
            if task.user_id != user.id:
                return json.dumps({"error": "Not your task"})

            # Update
            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            return json.dumps({
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed
                }
            })

    except Exception as e:
        return json.dumps({"error": str(e)})
```

---

### Tool 4: delete_task

```python
@server.tool()
async def delete_task(
    jwt_token: str,
    task_id: int
) -> str:
    """
    Delete a task permanently.

    Args:
        jwt_token: Better Auth JWT token
        task_id: ID of task to delete

    Returns:
        JSON with success status or error
    """
    try:
        user = await get_user_from_token(jwt_token)
        if not user:
            return json.dumps({"error": "Unauthorized"})

        with Session(engine) as session:
            task = session.get(Task, task_id)

            if not task:
                return json.dumps({"error": "Task not found"})

            if task.user_id != user.id:
                return json.dumps({"error": "Not your task"})

            # Delete
            session.delete(task)
            session.commit()

            return json.dumps({
                "success": True,
                "message": f"Task '{task.title}' deleted"
            })

    except Exception as e:
        return json.dumps({"error": str(e)})
```

---

### Tool 5: update_task

```python
@server.tool()
async def update_task(
    jwt_token: str,
    task_id: int,
    title: str = None,
    description: str = None,
    completed: bool = None
) -> str:
    """
    Update task details.

    Args:
        jwt_token: Better Auth JWT token
        task_id: ID of task to update
        title: New title (optional)
        description: New description (optional)
        completed: New completed status (optional)

    Returns:
        JSON with updated task or error
    """
    try:
        user = await get_user_from_token(jwt_token)
        if not user:
            return json.dumps({"error": "Unauthorized"})

        with Session(engine) as session:
            task = session.get(Task, task_id)

            if not task:
                return json.dumps({"error": "Task not found"})

            if task.user_id != user.id:
                return json.dumps({"error": "Not your task"})

            # Update only provided fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed

            session.add(task)
            session.commit()
            session.refresh(task)

            return json.dumps({
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
            })

    except Exception as e:
        return json.dumps({"error": str(e)})
```

---

## Error Handling Best Practices

```python
from enum import Enum

class ErrorCode(Enum):
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "not_found"
    FORBIDDEN = "forbidden"
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"

def error_response(code: ErrorCode, message: str):
    """Standardized error response"""
    return json.dumps({
        "error": {
            "code": code.value,
            "message": message
        }
    })

# Usage in tool
@server.tool()
async def example_tool(jwt_token: str) -> str:
    try:
        user = await get_user_from_token(jwt_token)
        if not user:
            return error_response(
                ErrorCode.UNAUTHORIZED,
                "Invalid or expired token"
            )
        # ... rest of logic
    except ValueError as e:
        return error_response(
            ErrorCode.VALIDATION_ERROR,
            str(e)
        )
    except Exception as e:
        return error_response(
            ErrorCode.SERVER_ERROR,
            "An unexpected error occurred"
        )
```

---

## Testing MCP Tools

### Manual Testing with MCP Inspector

```bash
# Install MCP inspector
npm install -g @modelcontextprotocol/inspector

# Run your MCP server
python -m uvicorn mcp_server:app --port 8001

# Open inspector
mcp-inspector
```

### Programmatic Testing

```python
import asyncio
from mcp.client import Client

async def test_add_task():
    client = Client("http://localhost:8001")

    result = await client.call_tool(
        "add_task",
        {
            "jwt_token": "your-test-token",
            "title": "Test task",
            "description": "Testing MCP tool"
        }
    )

    print(result)

asyncio.run(test_add_task())
```

---

## Configuration & Environment

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    mcp_server_port: int = 8001

    class Config:
        env_file = ".env"

settings = Settings()
```

```env
# .env file
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-secret-key
MCP_SERVER_PORT=8001
```

---

## File Structure

```
apps/backend/
├── mcp_server/
│   ├── __init__.py
│   ├── server.py          # MCP server initialization
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── add_task.py
│   │   ├── list_tasks.py
│   │   ├── complete_task.py
│   │   ├── delete_task.py
│   │   └── update_task.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── errors.py      # Error handling utilities
│   └── config.py          # MCP-specific config
└── requirements.txt
```

---

## Common Pitfalls & Solutions

### ❌ Pitfall 1: Not handling database sessions properly
```python
# WRONG
session = Session(engine)
task = session.get(Task, task_id)
# Session never closed!
```

```python
# CORRECT
with Session(engine) as session:
    task = session.get(Task, task_id)
# Session auto-closed
```

### ❌ Pitfall 2: Returning Python objects instead of JSON strings
```python
# WRONG
return {"error": "Not found"}  # MCP expects strings!

# CORRECT
return json.dumps({"error": "Not found"})
```

### ❌ Pitfall 3: Not verifying task ownership
```python
# WRONG
task = session.get(Task, task_id)
session.delete(task)  # Anyone can delete anyone's task!

# CORRECT
task = session.get(Task, task_id)
if task.user_id != user.id:
    return error_response(ErrorCode.FORBIDDEN, "Not your task")
session.delete(task)
```

---

## Natural Language Examples

AI agent will interpret natural language like:

| User Input | MCP Tool Called | Parameters |
|------------|----------------|------------|
| "Add a task to buy groceries" | `add_task` | `title="Buy groceries"` |
| "Show me all my tasks" | `list_tasks` | `filter="all"` |
| "Mark task 5 as done" | `complete_task` | `task_id=5` |
| "Delete the meeting task" | `delete_task` | `task_id=<extracted from context>` |
| "Change task 3 title to 'Call mom'" | `update_task` | `task_id=3, title="Call mom"` |

---

## Performance Tips

1. **Connection Pooling**: Use `pool_size` and `max_overflow` in SQLModel engine
```python
engine = create_engine(
    url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

2. **Caching**: Cache user authentication results
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def verify_token(token: str):
    # Token verification logic
    pass
```

3. **Async All The Way**: Use async database drivers if possible
```python
from sqlalchemy.ext.asyncio import create_async_engine
```

---

## When to Use This Skill

- ✅ Creating MCP server for Phase 3
- ✅ Defining new MCP tools
- ✅ Debugging tool call issues
- ✅ Understanding MCP-database integration
- ✅ Implementing authentication in tools

## When to Use Context7 Instead

- 🔍 Need latest MCP SDK API reference
- 🔍 Exploring new MCP features
- 🔍 Checking breaking changes in MCP updates

## When to Use Backend Sub-agent Instead

- 🤖 Complex SQLModel queries
- 🤖 FastAPI integration issues
- 🤖 Database migration problems

---

## Version
**Last Updated**: 2026-02-04
**MCP SDK Version**: Latest (via Context7)
**Status**: Active for Phase 3 Development
