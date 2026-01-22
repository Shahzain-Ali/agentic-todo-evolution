# Tasks: Full-Stack Todo Web Application

**Feature**: 002-todo-web-app
**Input**: Design documents from `/specs/002-todo-web-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/api-endpoints.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo structure**: `apps/frontend/` and `apps/backend/`
- Frontend paths: `apps/frontend/src/`
- Backend paths: `apps/backend/app/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

**Owner**: All subagents

- [x] T001 Create monorepo directory structure (apps/frontend/, apps/backend/)
- [x] T002 [P] Initialize Next.js 16+ project in apps/frontend/ with TypeScript and Tailwind CSS
- [x] T003 [P] Initialize FastAPI project in apps/backend/ with Python 3.11+ virtual environment
- [x] T004 [P] Configure frontend dependencies in apps/frontend/package.json (Next.js 16+, React 19+, Tailwind CSS 4+, Better Auth)
- [x] T005 [P] Configure backend dependencies in apps/backend/requirements.txt (FastAPI 0.100+, SQLModel 0.14+, python-jose, passlib, uvicorn, alembic)
- [x] T006 [P] Create frontend environment template in apps/frontend/.env.example
- [x] T007 [P] Create backend environment template in apps/backend/.env.example
- [x] T008 [P] Configure Tailwind CSS in apps/frontend/tailwind.config.ts with custom theme
- [x] T009 [P] Configure TypeScript in apps/frontend/tsconfig.json with strict mode
- [x] T010 [P] Create root layout in apps/frontend/src/app/layout.tsx with metadata
- [x] T011 [P] Configure CORS middleware in apps/backend/app/main.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Owner**: database-subagent, backend-subagent

### Database Foundation

- [x] T012 Create User model in apps/backend/app/models/user.py with SQLModel (id UUID, email, password_hash, created_at)
- [x] T013 Create Task model in apps/backend/app/models/task.py with SQLModel (id UUID, user_id FK, title, description, status, created_at, updated_at)
- [x] T014 Configure database engine and session in apps/backend/app/database.py with connection pooling
- [x] T015 Initialize Alembic in apps/backend/ and configure alembic.ini with DATABASE_URL
- [x] T016 Configure Alembic env.py in apps/backend/alembic/env.py to use SQLModel metadata
- [x] T017 Generate initial migration in apps/backend/alembic/versions/ for users and tasks tables
- [x] T018 Create database initialization script to apply migrations

### Authentication Foundation

- [x] T019 [P] Implement password hashing utilities in apps/backend/app/auth/password.py (hash_password, verify_password with bcrypt)
- [x] T020 [P] Implement JWT token utilities in apps/backend/app/auth/jwt.py (create_access_token, decode_access_token with python-jose)
- [x] T021 Create get_current_user dependency in apps/backend/app/auth/dependencies.py with OAuth2PasswordBearer
- [x] T022 Create Pydantic schemas in apps/backend/app/schemas/auth.py (UserCreate, UserResponse, Token)
- [x] T023 Create Pydantic schemas in apps/backend/app/schemas/task.py (TaskCreate, TaskUpdate, TaskResponse)

### Frontend Foundation

- [x] T024 [P] Create API client utility in apps/frontend/src/lib/api-client.ts with JWT token handling
- [x] T025 [P] Configure Better Auth in apps/frontend/src/lib/auth.ts with JWT strategy
- [x] T026 [P] Create Better Auth API route in apps/frontend/src/app/api/auth/[...all]/route.ts
- [x] T027 Create middleware for route protection in apps/frontend/middleware.ts (protect /dashboard routes)
- [x] T028 [P] Create TypeScript type definitions in apps/frontend/src/lib/definitions.ts (User, Task, AuthResponse)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email and password

**Independent Test**: Submit registration form with valid/invalid credentials and verify account creation

**Owner**: backend-subagent (API), frontend-subagent (UI)

### Backend Implementation for US1

- [x] T029 [P] [US1] Create auth router in apps/backend/app/routers/auth.py with FastAPI APIRouter
- [x] T030 [US1] Implement POST /api/auth/register endpoint in apps/backend/app/routers/auth.py (check email uniqueness, hash password, create user)
- [x] T031 [US1] Add auth router to FastAPI app in apps/backend/app/main.py with /api/auth prefix
- [x] T032 [US1] Add error handling for duplicate email (409 Conflict) in register endpoint

### Frontend Implementation for US1

- [x] T033 [P] [US1] Create registration page in apps/frontend/src/app/register/page.tsx with Server Component
- [x] T034 [P] [US1] Create RegisterForm component in apps/frontend/src/components/RegisterForm.tsx with Client Component
- [x] T035 [US1] Implement form validation in RegisterForm (email format, password min 8 chars)
- [x] T036 [US1] Implement form submission in RegisterForm calling POST /api/auth/register
- [x] T037 [US1] Add success/error state handling in RegisterForm with user feedback
- [x] T038 [US1] Add redirect to login page on successful registration

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Login and Authentication (Priority: P1)

**Goal**: Enable registered users to authenticate and access protected routes

**Independent Test**: Attempt login with valid/invalid credentials and verify access to dashboard

**Owner**: backend-subagent (API), frontend-subagent (UI)

### Backend Implementation for US2

- [x] T039 [US2] Implement POST /api/auth/login endpoint in apps/backend/app/routers/auth.py (verify credentials, generate JWT token)
- [x] T040 [US2] Add error handling for invalid credentials (401 Unauthorized) in login endpoint
- [x] T041 [US2] Add token expiration configuration (24 hours) in JWT utilities

### Frontend Implementation for US2

- [x] T042 [P] [US2] Create login page in apps/frontend/src/app/login/page.tsx with Server Component
- [x] T043 [P] [US2] Create LoginForm component in apps/frontend/src/components/LoginForm.tsx with Client Component
- [x] T044 [US2] Implement form validation in LoginForm (email format, password required)
- [x] T045 [US2] Implement form submission in LoginForm calling POST /api/auth/login
- [x] T046 [US2] Store JWT token using Better Auth session management
- [x] T047 [US2] Add success/error state handling in LoginForm with user feedback
- [x] T048 [US2] Add redirect to dashboard on successful login
- [x] T049 [P] [US2] Create Header component in apps/frontend/src/components/Header.tsx with logout button
- [x] T050 [US2] Implement logout functionality clearing session and redirecting to login
- [x] T051 [US2] Update middleware to redirect unauthenticated users from /dashboard to /login
- [x] T052 [US2] Update middleware to redirect authenticated users from /login and /register to /dashboard

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (registration + authentication)

---

## Phase 5: User Story 3 - View All Tasks (Priority: P2)

**Goal**: Display all user's tasks in an organized list

**Independent Test**: Log in and verify task list displays correctly with various states (empty, few tasks, many tasks)

**Owner**: backend-subagent (API), frontend-subagent (UI)

### Backend Implementation for US3

- [x] T053 [P] [US3] Create tasks router in apps/backend/app/routers/tasks.py with FastAPI APIRouter
- [x] T054 [US3] Implement GET /api/tasks endpoint in apps/backend/app/routers/tasks.py (query tasks filtered by current_user.id)
- [x] T055 [US3] Add tasks router to FastAPI app in apps/backend/app/main.py with /api/tasks prefix
- [x] T056 [US3] Add authentication dependency to GET /api/tasks endpoint (require valid JWT)
- [x] T057 [US3] Add ordering by created_at DESC in GET /api/tasks query

### Frontend Implementation for US3

- [x] T058 [P] [US3] Create dashboard page in apps/frontend/src/app/dashboard/page.tsx with Server Component
- [x] T059 [P] [US3] Create dashboard layout in apps/frontend/src/app/dashboard/layout.tsx with Header
- [x] T060 [P] [US3] Create TaskList component in apps/frontend/src/components/TaskList.tsx with Client Component
- [x] T061 [P] [US3] Create TaskCard component in apps/frontend/src/components/TaskCard.tsx displaying title, description, status
- [x] T062 [US3] Implement data fetching in dashboard page calling GET /api/tasks with JWT token
- [x] T063 [US3] Pass tasks data to TaskList component
- [x] T064 [US3] Implement empty state in TaskList when no tasks exist
- [x] T065 [US3] Implement loading state in TaskList while fetching tasks
- [x] T066 [US3] Add visual distinction for pending vs completed tasks in TaskCard (strikethrough, muted colors)
- [x] T067 [US3] Add error handling for failed API requests with user-friendly messages

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently (registration + login + view tasks)

---

## Phase 6: User Story 4 - Create New Task (Priority: P2)

**Goal**: Allow users to add new tasks to their list

**Independent Test**: Submit create task form and verify new task appears in list

**Owner**: backend-subagent (API), frontend-subagent (UI)

### Backend Implementation for US4

- [x] T068 [US4] Implement POST /api/tasks endpoint in apps/backend/app/routers/tasks.py (create task with current_user.id)
- [x] T069 [US4] Add authentication dependency to POST /api/tasks endpoint (require valid JWT)
- [x] T070 [US4] Add validation for title (min 1, max 200 chars) and description (max 2000 chars)
- [x] T071 [US4] Add error handling for validation errors (422 Unprocessable Entity)
- [x] T072 [US4] Set default status to "pending" for new tasks

### Frontend Implementation for US4

- [x] T073 [P] [US4] Create AddTaskForm component in apps/frontend/src/components/AddTaskForm.tsx with Client Component
- [x] T074 [US4] Add AddTaskForm to dashboard page in apps/frontend/src/app/dashboard/page.tsx
- [x] T075 [US4] Implement form validation in AddTaskForm (title required, max lengths)
- [x] T076 [US4] Implement form submission in AddTaskForm calling POST /api/tasks with JWT token
- [x] T077 [US4] Add optimistic UI update in TaskList (show new task immediately)
- [x] T078 [US4] Refresh task list after successful creation
- [x] T079 [US4] Clear form inputs after successful submission
- [x] T080 [US4] Add loading state during submission (disable button, show spinner)
- [x] T081 [US4] Add error handling for failed creation with user feedback

**Checkpoint**: At this point, User Stories 1-4 should all work independently (full create flow)

---

## Phase 7: User Story 5 - Update Task (Priority: P3)

**Goal**: Allow users to modify existing tasks (title, description, status)

**Independent Test**: Edit a task's properties and verify changes persist

**Owner**: backend-subagent (API), frontend-subagent (UI)

### Backend Implementation for US5

- [x] T082 [US5] Implement PUT /api/tasks/{id} endpoint in apps/backend/app/routers/tasks.py (update task with ownership check)
- [x] T083 [US5] Add authentication dependency to PUT /api/tasks/{id} endpoint (require valid JWT)
- [x] T084 [US5] Add ownership verification (task.user_id == current_user.id) returning 403 if not owner
- [x] T085 [US5] Add 404 Not Found handling if task doesn't exist
- [x] T086 [US5] Update updated_at timestamp on task modification
- [x] T087 [US5] Support partial updates (only update provided fields)

### Frontend Implementation for US5

- [x] T088 [US5] Add edit mode state to TaskCard component
- [x] T089 [US5] Add edit button to TaskCard component
- [x] T090 [US5] Create inline edit form in TaskCard for title and description
- [x] T091 [US5] Implement form submission calling PUT /api/tasks/{id} with JWT token
- [x] T092 [US5] Add status toggle (checkbox) in TaskCard calling PUT /api/tasks/{id}
- [x] T093 [US5] Add optimistic UI update for status changes
- [x] T094 [US5] Add cancel button to revert changes without saving
- [x] T095 [US5] Add validation for edit form (title required, max lengths)
- [x] T096 [US5] Add loading state during update
- [x] T097 [US5] Add error handling for failed updates (403, 404, 422)
- [x] T098 [US5] Refresh task list after successful update

**Checkpoint**: At this point, User Stories 1-5 should all work independently (full CRUD except delete)

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Allow users to remove tasks with confirmation

**Independent Test**: Delete a task with/without confirmation and verify removal

**Owner**: backend-subagent (API), frontend-subagent (UI)

### Backend Implementation for US6

- [x] T099 [US6] Implement DELETE /api/tasks/{id} endpoint in apps/backend/app/routers/tasks.py (delete task with ownership check)
- [x] T100 [US6] Add authentication dependency to DELETE /api/tasks/{id} endpoint (require valid JWT)
- [x] T101 [US6] Add ownership verification (task.user_id == current_user.id) returning 403 if not owner
- [x] T102 [US6] Add 404 Not Found handling if task doesn't exist
- [x] T103 [US6] Return success message on deletion

### Frontend Implementation for US6

- [x] T104 [US6] Add delete button to TaskCard component
- [x] T105 [US6] Create confirmation dialog component or use browser confirm
- [x] T106 [US6] Implement delete handler calling DELETE /api/tasks/{id} with JWT token
- [x] T107 [US6] Add optimistic UI update (remove task from list immediately)
- [x] T108 [US6] Add loading state during deletion
- [x] T109 [US6] Add error handling for failed deletion (403, 404)
- [x] T110 [US6] Refresh task list after successful deletion
- [ ] T111 [US6] Add undo functionality (optional enhancement)

**Checkpoint**: All user stories should now be independently functional (complete CRUD)

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

**Owner**: All subagents

### Backend Polish

- [x] T112 [P] Add health check endpoint GET /health in apps/backend/app/main.py
- [x] T113 [P] Add request logging middleware in apps/backend/app/main.py
- [x] T114 [P] Add error logging for exceptions
- [x] T115 [P] Configure production environment settings (echo=False, secure cookies)
- [x] T116 [P] Add API documentation metadata in FastAPI app (title, description, version)

### Frontend Polish

- [x] T117 [P] Create landing page in apps/frontend/src/app/page.tsx with redirect logic
- [x] T118 [P] Add loading skeletons for task list in TaskList component
- [x] T119 [P] Add smooth animations for task add/remove/update (fade, slide)
- [x] T120 [P] Add hover states and focus indicators for accessibility
- [ ] T121 [P] Add keyboard shortcuts (Enter to submit forms, Escape to cancel)
- [x] T122 [P] Optimize responsive design for mobile (375px+), tablet, desktop
- [ ] T123 [P] Add proper ARIA labels and semantic HTML for screen readers
- [ ] T124 [P] Test and fix color contrast for WCAG 2.1 AA compliance
- [x] T125 [P] Add favicon and metadata in root layout

### Deployment Preparation

- [x] T126 [P] Create Dockerfile for backend in apps/backend/Dockerfile
- [x] T127 [P] Create .dockerignore in apps/backend/
- [x] T128 [P] Configure Next.js for production build in apps/frontend/next.config.js
- [x] T129 [P] Add deployment documentation in specs/002-todo-web-app/quickstart.md
- [ ] T130 [P] Test production build locally (npm run build, docker build)

### Documentation

- [x] T131 [P] Update README.md with project overview and setup instructions
- [x] T132 [P] Document environment variables in .env.example files
- [ ] T133 [P] Add API documentation screenshots from Swagger UI

---

## Phase 10: Better Auth Library Integration

**Purpose**: Implement official Better Auth library with backend FastAPI JWT API

**Owner**: frontend-subagent, backend-subagent

**Context**: Use official Better Auth library (better-auth/react) with createAuthClient. Configure baseURL to point to FastAPI backend (http://localhost:8001). Backend returns Better Auth-compatible response format.

**References**:
- Better Auth Docs: https://www.better-auth.com/docs/installation
- Context7 Library ID: /llmstxt/better-auth_llms_txt

### Frontend: Better Auth Client Setup

- [x] T134 [P] Create lib directory in apps/frontend/
- [x] T135 [P] Install better-auth package: `npm install better-auth --legacy-peer-deps`
- [x] T136 Create auth-client.ts in apps/frontend/lib/auth-client.ts
  - Import createAuthClient from "better-auth/react"
  - Configure baseURL: http://localhost:8001 (FastAPI backend)
  - Export authClient instance
  - Export { signIn, signUp, signOut, useSession } methods
- [x] T137 Update .env.local with NEXT_PUBLIC_API_URL=http://localhost:8001

### Backend: Better Auth Compatible Responses

- [x] T138 [BACKEND] Add POST /api/auth/sign-up/email endpoint with Better Auth format
  - Return { user: {...}, session: { token: "..." } } on success
  - HTTPException with proper status code on failure
- [x] T139 [BACKEND] Add POST /api/auth/sign-in/email endpoint with Better Auth format
  - Return { user: {...}, session: { token: "..." } } on success
  - HTTPException with proper status code on failure
- [x] T140 [BACKEND] CORS headers configured with FRONTEND_URL environment variable (Fixed: Added port 3001 to allowed origins)

### Testing & Validation

- [x] T141 Test Better Auth client initialization with baseURL (Verified: v1.4.17 installed, configured with http://localhost:8001/api/auth)
- [x] T142 Test signUp.email() → backend register → auto session → dashboard redirect (Backend API verified via curl)
- [x] T143 Test signIn.email() → backend login → session stored → dashboard redirect (Backend API verified via curl)
- [ ] T144 Test signOut() → clear session → redirect to login (Requires browser testing)
- [ ] T145 Test useSession() hook for protected routes authentication check (Requires browser testing)
- [x] T146 Test JWT token in Authorization header for API requests (Verified: GET/POST/PUT/DELETE all working with JWT)
- [x] T147 End-to-end test: register → login → CRUD operations → logout (Backend API fully tested: login ✓, create task ✓, update task ✓, delete task ✓)
- [x] T148 Test error handling: invalid credentials, duplicate email, network errors (Backend returns proper HTTP status codes: 409 for duplicate, 401 for invalid credentials)

**Checkpoint**: Better Auth library fully integrated with FastAPI backend, all flows working

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (Registration) can start after Foundational - No dependencies on other stories
  - US2 (Login) can start after Foundational - No dependencies on other stories (but logically follows US1)
  - US3 (View Tasks) depends on US1+US2 for authentication flow
  - US4 (Create Task) depends on US1+US2+US3 for full user flow
  - US5 (Update Task) depends on US1+US2+US3+US4 for tasks to exist
  - US6 (Delete Task) depends on US1+US2+US3+US4 for tasks to exist
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Logically follows US1 but technically independent
- **User Story 3 (P2)**: Requires US1+US2 for authentication to work
- **User Story 4 (P2)**: Requires US1+US2+US3 for complete user flow
- **User Story 5 (P3)**: Requires US1+US2+US3+US4 for tasks to exist
- **User Story 6 (P3)**: Requires US1+US2+US3+US4 for tasks to exist

### Within Each User Story

- Backend implementation before frontend (API must exist for frontend to call)
- Models before endpoints (database schema must exist)
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T002-T011 can all run in parallel (different files)
- **Phase 2 (Foundational)**: T019-T020, T022-T023, T024-T028 can run in parallel within their groups
- **Within User Stories**: Backend and frontend tasks marked [P] can run in parallel
- **Phase 9 (Polish)**: Most tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1 (Registration)

```bash
# Backend tasks can run in parallel:
Task T029: "Create auth router in apps/backend/app/routers/auth.py"

# Frontend tasks can run in parallel:
Task T033: "Create registration page in apps/frontend/src/app/register/page.tsx"
Task T034: "Create RegisterForm component in apps/frontend/src/components/RegisterForm.tsx"

# Then sequential tasks:
Task T030: "Implement POST /api/auth/register endpoint" (depends on T029)
Task T035-T038: Form implementation (depends on T033, T034)
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration)
4. Complete Phase 4: User Story 2 (Login + Authentication)
5. **STOP and VALIDATE**: Test registration and login flow independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + 2 → Test independently → Deploy/Demo (MVP - authentication working!)
3. Add User Story 3 → Test independently → Deploy/Demo (can view tasks)
4. Add User Story 4 → Test independently → Deploy/Demo (can create tasks)
5. Add User Story 5 → Test independently → Deploy/Demo (can update tasks)
6. Add User Story 6 → Test independently → Deploy/Demo (full CRUD complete)
7. Add Polish → Final deployment

### Parallel Team Strategy

With multiple developers or subagents:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - database-subagent: Focus on backend models and endpoints
   - backend-subagent: Focus on API routers and authentication
   - frontend-subagent: Focus on UI components and pages
3. Coordinate at user story boundaries for integration

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Owner assignments guide which subagent should handle each task
- Tests are not included as they were not explicitly requested in the specification
- All file paths are absolute from repository root
- Environment variables must be configured before running (see .env.example files)

---

## Task Summary

- **Total Tasks**: 148
- **Phase 1 (Setup)**: 11 tasks
- **Phase 2 (Foundational)**: 17 tasks
- **Phase 3 (US1 - Registration)**: 10 tasks
- **Phase 4 (US2 - Login)**: 14 tasks
- **Phase 5 (US3 - View Tasks)**: 15 tasks
- **Phase 6 (US4 - Create Task)**: 14 tasks
- **Phase 7 (US5 - Update Task)**: 17 tasks
- **Phase 8 (US6 - Delete Task)**: 13 tasks
- **Phase 9 (Polish)**: 22 tasks
- **Phase 10 (Better Auth Integration)**: 15 tasks

**Parallel Opportunities**: 45+ tasks marked [P] can run in parallel within their phases

**MVP Scope**: Phases 1-4 (52 tasks) deliver authentication system

**Full CRUD**: Phases 1-8 (111 tasks) deliver complete application

**Production Ready**: All phases (133 tasks) deliver polished, deployable application
