# Tasks: AI-Powered Todo Chatbot (Phase 3)

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Tests are included as per constitution (TDD commitment in plan.md).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend (Python)**: `apps/backend/`
- **Frontend (Next.js)**: `apps/frontend/src/`
- **MCP Server**: `apps/backend/mcp_server/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and basic structure for Phase 3

- [X] T001 Add MCP SDK and OpenAI dependencies to apps/backend/requirements.txt
- [X] T002 Add @openai/chatkit-react to apps/frontend/package.json
- [X] T003 [P] Create MCP server directory structure at apps/backend/mcp_server/
- [X] T004 [P] Add Phase 3 environment variables to apps/backend/.env.example (OPENAI_API_KEY, MCP_SERVER_PORT)
- [X] T005 [P] Add Phase 3 environment variables to apps/frontend/.env.local.example (OPENAI_API_KEY)
- [X] T006 Update apps/backend/.gitignore to exclude conversation_history.db (SQLite)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core MCP infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### MCP Server Core

- [X] T007 Create MCP server configuration at apps/backend/mcp_server/config.py
- [X] T008 Create error handling utilities at apps/backend/mcp_server/utils/errors.py
- [X] T009 Create auth utilities (JWT validation wrapper) at apps/backend/mcp_server/utils/auth.py
- [X] T010 Create MCP server initialization with lifespan at apps/backend/mcp_server/server.py
- [X] T011 Create MCP server __init__.py with exports at apps/backend/mcp_server/__init__.py
- [X] T012 [P] Create tools __init__.py at apps/backend/mcp_server/tools/__init__.py
- [X] T013 [P] Create utils __init__.py at apps/backend/mcp_server/utils/__init__.py

### ChatKit API Routes (Frontend)

- [X] T014 [P] Create ChatKit session API route at apps/frontend/src/app/api/chatkit/session/route.ts
- [X] T015 [P] Create ChatKit refresh API route at apps/frontend/src/app/api/chatkit/refresh/route.ts
- [X] T016 Create ChatKit configuration at apps/frontend/src/lib/chatkit-config.ts

### Test Infrastructure

- [X] T017 [P] Create MCP test directory at apps/backend/tests/mcp/__init__.py
- [X] T018 [P] Create test fixtures for MCP tools at apps/backend/tests/mcp/conftest.py

**Checkpoint**: Foundation ready - MCP server can start, ChatKit routes exist, user story implementation can begin

---

## Phase 3: User Story 1 - Natural Language Todo Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create todo tasks through natural language conversation

**Independent Test**: Send "Add buy groceries to my list" and verify task is created in database

### Tests for User Story 1

- [X] T019 [P] [US1] Create test for add_task tool at apps/backend/tests/mcp/test_add_task.py
- [X] T020 [P] [US1] Create test for authentication in add_task at apps/backend/tests/mcp/test_add_task.py

### Implementation for User Story 1

- [X] T021 [US1] Implement add_task MCP tool at apps/backend/mcp_server/tools/add_task.py
- [X] T022 [US1] Register add_task tool in apps/backend/mcp_server/server.py
- [X] T023 [US1] Verify add_task works with MCP Inspector (manual test)

**Checkpoint**: User can create tasks via MCP tool - core add functionality working

---

## Phase 4: User Story 2 - View and Query Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can view and query their task list using natural language

**Independent Test**: Ask "Show me all my tasks" and verify correct list is returned

### Tests for User Story 2

- [X] T024 [P] [US2] Create test for list_tasks tool at apps/backend/tests/mcp/test_list_tasks.py
- [X] T025 [P] [US2] Create test for filter functionality (all/completed/pending) at apps/backend/tests/mcp/test_list_tasks.py

### Implementation for User Story 2

- [X] T026 [US2] Implement list_tasks MCP tool at apps/backend/mcp_server/tools/list_tasks.py
- [X] T027 [US2] Register list_tasks tool in apps/backend/mcp_server/server.py
- [X] T028 [US2] Verify list_tasks works with filters via MCP Inspector (manual test)

**Checkpoint**: User can create AND list tasks - core read functionality working

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P1) 🎯 MVP

**Goal**: Users can mark tasks as complete through natural language

**Independent Test**: Say "Mark task 1 as done" and verify task.completed changes to True

### Tests for User Story 3

- [X] T029 [P] [US3] Create test for complete_task tool at apps/backend/tests/mcp/test_complete_task.py
- [X] T030 [P] [US3] Create test for ownership verification in complete_task at apps/backend/tests/mcp/test_complete_task.py

### Implementation for User Story 3

- [X] T031 [US3] Implement complete_task MCP tool at apps/backend/mcp_server/tools/complete_task.py
- [X] T032 [US3] Register complete_task tool in apps/backend/mcp_server/server.py
- [X] T033 [US3] Verify complete_task works via MCP Inspector (manual test)

**Checkpoint**: User can create, list, and complete tasks - MVP CRUD (CRU) working

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Users can delete tasks through natural language

**Independent Test**: Say "Delete task 3" and verify task is removed from database

### Tests for User Story 4

- [ ] T034 [P] [US4] Create test for delete_task tool at apps/backend/tests/mcp/test_delete_task.py
- [ ] T035 [P] [US4] Create test for ownership verification in delete_task at apps/backend/tests/mcp/test_delete_task.py

### Implementation for User Story 4

- [ ] T036 [US4] Implement delete_task MCP tool at apps/backend/mcp_server/tools/delete_task.py
- [ ] T037 [US4] Register delete_task tool in apps/backend/mcp_server/server.py
- [ ] T038 [US4] Verify delete_task works via MCP Inspector (manual test)

**Checkpoint**: Full CRUD via MCP tools (add, list, complete, delete)

---

## Phase 7: User Story 5 - Update Task Details (Priority: P2)

**Goal**: Users can modify task titles and descriptions through natural language

**Independent Test**: Say "Change task 2 title to Call doctor" and verify update

### Tests for User Story 5

- [ ] T039 [P] [US5] Create test for update_task tool at apps/backend/tests/mcp/test_update_task.py
- [ ] T040 [P] [US5] Create test for partial updates (title only, description only) at apps/backend/tests/mcp/test_update_task.py

### Implementation for User Story 5

- [ ] T041 [US5] Implement update_task MCP tool at apps/backend/mcp_server/tools/update_task.py
- [ ] T042 [US5] Register update_task tool in apps/backend/mcp_server/server.py
- [ ] T043 [US5] Verify update_task works via MCP Inspector (manual test)

**Checkpoint**: All 5 MCP tools complete and tested

---

## Phase 8: ChatKit Frontend Integration

**Goal**: Create the chat UI that connects to the AI agent

**Independent Test**: Open /chat page, see ChatKit UI, send message

### Chat Page & Components

- [X] T044 [P] Create TodoChatbot component at apps/frontend/components/chat/TodoChatbot.tsx
- [X] T045 [P] Create chat page at apps/frontend/app/chat/page.tsx
- [X] T046 Create component test at apps/frontend/components/chat/__tests__/TodoChatbot.test.tsx
- [X] T047 Add navigation link to chat from dashboard at apps/frontend/app/dashboard/page.tsx

**Checkpoint**: Chat UI renders and connects to ChatKit

---

## Phase 9: User Story 6 - Persistent Conversation Context (Priority: P3)

**Goal**: Conversation history maintained within session

**Independent Test**: Create task, then say "mark that as complete" - verify context works

### Implementation for User Story 6

- [ ] T048 [US6] Configure SQLiteSession in OpenAI Agent setup documentation
- [ ] T049 [US6] Test conversation context with multi-turn interaction
- [ ] T050 [US6] Document session management in quickstart.md

**Checkpoint**: Multi-turn conversations work with context

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

### Documentation

- [ ] T051 [P] Create quickstart.md with local development instructions at specs/003-ai-chatbot/quickstart.md
- [ ] T052 [P] Update backend-subagent.md Phase 3 references at .claude/agents/backend-subagent.md
- [ ] T053 [P] Update frontend-subagent.md Phase 3 references at .claude/agents/frontend-subagent.md

### Integration & Validation

- [ ] T054 Run all MCP tool tests: cd apps/backend && pytest tests/mcp/
- [ ] T055 Manual end-to-end test: Login → Open chat → Create task → List → Complete → Delete
- [ ] T056 Verify user isolation: Test with two different users
- [ ] T057 Performance check: Verify response time < 3 seconds for simple operations

### Security Hardening

- [ ] T058 [P] Verify JWT validation in all 5 MCP tools
- [ ] T059 [P] Verify user isolation (user_id filter) in all 5 MCP tools
- [ ] T060 Audit error messages for information leakage

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ─────────────────────────────────────────────┐
                                                            │
Phase 2: Foundational ◄─────────────────────────────────────┘
     │
     │  BLOCKS ALL USER STORIES
     ▼
┌─────────────────────────────────────────────────────────────┐
│  User Stories can proceed in parallel after Foundational    │
│                                                             │
│  Phase 3: US1 (add_task)    ─┬─► Phase 8: ChatKit Frontend │
│  Phase 4: US2 (list_tasks)  ─┤                             │
│  Phase 5: US3 (complete)    ─┤                             │
│  Phase 6: US4 (delete)      ─┤                             │
│  Phase 7: US5 (update)      ─┘                             │
│                                                             │
│  Phase 9: US6 (context) - depends on Phase 8               │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
Phase 10: Polish (depends on all user stories)
```

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (add_task) | Foundational | Phase 2 complete |
| US2 (list_tasks) | Foundational | Phase 2 complete |
| US3 (complete_task) | Foundational | Phase 2 complete |
| US4 (delete_task) | Foundational | Phase 2 complete |
| US5 (update_task) | Foundational | Phase 2 complete |
| US6 (context) | ChatKit Frontend | Phase 8 complete |

**Note**: US1-US5 (MCP tools) can be implemented in parallel. US6 requires ChatKit to test.

### Within Each User Story

1. Tests FIRST → ensure they FAIL
2. Implement tool
3. Register in server.py
4. Manual verification
5. Story complete

### Parallel Opportunities

**Phase 1 (Setup):**
```bash
# Can run in parallel:
T003: Create MCP server directory
T004: Add backend env vars
T005: Add frontend env vars
```

**Phase 2 (Foundational):**
```bash
# Can run in parallel after T007-T010:
T012: Create tools __init__.py
T013: Create utils __init__.py
T014: Create ChatKit session route
T015: Create ChatKit refresh route
T017: Create MCP test directory
T018: Create test fixtures
```

**MCP Tools (Phases 3-7):**
```bash
# Can run in parallel (different files):
T019: Test add_task
T024: Test list_tasks
T029: Test complete_task
T034: Test delete_task
T039: Test update_task
```

**ChatKit Frontend (Phase 8):**
```bash
# Can run in parallel:
T044: TodoChatbot component
T045: Chat page
```

---

## Parallel Example: All MCP Tool Tests

```bash
# Launch all MCP tool tests together (they're in different files):
Task: "Create test for add_task tool at apps/backend/tests/mcp/test_add_task.py"
Task: "Create test for list_tasks tool at apps/backend/tests/mcp/test_list_tasks.py"
Task: "Create test for complete_task tool at apps/backend/tests/mcp/test_complete_task.py"
Task: "Create test for delete_task tool at apps/backend/tests/mcp/test_delete_task.py"
Task: "Create test for update_task tool at apps/backend/tests/mcp/test_update_task.py"
```

---

## Implementation Strategy

### MVP First (US1 + US2 + US3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: US1 (add_task)
4. Complete Phase 4: US2 (list_tasks)
5. Complete Phase 5: US3 (complete_task)
6. Complete Phase 8: ChatKit Frontend
7. **STOP and VALIDATE**: Test core CRUD independently
8. Deploy/demo if ready - MVP complete!

### Incremental Delivery

1. **Setup + Foundational** → Infrastructure ready
2. **+ US1 + US2 + US3 + ChatKit** → MVP! (create, list, complete via chat)
3. **+ US4 (delete)** → Full CRUD via chat
4. **+ US5 (update)** → Complete task management
5. **+ US6 (context)** → Enhanced conversational experience
6. **+ Polish** → Production-ready

### Parallel Team Strategy

With multiple developers:

1. **Together**: Setup + Foundational (Phase 1-2)
2. **Split after Foundational**:
   - Developer A: US1 (add_task) + US2 (list_tasks)
   - Developer B: US3 (complete) + US4 (delete) + US5 (update)
   - Developer C: ChatKit Frontend (Phase 8)
3. **Together**: Integration, US6, Polish

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T006 (6) | Setup |
| Phase 2 | T007-T018 (12) | Foundational |
| Phase 3 | T019-T023 (5) | US1: add_task |
| Phase 4 | T024-T028 (5) | US2: list_tasks |
| Phase 5 | T029-T033 (5) | US3: complete_task |
| Phase 6 | T034-T038 (5) | US4: delete_task |
| Phase 7 | T039-T043 (5) | US5: update_task |
| Phase 8 | T044-T047 (4) | ChatKit Frontend |
| Phase 9 | T048-T050 (3) | US6: context |
| Phase 10 | T051-T060 (10) | Polish |
| **Total** | **60 tasks** | |

### Tasks Per User Story

| User Story | Priority | Tasks | MVP? |
|------------|----------|-------|------|
| US1: Natural Language Todo Creation | P1 | 5 | ✅ |
| US2: View and Query Tasks | P1 | 5 | ✅ |
| US3: Mark Tasks Complete | P1 | 5 | ✅ |
| US4: Delete Tasks | P2 | 5 | |
| US5: Update Task Details | P2 | 5 | |
| US6: Persistent Conversation Context | P3 | 3 | |

### Suggested MVP Scope

**MVP = Phase 1 + Phase 2 + Phase 3 + Phase 4 + Phase 5 + Phase 8**

Tasks: T001-T033, T044-T047 = **37 tasks**

Delivers: Create, list, and complete tasks via natural language chat interface.

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [US#] label maps task to specific user story for traceability
- Each MCP tool is independently testable via MCP Inspector
- ChatKit requires OPENAI_API_KEY to function
- Manual testing with MCP Inspector recommended before integration
- Commit after each task or logical group
- Run `pytest tests/mcp/` to validate all MCP tools
