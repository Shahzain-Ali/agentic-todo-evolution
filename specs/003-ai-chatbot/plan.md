# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot` | **Date**: 2026-02-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

## Summary

Build a natural language interface for todo management using OpenAI Agents SDK, Model Context Protocol (MCP) server, and ChatKit React component. Users interact with todos through conversational AI instead of traditional forms. The system consists of three layers: (1) ChatKit frontend providing chat UI, (2) OpenAI Agent with access to MCP tools, and (3) MCP server exposing 5 todo management tools (add_task, list_tasks, complete_task, delete_task, update_task) that interact with the existing Phase 2 database.

## Technical Context

**Language/Version**:
- **Backend**: Python 3.11+ (matches Phase 2)
- **Frontend**: TypeScript 5+ / JavaScript ES2022 (matches Phase 2)
- **MCP Server**: Python 3.11+ (new component)

**Primary Dependencies**:
- **Backend (existing)**: FastAPI 0.100+, SQLModel 0.14+, Better Auth
- **MCP Server (new)**: `mcp` (official Python SDK), FastMCP for HTTP/SSE transport
- **AI Agent (new)**: OpenAI Agents SDK (`agents` Python package), OpenAI API
- **Frontend (new component)**: `@openai/chatkit-react`, Next.js 16 App Router
- **Session Storage (new)**: SQLite for conversation history (managed by Agents SDK)

**Storage**:
- **Primary Database**: PostgreSQL 15+ (Neon Serverless) - reuses Phase 2 schema
- **Conversation History**: SQLite (local storage for chat sessions)
- **Authentication**: Reuses Phase 2 Better Auth JWT tokens

**Testing**:
- **Backend MCP Tools**: pytest with async support
- **Frontend ChatKit Integration**: Jest + React Testing Library
- **Integration**: Manual testing with MCP Inspector, end-to-end with real OpenAI agent

**Target Platform**:
- **MCP Server**: Linux server (WSL/Docker compatible)
- **Frontend**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- **AI Agent**: Server-side only (OpenAI infrastructure or self-hosted)

**Project Type**: Web application (extends Phase 2 monorepo with new MCP server component)

**Performance Goals**:
- Chat message response time: < 3 seconds (includes AI processing + tool execution)
- MCP tool execution: < 500ms for CRUD operations
- ChatKit UI render: < 100ms
- Support 100 concurrent chat sessions
- Conversation history: Handle 1000+ messages per session

**Constraints**:
- **Stateless MCP Server**: No conversation state stored in MCP layer (all state in database or Agents SDK)
- **OpenAI API Rate Limits**: Subject to OpenAI API quotas (consider fallback/retry logic)
- **Cost**: OpenAI API calls incur cost ($0.15$ Input-0.6 Output per 1K tokens for GPT-4o mini)
- **Latency**: Network round-trips to OpenAI add 1-2 seconds base latency
- **Session Scope**: Conversation history is per-session, not cross-device (Phase 3 limitation)

**Scale/Scope**:
- **Users**: Supports existing Phase 2 user base (designed for 10K users)
- **Concurrent Sessions**: 100 simultaneous chat sessions
- **Message Volume**: 1000 messages per conversation session
- **MCP Tools**: Exactly 5 tools (no tool expansion in Phase 3)
- **Natural Language**: English only for Phase 3

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development
- **Status**: PASS
- **Evidence**: Complete specification in `specs/003-ai-chatbot/spec.md` with 6 user stories, 15 functional requirements, and 10 success criteria
- **Action**: Implementation blocked until plan approval

### ✅ II. Test-Driven Development
- **Status**: PASS (design phase)
- **Commitment**:
  - MCP tools: Unit tests for each tool (add_task, list_tasks, etc.)
  - ChatKit integration: Component tests for chat interface
  - E2E tests: Natural language task creation, viewing, completion flows
  - Target coverage: 80% overall, 100% for MCP authentication and user isolation logic
- **Test Organization**:
  ```
  apps/backend/tests/
  ├── mcp/              # MCP server tests
  │   ├── test_add_task.py
  │   ├── test_list_tasks.py
  │   └── ...
  ├── integration/      # Cross-component tests
  └── e2e/             # Full chatbot flows

  apps/frontend/src/
  └── components/chat/__tests__/
      └── TodoChatbot.test.tsx
  ```

### ✅ III. Security by Design
- **Status**: PASS
- **Security Measures**:
  1. **Authentication**: Reuse Phase 2 Better Auth JWT tokens, passed from ChatKit → Agent → MCP tools
  2. **Authorization**: Every MCP tool validates JWT before database access
  3. **User Isolation**: All tools filter by `user_id` from validated JWT
  4. **Input Validation**: AI agent validates natural language intent; MCP tools validate parameters
  5. **Secrets Management**: OpenAI API key in `.env`, never in code or logs
  6. **API Security**: MCP server accessible only from localhost/internal network (not public internet)
  7. **Data Protection**: No sensitive data logged (sanitize task content from logs)
  8. **Rate Limiting**: Implement per-user rate limits for chat messages (prevent abuse)

### ✅ IV. Simplicity and YAGNI
- **Status**: PASS
- **Simple Choices**:
  - **No custom NLP**: Use OpenAI's built-in language understanding
  - **No custom chat UI**: Use pre-built ChatKit React component
  - **No new database tables**: Reuse Phase 2 Task/User schema (only add conversation history in SQLite)
  - **No microservices**: MCP server runs as additional process in same environment
  - **No caching layer**: Direct database queries (optimize if needed later)
  - **No tool orchestration**: Agent decides tool calls (no complex workflows)
- **Avoided Over-Engineering**:
  - ❌ Custom LLM training (using GPT-4o mini out-of-box)
  - ❌ Conversation branching/threading (single linear conversation)
  - ❌ Multi-modal input (text only, no voice/images)
  - ❌ Advanced NLU (OpenAI handles intent recognition)

### ✅ V. Documentation as Code
- **Status**: PASS (in progress)
- **Deliverables**:
  - ✅ Specification: `specs/003-ai-chatbot/spec.md`
  - 🚧 Implementation Plan: This file
  - 📋 Data Model: `data-model.md` (Phase 1)
  - 📋 API Contracts: `contracts/mcp-tools.yaml` (Phase 1)
  - 📋 Quickstart: `quickstart.md` (Phase 1)
  - 📋 Code Documentation: Docstrings for all MCP tools + ChatKit setup
  - 📋 Architecture Diagrams: Flow diagrams in plan

### ✅ VI. Observability and Debugging
- **Status**: PASS (planned)
- **Logging Strategy**:
  - **MCP Server**: Structured JSON logs (tool calls, execution time, errors)
  - **AI Agent**: Log tool invocations and parameters (sanitize user content)
  - **Frontend**: Log ChatKit errors and session lifecycle events
  - **Metrics**: Track message latency, tool success rate, error types
- **Debugging Tools**:
  - MCP Inspector for manual tool testing
  - ChatKit event handlers for frontend debugging
  - Agent execution traces for NL understanding issues

### Summary
**Overall Constitution Status**: ✅ **PASS** - No violations. All principles adhered to.

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file - implementation plan
├── research.md          # Technology decisions and patterns
├── data-model.md        # MCP tools and conversation entities
├── quickstart.md        # How to run Phase 3 locally
├── contracts/           # MCP tool specifications
│   └── mcp-tools.yaml   # OpenAPI-style spec for 5 tools
└── checklists/
    └── requirements.md  # Spec validation (complete)
```

### Source Code (repository root)

This project uses **Option 2: Web application** structure (extending Phase 2):

```text
apps/
├── backend/                   # Phase 2 (existing)
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── models/           # SQLModel entities (Task, User)
│   │   ├── routers/          # REST API endpoints
│   │   ├── auth/             # Better Auth integration
│   │   └── database.py       # Database session management
│   ├── mcp_server/           # Phase 3 (NEW)
│   │   ├── __init__.py
│   │   ├── server.py         # MCP server initialization (FastMCP)
│   │   ├── tools/            # MCP tool implementations
│   │   │   ├── __init__.py
│   │   │   ├── add_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── complete_task.py
│   │   │   ├── delete_task.py
│   │   │   └── update_task.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── errors.py     # Error handling utilities
│   │   │   └── auth.py       # JWT validation (reuse from app/auth/)
│   │   └── config.py         # MCP-specific configuration
│   ├── tests/
│   │   ├── mcp/              # Phase 3 MCP tests
│   │   │   ├── test_add_task.py
│   │   │   ├── test_list_tasks.py
│   │   │   ├── test_complete_task.py
│   │   │   ├── test_delete_task.py
│   │   │   └── test_update_task.py
│   │   ├── integration/
│   │   └── e2e/
│   ├── requirements.txt      # Add: mcp, openai
│   └── .env                  # Add: OPENAI_API_KEY, MCP_SERVER_PORT
│
└── frontend/                  # Phase 2 (existing)
    ├── src/
    │   ├── app/
    │   │   ├── (auth)/       # Login/register pages (Phase 2)
    │   │   ├── dashboard/    # Task dashboard (Phase 2)
    │   │   ├── chat/         # Phase 3 (NEW) - AI chatbot page
    │   │   │   └── page.tsx
    │   │   └── api/
    │   │       └── chatkit/  # Phase 3 (NEW)
    │   │           ├── session/
    │   │           │   └── route.ts   # ChatKit session creation
    │   │           └── refresh/
    │   │               └── route.ts   # ChatKit token refresh
    │   ├── components/
    │   │   ├── tasks/        # Phase 2 task components
    │   │   └── chat/         # Phase 3 (NEW)
    │   │       ├── TodoChatbot.tsx
    │   │       └── __tests__/
    │   │           └── TodoChatbot.test.tsx
    │   ├── lib/
    │   │   ├── api-client.ts        # Phase 2 REST client
    │   │   └── chatkit-config.ts    # Phase 3 (NEW)
    │   └── actions/          # Server Actions (Phase 2)
    ├── package.json          # Add: @openai/chatkit-react
    └── .env.local            # Add: OPENAI_API_KEY

# Phase 3 also adds conversation history storage (managed by Agents SDK)
# Location: apps/backend/conversation_history.db (SQLite, gitignored)
```

**Structure Decision**:
- **Extended Web Application**: Phase 3 adds MCP server to existing backend and ChatKit integration to existing frontend
- **Rationale**: Minimal structural changes; MCP server is a sibling to FastAPI app, shares database/auth utilities
- **New Directories**: `apps/backend/mcp_server/` and `apps/frontend/src/app/chat/`
- **Shared Code**: MCP tools reuse `app/models/`, `app/auth/`, and `app/database.py` from Phase 2

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations to justify.** All complexity additions are minimal and justified:

- **OpenAI Agents SDK**: Necessary for natural language understanding (no simpler alternative for robust NLP)
- **MCP Server**: Required architecture for tool-based AI agents (industry standard protocol)
- **ChatKit Component**: Pre-built UI reduces complexity vs. custom chat interface
- **SQLite for Conversations**: Simpler than adding PostgreSQL tables; conversations are transient/session-specific

---

## Phase 0: Research & Technical Decisions

### Research Tasks

1. **MCP SDK Python Integration**
   - **Question**: How to create MCP server with HTTP/SSE transport for web-based agents?
   - **Decision Needed**: Server initialization pattern, tool registration, lifecycle management

2. **OpenAI Agents SDK Setup**
   - **Question**: How to connect Agents SDK to MCP server and manage sessions?
   - **Decision Needed**: Agent configuration, session management (SQLite vs. OpenAI Conversations API)

3. **ChatKit React Integration**
   - **Question**: How to integrate ChatKit with Next.js 16 App Router and Better Auth?
   - **Decision Needed**: Session API routes, token passing, custom theme configuration

4. **JWT Token Flow**
   - **Question**: How to pass Better Auth JWT from ChatKit → OpenAI Agent → MCP Tools?
   - **Decision Needed**: Token injection point, validation in MCP tools

5. **Tool Invocation Patterns**
   - **Question**: How does OpenAI Agent decide which tool to call based on natural language?
   - **Decision Needed**: Tool descriptions (docstrings), parameter extraction, error handling

### Research Output

See [research.md](./research.md) for detailed findings and decisions.

---

## Phase 1: Data Models & API Contracts

### Entities

#### Existing Entities (Phase 2 - Reused)

**Task** (from `app/models/task.py`):
- `id`: Integer (primary key)
- `title`: String (max 200 chars)
- `description`: String (optional, max 1000 chars)
- `completed`: Boolean (default False)
- `user_id`: Integer (foreign key to User)
- `created_at`: DateTime
- `updated_at`: DateTime

**User** (from `app/models/user.py`):
- `id`: Integer (primary key)
- `email`: String (unique)
- `hashed_password`: String
- `created_at`: DateTime

#### New Entities (Phase 3)

**Conversation** (SQLite - managed by OpenAI Agents SDK):
- `id`: String (conversation ID from Agents SDK)
- `user_id`: String (links to Better Auth user)
- `created_at`: DateTime
- `last_active_at`: DateTime

**Message** (SQLite - managed by OpenAI Agents SDK):
- `id`: Integer (auto-increment)
- `conversation_id`: String (foreign key)
- `role`: Enum (`user` | `assistant`)
- `content`: Text
- `tool_calls`: JSON (optional - records which MCP tools were called)
- `created_at`: DateTime

**Note**: Conversation/Message entities are automatically managed by Agents SDK's SQLiteSession. We don't create these tables manually.

**MCP Tool Call** (Conceptual - not persisted):
- `tool_name`: String (`add_task`, `list_tasks`, etc.)
- `parameters`: JSON (tool-specific parameters)
- `jwt_token`: String (user authentication)
- `result`: JSON (tool execution result)

### API Contracts

See [contracts/mcp-tools.yaml](./contracts/mcp-tools.yaml) for complete OpenAPI specification.

**MCP Tools Summary**:

1. **add_task**
   - **Input**: `jwt_token` (string), `title` (string), `description` (string, optional)
   - **Output**: JSON `{"success": true, "task": {...}}` or `{"error": "message"}`

2. **list_tasks**
   - **Input**: `jwt_token` (string), `filter` (string: "all" | "completed" | "pending")
   - **Output**: JSON `{"tasks": [...], "count": N}` or `{"error": "message"}`

3. **complete_task**
   - **Input**: `jwt_token` (string), `task_id` (integer)
   - **Output**: JSON `{"success": true, "task": {...}}` or `{"error": "message"}`

4. **delete_task**
   - **Input**: `jwt_token` (string), `task_id` (integer)
   - **Output**: JSON `{"success": true, "message": "..."}` or `{"error": "message"}`

5. **update_task**
   - **Input**: `jwt_token` (string), `task_id` (integer), `title` (string, optional), `description` (string, optional), `completed` (boolean, optional)
   - **Output**: JSON `{"success": true, "task": {...}}` or `{"error": "message"}`

**ChatKit API Routes** (Next.js App Router):

1. **POST /api/chatkit/session**
   - **Purpose**: Create new ChatKit session
   - **Authentication**: Requires Better Auth session
   - **Response**: `{"client_secret": "..."}`

2. **POST /api/chatkit/refresh**
   - **Purpose**: Refresh expired ChatKit session token
   - **Input**: `{"token": "existing_token"}`
   - **Response**: `{"client_secret": "..."}`

---

## Phase 2: Component Breakdown

**Note**: This section outlines components for reference. Tasks are generated in separate `/sp.tasks` command.

### Backend Components

1. **MCP Server Initialization** (`mcp_server/server.py`)
   - Initialize FastMCP with lifespan management
   - Set up database engine connection
   - Register 5 tools
   - Start HTTP/SSE transport on port 8001

2. **MCP Tool: add_task** (`mcp_server/tools/add_task.py`)
   - Validate JWT token
   - Extract user_id
   - Create Task in database
   - Return JSON result

3. **MCP Tool: list_tasks** (`mcp_server/tools/list_tasks.py`)
   - Validate JWT token
   - Query tasks filtered by user_id
   - Apply filter (all/completed/pending)
   - Return JSON task list

4. **MCP Tool: complete_task** (`mcp_server/tools/complete_task.py`)
   - Validate JWT token
   - Find task by ID
   - Verify ownership
   - Update completed=True
   - Return JSON result

5. **MCP Tool: delete_task** (`mcp_server/tools/delete_task.py`)
   - Validate JWT token
   - Find task by ID
   - Verify ownership
   - Delete task
   - Return JSON confirmation

6. **MCP Tool: update_task** (`mcp_server/tools/update_task.py`)
   - Validate JWT token
   - Find task by ID
   - Verify ownership
   - Update provided fields
   - Return JSON result

7. **Error Handling Utilities** (`mcp_server/utils/errors.py`)
   - Standard error response format
   - Error code enum
   - Logging integration

8. **Authentication Utilities** (`mcp_server/utils/auth.py`)
   - JWT validation (reuse from `app/auth/`)
   - User extraction from token
   - Error handling for invalid tokens

### Frontend Components

1. **Chat Page** (`app/chat/page.tsx`)
   - Server Component for authentication check
   - Redirect unauthenticated users
   - Render TodoChatbot component

2. **TodoChatbot Component** (`components/chat/TodoChatbot.tsx`)
   - Client Component (`'use client'`)
   - Use useChatKit hook
   - Configure ChatKit with custom theme
   - Handle session creation/refresh

3. **ChatKit Configuration** (`lib/chatkit-config.ts`)
   - Theme customization
   - Composer placeholder
   - Start screen prompts
   - Header actions

4. **ChatKit Session API Route** (`app/api/chatkit/session/route.ts`)
   - Validate Better Auth session
   - Call OpenAI API to create ChatKit session
   - Pass user JWT token in metadata
   - Return client_secret

5. **ChatKit Refresh API Route** (`app/api/chatkit/refresh/route.ts`)
   - Validate existing token
   - Call OpenAI API to refresh session
   - Return new client_secret

### Integration Components

1. **OpenAI Agent Configuration** (Server-side, not in repo)
   - Initialize Agent with MCP server connection
   - Set instructions for todo management
   - Configure model (GPT-4o mini)
   - Set up session management (SQLiteSession)

2. **MCP-Agent Connection**
   - Agent connects to `http://localhost:8001/mcp` (MCP server endpoint)
   - Discovers 5 tools via MCP protocol
   - Calls tools based on user natural language input

---

## Architecture Diagrams

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       User Browser                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Next.js Frontend (Port 3000)                         │ │
│  │  ┌──────────────────┐  ┌──────────────────┐          │ │
│  │  │  Chat Page       │  │  Dashboard Page  │          │ │
│  │  │  /chat           │  │  /dashboard      │          │ │
│  │  │                  │  │  (Phase 2)       │          │ │
│  │  │ ┌──────────────┐ │  │                  │          │ │
│  │  │ │ TodoChatbot  │ │  │                  │          │ │
│  │  │ │ (ChatKit UI) │ │  │                  │          │ │
│  │  │ └──────────────┘ │  │                  │          │ │
│  │  └──────────────────┘  └──────────────────┘          │ │
│  └───────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ HTTP/WebSocket
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              OpenAI Infrastructure                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  OpenAI Agent (GPT-4o mini)                           │  │
│  │  - Understands natural language                       │  │
│  │  - Decides which MCP tool to call                     │  │
│  │  - Manages conversation context                       │  │
│  └───────────────┬───────────────────────────────────────┘  │
└──────────────────┼──────────────────────────────────────────┘
                   │
                   │ MCP Protocol (HTTP/SSE)
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend Server (Port 8000, 8001)               │
│  ┌─────────────────────────┐  ┌──────────────────────────┐ │
│  │  FastAPI (Port 8000)    │  │  MCP Server (Port 8001)  │ │
│  │  (Phase 2)              │  │  (Phase 3)               │ │
│  │  - REST API             │  │  - 5 MCP Tools:          │ │
│  │  - Better Auth          │  │    • add_task            │ │
│  │  - CRUD endpoints       │  │    • list_tasks          │ │
│  │                         │  │    • complete_task       │ │
│  │                         │  │    • delete_task         │ │
│  │                         │  │    • update_task         │ │
│  └───────┬─────────────────┘  └────────┬─────────────────┘ │
│          │                              │                   │
│          │  Shared: app/auth/, app/models/, app/database.py │
│          │                              │                   │
│          └──────────────┬───────────────┘                   │
└─────────────────────────┼──────────────────────────────────────┘
                          │
                          │ SQLModel
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Database Layer                                 │
│  ┌──────────────────────┐  ┌───────────────────────────┐   │
│  │  PostgreSQL (Neon)   │  │  SQLite (conversation     │   │
│  │  - Users             │  │  history)                 │   │
│  │  - Tasks             │  │  - Conversations          │   │
│  │  (Phase 2 schema)    │  │  - Messages               │   │
│  │                      │  │  (Managed by Agents SDK)  │   │
│  └──────────────────────┘  └───────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Message Flow: User Creates Task via Natural Language

```
User                ChatKit              Agent               MCP Server          Database
 │                    │                    │                     │                  │
 │ "Add buy milk"     │                    │                     │                  │
 ├────────────────────>                    │                     │                  │
 │                    │  Send message      │                     │                  │
 │                    ├────────────────────>                     │                  │
 │                    │                    │ Understand intent   │                  │
 │                    │                    │ → calls add_task    │                  │
 │                    │                    ├─────────────────────>                  │
 │                    │                    │                     │ Validate JWT     │
 │                    │                    │                     ├──────────────────>
 │                    │                    │                     │ Extract user_id  │
 │                    │                    │                     │<─────────────────┤
 │                    │                    │                     │ Create Task      │
 │                    │                    │                     │ (user_id, "Buy   │
 │                    │                    │                     │  milk")          │
 │                    │                    │                     ├──────────────────>
 │                    │                    │                     │ Task created     │
 │                    │                    │                     │<─────────────────┤
 │                    │                    │ Tool result:        │                  │
 │                    │                    │ {"success": true,   │                  │
 │                    │                    │  "task": {...}}     │                  │
 │                    │                    │<────────────────────┤                  │
 │                    │  "I've added 'Buy  │                     │                  │
 │                    │   milk' to your    │                     │                  │
 │                    │   todo list!"      │                     │                  │
 │                    │<───────────────────┤                     │                  │
 │ See confirmation   │                    │                     │                  │
 │<───────────────────┤                    │                     │                  │
 │                    │                    │                     │                  │
```

---

## Testing Strategy

### Unit Tests

**MCP Tools** (`apps/backend/tests/mcp/`):
- Test each tool in isolation with mocked database
- Verify JWT validation logic
- Test error handling (invalid token, task not found, etc.)
- Test user isolation (user can't access other users' tasks)

**Example Test**:
```python
# tests/mcp/test_add_task.py
async def test_add_task_creates_task_for_authenticated_user():
    # Given: Valid JWT token
    token = create_test_jwt(user_id=1)

    # When: Call add_task tool
    result = await add_task(jwt_token=token, title="Test task")

    # Then: Task created for user 1
    assert result["success"] == True
    assert result["task"]["title"] == "Test task"
    assert result["task"]["user_id"] == 1
```

### Integration Tests

**Agent-MCP Integration** (`apps/backend/tests/integration/`):
- Start local MCP server
- Create test agent
- Send natural language messages
- Verify correct tools are called
- Verify database state changes

**Example Test**:
```python
async def test_natural_language_task_creation():
    # Given: Running MCP server and connected agent
    agent = create_test_agent()

    # When: User sends natural language message
    result = await agent.send_message(
        "Add a task to buy groceries",
        user_jwt=test_token
    )

    # Then: Task created in database
    tasks = get_user_tasks(user_id=1)
    assert any("groceries" in task.title.lower() for task in tasks)
```

### End-to-End Tests

**ChatKit UI Flow** (`apps/frontend/src/components/chat/__tests__/`):
- Render TodoChatbot component
- Mock ChatKit API responses
- Simulate user typing and sending message
- Verify UI updates with assistant response

**Manual Testing Checklist**:
- [ ] User can log in and access /chat page
- [ ] ChatKit interface loads correctly
- [ ] User can create task via "Add task to X"
- [ ] User can list tasks via "Show my tasks"
- [ ] User can complete task via "Mark task Y as done"
- [ ] User can delete task via "Delete task Z"
- [ ] User can update task via "Change task A to B"
- [ ] Conversation history persists within session
- [ ] Error messages are user-friendly
- [ ] Multiple users can chat simultaneously without interference

---

## Deployment Strategy

### Local Development

**Terminal 1: FastAPI (Phase 2)**
```bash
cd apps/backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2: MCP Server (Phase 3)**
```bash
cd apps/backend
python -m mcp_server.server --port 8001
```

**Terminal 3: Frontend (Phase 2 + 3)**
```bash
cd apps/frontend
npm run dev  # Port 3000
```

**Environment Variables**:
```bash
# apps/backend/.env
DATABASE_URL=postgresql://user:pass@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-secret
OPENAI_API_KEY=sk-...
MCP_SERVER_PORT=8001

# apps/frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
OPENAI_API_KEY=sk-...  # For ChatKit session creation
```

### Production Deployment

**Backend**:
- Run FastAPI and MCP server as separate processes (systemd/supervisor)
- Use process manager (PM2, systemd) for auto-restart
- Both behind reverse proxy (nginx) if needed

**Frontend**:
- Standard Vercel/Next.js deployment
- Environment variables configured in Vercel dashboard

**Database**:
- PostgreSQL: Neon Serverless (existing Phase 2)
- SQLite: Local file for conversation history (ephemeral OK for Phase 3)

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| OpenAI API rate limits hit during high usage | Users can't chat | Medium | Implement exponential backoff retry logic; fallback to error message |
| OpenAI API cost exceeds budget | Financial impact | Medium | Set monthly budget cap; monitor usage dashboard; use GPT-3.5 for non-critical |
| Agent misinterprets natural language | Wrong task created/deleted | High (initial) | Clear tool docstrings; extensive testing; allow undo operations |
| JWT token not passed correctly to MCP tools | Authentication failure | Low | Integration tests verify token flow; log token presence (not value) |
| Conversation history grows unbounded | Storage/performance issues | Low | Limit to 1000 messages per session; archive old conversations |
| MCP server crashes during high load | Chat unavailable | Low | Proper error handling; health checks; auto-restart on crash |
| ChatKit frontend breaks with Next.js updates | UI non-functional | Low | Pin ChatKit version; test before upgrading Next.js |

---

## Success Metrics

**Phase 3 will be considered successful when**:

1. ✅ All 5 MCP tools pass unit tests (100% coverage on tool logic)
2. ✅ Agent correctly interprets 90%+ of common task phrases in manual testing
3. ✅ End-to-end flow works: User logs in → opens chat → creates task → sees in dashboard
4. ✅ Response time < 3 seconds for simple operations (add/list tasks)
5. ✅ User isolation verified: No cross-user data leaks in testing
6. ✅ ChatKit UI renders and is usable on desktop and mobile browsers
7. ✅ Conversation history persists throughout session
8. ✅ Error handling graceful: Network failures show friendly messages, not crashes

---

## Completed Steps

1. ✅ **Research Validated** - Technology choices documented in [research.md](./research.md)
2. ✅ **Data Model Confirmed** - Entities defined in [data-model.md](./data-model.md)
3. ✅ **Contracts Validated** - MCP tool specs in [contracts/mcp-tools.yaml](./contracts/mcp-tools.yaml)
4. ✅ **Tasks Generated** - Actionable breakdown in [tasks.md](./tasks.md) (60 tasks across 10 phases)
5. ✅ **Analysis Complete** - Cross-artifact validation in [analysis.md](./analysis.md)

## Next Steps

**Ready for Implementation**:
- Run `/sp.implement` to begin executing tasks from [tasks.md](./tasks.md)
- Follow Red-Green-Refactor TDD cycle per task
- Start with MVP scope: 37 tasks (Phases 1-5 + Phase 8)

---

**Plan Status**: ✅ Approved and validated
**Next Command**: `/sp.implement` to start Phase 3 implementation
