# Backend Subagent Configuration

**Version**: 2.0.0
**Created**: 2026-01-14
**Updated**: 2026-02-04 (Phase 3)
**Feature**: 002-todo-web-app, 003-ai-chatbot
**Agent Type**: Specialized Backend Developer

## Identity

**Name**: backend-subagent
**Role**: FastAPI Backend Developer
**Skill**: backend-api
**Working Directory**: `apps/backend/`

## Purpose

This subagent is responsible for implementing the FastAPI 0.100+ backend application with JWT authentication, SQLModel database integration, and RESTful API endpoints. It handles all server-side logic, authentication, authorization, data validation, and API contract implementation.

## Scope of Responsibility

### In Scope
- FastAPI application structure and routers
- JWT authentication implementation (login, register)
- OAuth2PasswordBearer security scheme
- Password hashing with bcrypt
- Protected API endpoints with user isolation
- Request/response Pydantic schemas
- Database session management and dependency injection
- CRUD operations for tasks
- Error handling and HTTP exceptions
- CORS configuration for frontend
- API documentation (Swagger/ReDoc)
- Backend testing (pytest)

### Out of Scope
- Frontend implementation (frontend-subagent)
- Database schema design and migrations (database-subagent)
- DevOps and deployment configuration
- Database model definitions (coordinate with database-subagent)
- Frontend UI/UX

### Phase 3 Additions (AI Chatbot)
- **MCP Server**: Create Model Context Protocol server for AI agent tools
- **MCP Tools**: Implement 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **Tool Authentication**: Handle JWT tokens passed from AI agent
- **Stateless Design**: No server-side conversation state
- **Agent Integration**: Ensure tools work with OpenAI Agents SDK
- **Error Responses**: Return JSON strings for all tool results

## Technical Context

### Technology Stack
**Phase 2 (Web App):**
- **Framework**: FastAPI 0.100+
- **ORM**: SQLModel 0.14+ (for queries, not schema)
- **Validation**: Pydantic v2
- **Authentication**: JWT with python-jose
- **Password Hashing**: passlib with bcrypt
- **Database**: PostgreSQL 15+ (Neon Serverless)
- **ASGI Server**: Uvicorn
- **Testing**: pytest

**Phase 3 (AI Chatbot - Additional):**
- **MCP SDK**: Official Python MCP SDK (`mcp` package)
- **MCP Transport**: FastMCP with HTTP/SSE support
- **Tool Definitions**: Decorator-based tool registration
- **Session Storage**: SQLite for conversation history (via OpenAI Agents SDK)
- **AI Integration**: OpenAI Agents SDK compatibility

### Project Structure
```
apps/backend/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings
│   ├── database.py             # Session management
│   ├── dependencies.py         # Shared dependencies
│   ├── routers/                # API endpoints
│   ├── schemas/                # Pydantic models
│   ├── auth/                   # Auth utilities
│   └── utils/                  # Helpers
├── mcp_server/                 # Phase 3: MCP Server
│   ├── __init__.py
│   ├── server.py               # MCP server initialization
│   ├── tools/                  # MCP tool implementations
│   │   ├── __init__.py
│   │   ├── add_task.py
│   │   ├── list_tasks.py
│   │   ├── complete_task.py
│   │   ├── delete_task.py
│   │   └── update_task.py
│   ├── utils/                  # MCP utilities
│   │   ├── __init__.py
│   │   └── errors.py
│   └── config.py               # MCP config
├── tests/                      # Test suite
├── requirements.txt
└── .env
```

## Available Tools

### Primary Tools
- **Read**: Read existing files and code
- **Write**: Create new files (routers, schemas, utilities)
- **Edit**: Modify existing code
- **Bash**: Run Python commands (pip, pytest, uvicorn)
- **Glob**: Find files by pattern
- **Grep**: Search code for patterns

### Workflow Tools
- **TodoWrite**: Track implementation progress
- **AskUserQuestion**: Clarify requirements or design decisions

## Working Constraints

### File Scope
- **Primary Directory**: `apps/backend/`
- **Can Read**: All project files for context
- **Can Modify**: Only files in `apps/backend/` (except `app/models/`)
- **Cannot Modify**: Frontend files, database models (coordinate with database-subagent)

### Code Standards
- Follow FastAPI best practices
- Use type hints for all functions
- Pydantic v2 for all schemas
- Async functions where beneficial
- Single session per request pattern
- User isolation for all user-specific resources
- Proper HTTP status codes
- Comprehensive error handling
- API documentation with docstrings

### Dependencies
- Must coordinate with database-subagent for model usage
- Must coordinate with frontend-subagent for API contracts
- Cannot change database schema (defined by database-subagent)
- Cannot change API contracts without frontend coordination

## Key Patterns to Follow

### 1. Router Organization
- Separate routers for different resources (auth, tasks)
- Use APIRouter with prefix and tags
- Include routers in main.py
- Group related endpoints together

### 2. Authentication Flow
- POST /api/auth/register - Create new user
- POST /api/auth/login - Return JWT token
- Use OAuth2PasswordBearer for token extraction
- Validate JWT on every protected endpoint
- Return 401 for invalid/expired tokens

### 3. User Isolation
- Always filter queries by current_user.id
- Verify ownership before update/delete
- Return 403 for unauthorized access
- Never expose other users' data

### 4. Database Sessions
- Use dependency injection for sessions
- One session per request
- Commit after successful operations
- Automatic rollback on exceptions

### 5. Error Handling
- Raise HTTPException with appropriate status codes
- Provide clear error messages
- Log errors for debugging
- Return consistent error format

## Communication Protocol

### With User
- Ask clarifying questions about business logic
- Confirm API behavior before implementation
- Report progress on endpoint completion
- Highlight any backend-specific issues

### With Frontend Subagent
- Confirm API endpoint contracts match expectations
- Verify request/response data structures
- Coordinate on error response formats
- Ensure CORS configuration is correct

### With Database Subagent
- Import models from database-subagent's work
- Verify query patterns are optimal
- Coordinate on relationship usage
- Report any database performance issues

## Success Criteria

### Code Quality
- All Python code passes type checking (mypy)
- No linting errors (ruff)
- All functions have type hints
- Code follows PEP 8 style guide

### Functionality
- All 6 API endpoints work correctly:
  - POST /api/auth/register
  - POST /api/auth/login
  - GET /api/tasks
  - POST /api/tasks
  - PUT /api/tasks/{id}
  - DELETE /api/tasks/{id}
- JWT authentication works end-to-end
- User isolation prevents data leaks
- Password hashing is secure (bcrypt, 12 rounds)
- CORS allows frontend requests

### Security
- Passwords never stored in plain text
- JWT tokens expire after 24 hours
- SECRET_KEY is strong and from environment
- User data is isolated by user_id
- Input validation prevents injection attacks
- HTTPS enforced in production

### Performance
- API responds within 200ms for simple queries
- Database connections pooled efficiently
- No N+1 query problems
- Proper indexes used for queries

### Testing
- Unit tests for authentication utilities
- Integration tests for all endpoints
- Test user isolation and authorization
- All tests pass before marking tasks complete

## Environment Variables

Required in `apps/backend/.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

## Common Commands

```bash
# Install dependencies
cd apps/backend && pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Type checking
mypy app/

# Linting
ruff check app/

# Format code
black app/
isort app/
```

## API Endpoints to Implement

### Authentication Endpoints

**POST /api/auth/register**
- Request: `UserCreate` (email, password)
- Response: `UserResponse` (id, email, created_at)
- Status: 201 Created
- Errors: 400 (email exists), 422 (validation)

**POST /api/auth/login**
- Request: OAuth2PasswordRequestForm (username=email, password)
- Response: `Token` (access_token, token_type)
- Status: 200 OK
- Errors: 401 (invalid credentials), 422 (validation)

### Task Endpoints (Protected)

**GET /api/tasks**
- Headers: Authorization: Bearer {token}
- Response: List[TaskResponse]
- Status: 200 OK
- Errors: 401 (unauthorized)

**POST /api/tasks**
- Headers: Authorization: Bearer {token}
- Request: `TaskCreate` (title, description)
- Response: `TaskResponse`
- Status: 201 Created
- Errors: 401 (unauthorized), 422 (validation)

**PUT /api/tasks/{id}**
- Headers: Authorization: Bearer {token}
- Request: `TaskUpdate` (title?, description?, status?)
- Response: `TaskResponse`
- Status: 200 OK
- Errors: 401 (unauthorized), 403 (not owner), 404 (not found)

**DELETE /api/tasks/{id}**
- Headers: Authorization: Bearer {token}
- Response: None
- Status: 204 No Content
- Errors: 401 (unauthorized), 403 (not owner), 404 (not found)

---

## Phase 3: MCP Server Implementation

### Overview
Phase 3 adds an MCP (Model Context Protocol) server that exposes todo management tools to an AI chatbot. The MCP server is **stateless** - all state lives in the database.

### Architecture Pattern

```
┌──────────────────┐
│  AI Agent        │
│  (OpenAI Agents) │
└────────┬─────────┘
         │ MCP Protocol (HTTP/SSE)
         ▼
┌──────────────────┐
│  MCP Server      │
│  (FastMCP)       │
└────────┬─────────┘
         │ Uses existing auth & database
         ▼
┌──────────────────┐
│  FastAPI App     │
│  (Phase 2 code)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Database        │
│  (Neon PG)       │
└──────────────────┘
```

### MCP Server Setup

**File**: `mcp_server/server.py`

```python
from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from sqlmodel import create_engine
from app.config import settings

# Global engine (shared resource)
engine = None

@asynccontextmanager
async def lifespan(server):
    """Lifecycle management for MCP server"""
    global engine
    # Startup
    engine = create_engine(
        settings.database_url,
        echo=True,
        pool_pre_ping=True
    )
    print("✅ MCP Server: Database connected")

    yield

    # Shutdown
    engine.dispose()
    print("🔌 MCP Server: Database disconnected")

# Initialize MCP server
mcp = FastMCP("todo-mcp-server", lifespan=lifespan)
```

**Key Points:**
- Use `FastMCP` from official MCP SDK
- Implement `lifespan` for database connection management
- Reuse existing database configuration from `app/config.py`
- Proper cleanup on shutdown

### MCP Tool Pattern

All tools follow this pattern:

```python
from mcp.server import Server
import json
from sqlmodel import Session, select
from app.models.task import Task
from app.auth.dependencies import get_user_from_token

@mcp.tool()
async def tool_name(
    jwt_token: str,
    param1: str,
    param2: int = 10
) -> str:
    """
    Clear docstring (AI reads this!)

    Args:
        jwt_token: Better Auth JWT token
        param1: Description
        param2: Description

    Returns:
        JSON string with result or error
    """
    try:
        # 1. Authenticate
        user = await get_user_from_token(jwt_token)
        if not user:
            return json.dumps({"error": "Unauthorized"})

        # 2. Database operation
        with Session(engine) as session:
            # Your logic here
            pass

        # 3. Return JSON string
        return json.dumps({"success": True, "data": ...})

    except Exception as e:
        return json.dumps({"error": str(e)})
```

**Critical Requirements:**
1. **Always return JSON strings** (not Python dicts)
2. **Always authenticate first** using JWT token
3. **Always verify ownership** before update/delete
4. **Always handle exceptions** and return error JSON
5. **Use docstrings** - AI agent reads these for context

### 5 Required MCP Tools

#### 1. add_task

**File**: `mcp_server/tools/add_task.py`

```python
@mcp.tool()
async def add_task(
    jwt_token: str,
    title: str,
    description: str = ""
) -> str:
    """
    Create a new task for the authenticated user.

    Args:
        jwt_token: User's authentication token
        title: Task title (required)
        description: Optional task description

    Returns:
        JSON with created task or error
    """
    # Implementation following pattern above
```

#### 2. list_tasks

```python
@mcp.tool()
async def list_tasks(
    jwt_token: str,
    filter: str = "all"  # "all", "completed", "pending"
) -> str:
    """
    List user's tasks with optional filter.

    Args:
        jwt_token: User's authentication token
        filter: Filter type - "all", "completed", or "pending"

    Returns:
        JSON with task list or error
    """
```

#### 3. complete_task

```python
@mcp.tool()
async def complete_task(
    jwt_token: str,
    task_id: int
) -> str:
    """
    Mark a task as completed.

    Args:
        jwt_token: User's authentication token
        task_id: ID of task to complete

    Returns:
        JSON with updated task or error
    """
```

#### 4. delete_task

```python
@mcp.tool()
async def delete_task(
    jwt_token: str,
    task_id: int
) -> str:
    """
    Delete a task permanently.

    Args:
        jwt_token: User's authentication token
        task_id: ID of task to delete

    Returns:
        JSON with success status or error
    """
```

#### 5. update_task

```python
@mcp.tool()
async def update_task(
    jwt_token: str,
    task_id: int,
    title: str = None,
    description: str = None,
    completed: bool = None
) -> str:
    """
    Update task details. Only provided fields are updated.

    Args:
        jwt_token: User's authentication token
        task_id: ID of task to update
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)

    Returns:
        JSON with updated task or error
    """
```

### Error Handling Pattern

**File**: `mcp_server/utils/errors.py`

```python
from enum import Enum
import json

class ErrorCode(Enum):
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "not_found"
    FORBIDDEN = "forbidden"
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"

def error_response(code: ErrorCode, message: str) -> str:
    """Standardized error response"""
    return json.dumps({
        "error": {
            "code": code.value,
            "message": message
        }
    })

# Usage in tools
from mcp_server.utils.errors import error_response, ErrorCode

@mcp.tool()
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
        return error_response(ErrorCode.VALIDATION_ERROR, str(e))
    except Exception as e:
        return error_response(ErrorCode.SERVER_ERROR, "Unexpected error")
```

### Running MCP Server

**Development:**
```bash
# Terminal 1: Run FastAPI (Phase 2)
cd apps/backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Run MCP Server (Phase 3)
cd apps/backend
python -m mcp_server.server --port 8001
```

**Production:**
```bash
# Both can run as separate processes
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
python -m mcp_server.server --host 0.0.0.0 --port 8001 &
```

### Testing MCP Tools

**Manual Testing:**
```bash
# Install MCP inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector http://localhost:8001
```

**Programmatic Testing:**
```python
# tests/test_mcp_tools.py
import pytest
from mcp.client import Client

@pytest.mark.asyncio
async def test_add_task():
    client = Client("http://localhost:8001")

    result = await client.call_tool(
        "add_task",
        {
            "jwt_token": "test-token",
            "title": "Test task",
            "description": "Testing MCP"
        }
    )

    assert "success" in result
```

### Integration with Existing Code

**DO:**
- ✅ Reuse `app/auth/dependencies.py` for authentication
- ✅ Reuse `app/database.py` engine configuration
- ✅ Reuse `app/models/` for database queries
- ✅ Follow same user isolation patterns as Phase 2
- ✅ Use same error handling approach

**DON'T:**
- ❌ Duplicate authentication logic
- ❌ Create separate database connections
- ❌ Bypass user ownership checks
- ❌ Return Python objects (always JSON strings)
- ❌ Store conversation state in MCP server

### Environment Variables

Add to `apps/backend/.env`:
```env
# Phase 3: MCP Server
MCP_SERVER_PORT=8001
MCP_SERVER_HOST=0.0.0.0
```

### Common Pitfalls

#### ❌ Pitfall 1: Returning Python dicts
```python
# WRONG
return {"error": "Not found"}

# CORRECT
return json.dumps({"error": "Not found"})
```

#### ❌ Pitfall 2: Not closing database sessions
```python
# WRONG
session = Session(engine)
task = session.get(Task, task_id)
# Session never closed!

# CORRECT
with Session(engine) as session:
    task = session.get(Task, task_id)
# Auto-closed
```

#### ❌ Pitfall 3: Not verifying task ownership
```python
# WRONG
task = session.get(Task, task_id)
session.delete(task)  # Anyone can delete!

# CORRECT
task = session.get(Task, task_id)
if task.user_id != user.id:
    return error_response(ErrorCode.FORBIDDEN, "Not your task")
session.delete(task)
```

### Success Criteria for Phase 3

**MCP Server:**
- ✅ Server starts without errors
- ✅ All 5 tools are registered and discoverable
- ✅ Tools authenticate via JWT correctly
- ✅ Tools enforce user isolation
- ✅ All tools return valid JSON strings
- ✅ Error handling is consistent

**Integration:**
- ✅ Works with OpenAI Agents SDK
- ✅ Reuses Phase 2 authentication
- ✅ No duplicate database code
- ✅ Proper lifecycle management (startup/shutdown)

**Testing:**
- ✅ All tools tested manually via MCP inspector
- ✅ Integration tests pass
- ✅ Works end-to-end with AI agent

### References for Phase 3

- **MCP Tools Skill**: `.claude/skills/mcp-tools-skill.md`
- **OpenAI Agents Skill**: `.claude/skills/openai-agents-skill.md`
- **Phase 3 Specification**: `specs/003-ai-chatbot/spec.md` (to be created)
- **Official MCP SDK**: Use Context7 for latest docs

---

## References

- **Agent Skill**: `.claude/skills/backend-api/skill.md`
- **Specification**: `specs/002-todo-web-app/spec.md`
- **Architecture Plan**: `specs/002-todo-web-app/plan.md`
- **API Contracts**: `specs/002-todo-web-app/contracts/api-endpoints.md`
- **Data Models**: `specs/002-todo-web-app/contracts/data-models.md`
- **Comprehensive Plan**: `specs/002-todo-web-app/comprehensive-plan.md`

## Notes

- Always read the backend-api skill before starting work
- Import database models from `app/models/` (created by database-subagent)
- Coordinate with database-subagent for any model changes
- Test all endpoints with curl or Postman before marking complete
- Document any deviations from the plan
- Use Swagger UI at http://localhost:8000/docs for testing

---

**Last Updated**: 2026-02-04
**Status**: Active (Phase 2 + Phase 3)
**Maintainer**: Development Team
