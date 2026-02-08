# Data Model: AI-Powered Todo Chatbot (Phase 3)

**Feature Branch**: `003-ai-chatbot`
**Date**: 2026-02-04
**Status**: Complete

## Overview

Phase 3 reuses the existing Phase 2 data model (User, Task) and adds conceptual entities for chat functionality. Conversation/Message entities are managed automatically by OpenAI Agents SDK's SQLiteSession.

## Entity Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     PostgreSQL (Phase 2)                        │
│  ┌─────────────────┐         ┌─────────────────┐               │
│  │      User       │         │      Task       │               │
│  ├─────────────────┤         ├─────────────────┤               │
│  │ id: Integer PK  │◄────────┤ id: Integer PK  │               │
│  │ email: String   │    1:N  │ title: String   │               │
│  │ hashed_password │         │ description: Str│               │
│  │ created_at: DT  │         │ completed: Bool │               │
│  └─────────────────┘         │ user_id: FK     │               │
│                              │ created_at: DT  │               │
│                              │ updated_at: DT  │               │
│                              └─────────────────┘               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                SQLite (Agents SDK Managed)                      │
│  ┌─────────────────┐         ┌─────────────────┐               │
│  │  Conversation   │         │    Message      │               │
│  ├─────────────────┤         ├─────────────────┤               │
│  │ id: String PK   │◄────────┤ id: Integer PK  │               │
│  │ user_id: String │    1:N  │ conversation_id │               │
│  │ created_at: DT  │         │ role: Enum      │               │
│  │ last_active: DT │         │ content: Text   │               │
│  └─────────────────┘         │ tool_calls: JSON│               │
│                              │ created_at: DT  │               │
│                              └─────────────────┘               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   Conceptual (Not Persisted)                    │
│  ┌─────────────────┐         ┌─────────────────┐               │
│  │   MCP Tool      │         │  Tool Result    │               │
│  ├─────────────────┤         ├─────────────────┤               │
│  │ name: String    │────────►│ success: Bool   │               │
│  │ parameters: JSON│  1:1    │ data: JSON      │               │
│  │ jwt_token: Str  │         │ error: String?  │               │
│  └─────────────────┘         └─────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Existing Entities (Phase 2 - Reused)

### User

**Source**: `apps/backend/app/models/user.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto-increment | Unique user identifier |
| email | String(255) | Unique, Not Null, Index | User's email address |
| hashed_password | String(255) | Not Null | Bcrypt hashed password |
| created_at | DateTime | Not Null, Default=now() | Account creation timestamp |

**Relationships**:
- One User → Many Tasks

**Phase 3 Usage**:
- JWT token contains user.id
- MCP tools extract user_id from validated JWT
- User isolation: all task queries filter by user_id

---

### Task

**Source**: `apps/backend/app/models/task.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto-increment | Unique task identifier |
| title | String(200) | Not Null | Task title (max 200 chars) |
| description | String(1000) | Nullable | Optional task description |
| completed | Boolean | Not Null, Default=False | Completion status |
| user_id | Integer | FK(User.id), Not Null, Index | Owner reference |
| created_at | DateTime | Not Null, Default=now() | Creation timestamp |
| updated_at | DateTime | Not Null, Default=now(), OnUpdate=now() | Last update timestamp |

**Relationships**:
- Many Tasks → One User (via user_id)

**Validation Rules**:
- title: Required, 1-200 characters
- description: Optional, max 1000 characters
- completed: Boolean only
- user_id: Must reference valid User

**Phase 3 Usage**:
- All 5 MCP tools operate on Task entity
- add_task creates new Task
- list_tasks queries Tasks with filter
- complete_task sets completed=True
- delete_task removes Task
- update_task modifies title/description/completed

---

## New Entities (Phase 3)

### Conversation (SQLite - Agents SDK Managed)

**Note**: This table is automatically created and managed by OpenAI Agents SDK's SQLiteSession. We do NOT create migrations for it.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String | PK | Session/conversation ID from Agents SDK |
| user_id | String | Not Null, Index | Better Auth user identifier |
| created_at | DateTime | Not Null | When conversation started |
| last_active_at | DateTime | Not Null | Last message timestamp |

**Purpose**:
- Groups messages into a single chat session
- Links to user for multi-user support
- Tracks session activity

**Location**: `apps/backend/conversation_history.db` (gitignored)

---

### Message (SQLite - Agents SDK Managed)

**Note**: This table is automatically created and managed by OpenAI Agents SDK's SQLiteSession.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto-increment | Unique message ID |
| conversation_id | String | FK(Conversation.id), Index | Parent conversation |
| role | Enum | Not Null | "user" or "assistant" |
| content | Text | Not Null | Message text content |
| tool_calls | JSON | Nullable | Record of MCP tools called |
| created_at | DateTime | Not Null | Message timestamp |

**Purpose**:
- Stores individual messages in conversation
- Records which tools were called by assistant
- Enables conversation context for multi-turn interactions

**tool_calls Format**:
```json
[
  {
    "tool": "add_task",
    "parameters": {"title": "Buy milk"},
    "result": {"success": true, "task": {...}}
  }
]
```

---

## Conceptual Entities (Not Persisted)

### MCP Tool Call

Represents a single invocation of an MCP tool by the AI agent.

| Field | Type | Description |
|-------|------|-------------|
| tool_name | String | One of: add_task, list_tasks, complete_task, delete_task, update_task |
| jwt_token | String | Better Auth JWT for user authentication |
| parameters | JSON | Tool-specific parameters |
| result | JSON | Tool execution result |

**Tool Parameters by Type**:

| Tool | Required Params | Optional Params |
|------|-----------------|-----------------|
| add_task | jwt_token, title | description |
| list_tasks | jwt_token | filter ("all"\|"completed"\|"pending") |
| complete_task | jwt_token, task_id | - |
| delete_task | jwt_token, task_id | - |
| update_task | jwt_token, task_id | title, description, completed |

---

### Tool Result

Standard response format from all MCP tools.

**Success Response**:
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy milk",
    "description": null,
    "completed": false,
    "user_id": 1,
    "created_at": "2026-02-04T10:00:00Z"
  }
}
```

**List Response**:
```json
{
  "tasks": [
    {"id": 1, "title": "Task 1", "completed": false},
    {"id": 2, "title": "Task 2", "completed": true}
  ],
  "count": 2,
  "filter": "all"
}
```

**Error Response**:
```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or expired token"
  }
}
```

**Error Codes**:
| Code | HTTP Equivalent | Description |
|------|-----------------|-------------|
| unauthorized | 401 | Invalid/expired JWT token |
| not_found | 404 | Task with given ID doesn't exist |
| forbidden | 403 | User doesn't own the task |
| validation_error | 400 | Invalid parameters |
| server_error | 500 | Unexpected server error |

---

## State Transitions

### Task.completed State Machine

```
┌─────────────┐
│   created   │
│ completed=  │
│   false     │
└──────┬──────┘
       │
       │ complete_task()
       ▼
┌─────────────┐
│  completed  │
│ completed=  │◄─────────────┐
│   true      │              │
└──────┬──────┘              │
       │                     │
       │ update_task         │
       │ (completed=false)   │
       ▼                     │
┌─────────────┐              │
│ uncompleted │──────────────┘
│ completed=  │  update_task
│   false     │  (completed=true)
└─────────────┘
```

---

## Database Queries

### Frequently Used Queries

**1. Get user's tasks (all)**:
```sql
SELECT * FROM task WHERE user_id = :user_id ORDER BY created_at DESC;
```

**2. Get user's pending tasks**:
```sql
SELECT * FROM task WHERE user_id = :user_id AND completed = false ORDER BY created_at DESC;
```

**3. Get user's completed tasks**:
```sql
SELECT * FROM task WHERE user_id = :user_id AND completed = true ORDER BY created_at DESC;
```

**4. Get single task (with ownership check)**:
```sql
SELECT * FROM task WHERE id = :task_id AND user_id = :user_id;
```

**5. Create task**:
```sql
INSERT INTO task (title, description, completed, user_id, created_at, updated_at)
VALUES (:title, :description, false, :user_id, NOW(), NOW())
RETURNING *;
```

**6. Update task**:
```sql
UPDATE task SET title = COALESCE(:title, title),
                description = COALESCE(:description, description),
                completed = COALESCE(:completed, completed),
                updated_at = NOW()
WHERE id = :task_id AND user_id = :user_id
RETURNING *;
```

**7. Delete task**:
```sql
DELETE FROM task WHERE id = :task_id AND user_id = :user_id;
```

---

## Indexes

### Existing Indexes (Phase 2)

| Table | Index Name | Columns | Purpose |
|-------|------------|---------|---------|
| user | user_email_idx | email | Fast login lookup |
| task | task_user_id_idx | user_id | Fast user task queries |

### Recommended Indexes (Phase 3)

| Table | Index Name | Columns | Purpose |
|-------|------------|---------|---------|
| task | task_user_completed_idx | (user_id, completed) | Fast filtered queries |

**SQLAlchemy Index Definition**:
```python
from sqlalchemy import Index

# Add to Task model
Index('task_user_completed_idx', Task.user_id, Task.completed)
```

**Note**: This index is optional for Phase 3 MVP. Add if list_tasks performance becomes an issue.

---

## Data Integrity Rules

### Phase 2 (Existing)

1. **User email uniqueness**: Each email can only exist once
2. **Task ownership**: task.user_id must reference valid user.id
3. **Cascade delete**: When user deleted, all tasks deleted (not implemented in Phase 2)

### Phase 3 (Additional)

1. **JWT validation**: All MCP tools must validate JWT before any operation
2. **Ownership verification**: Update/delete operations must verify user owns the task
3. **No cross-user access**: Queries always filter by user_id from JWT

---

## Migration Notes

### No New Migrations Required

Phase 3 does **NOT** require database migrations because:
- Task and User tables already exist (Phase 2)
- Conversation/Message tables are managed by Agents SDK in separate SQLite file
- MCP tools use existing schema

### SQLite Setup (Automatic)

The SQLiteSession from Agents SDK creates its schema automatically on first use:
```python
from agents import SQLiteSession

# This creates/connects to conversation_history.db automatically
session = SQLiteSession(user_id)
```

**File Location**: `apps/backend/conversation_history.db`

**gitignore Entry**:
```gitignore
# Conversation history (Agents SDK)
apps/backend/*.db
apps/backend/conversation_history.db
```

---

## Data Volume Estimates

| Entity | Expected Count | Growth Rate |
|--------|----------------|-------------|
| Users | ~100-1000 (from Phase 2) | Stable |
| Tasks | ~10-50 per user | Moderate |
| Conversations | ~1-5 per user/day | Moderate |
| Messages | ~20-100 per conversation | High |

**Storage Estimates**:
- PostgreSQL (Tasks): ~1KB per task × 50 tasks × 1000 users = ~50MB
- SQLite (Messages): ~500 bytes per message × 100 messages × 5 convos × 1000 users = ~250MB

**Cleanup Strategy**:
- Archive conversations older than 30 days
- Limit to 1000 messages per conversation
- Consider purging completed task history after 1 year

---

**Data Model Status**: ✅ Complete
**Next Step**: Create API contracts (mcp-tools.yaml)
