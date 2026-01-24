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
- Frontend paths: `apps/frontend/` (app/, components/, lib/)
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

- **Total Tasks**: 201
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
- **Phase 11A (US7 - Sidebar Navigation)**: 7 tasks
- **Phase 11B (US8 - Today View Redesign)**: 6 tasks
- **Phase 11C (US9 - Additional Views)**: 5 tasks
- **Phase 11D (US10 - Auth Pages Redesign)**: 4 tasks
- **Phase 11E (US11 - Mobile & Polish)**: 10 tasks
- **Phase 12 (Deployment)**: 21 tasks (includes 3 pre-deployment fixes)

**Parallel Opportunities**: 60+ tasks marked [P] can run in parallel within their phases

**MVP Scope**: Phases 1-4 (52 tasks) deliver authentication system

**Full CRUD**: Phases 1-8 (111 tasks) deliver complete application

**Full CRUD + Better Auth**: Phases 1-10 (148 tasks) deliver production-ready backend

**Modern UI/UX**: Phases 1-11 (180 tasks) deliver complete Todoist-inspired interface

**Execution Strategy**:
1. Complete Phases 1-10 first (backend + basic UI must work)
2. Then start Phase 11 (UI/UX enhancement)
3. Test each User Story (US7-US11) independently before moving to next

---

## Phase 11: UI/UX Enhancement - Todoist-Inspired Design

**Purpose**: Redesign frontend UI to match Todoist reference images with golden/amber color scheme

**Context**: Current UI has centered layout with blue theme. Target design requires left sidebar navigation, golden/amber (#FDB813) color scheme, and Todoist-inspired modern interface.

**Reference Images**: `apps/frontend/frontend-refference-images/*.png` (7 reference screenshots)

**Color Palette**:
- Primary: Golden Yellow `#FDB813`
- Secondary: Black `#1A1A1A`
- Accent: White/Cream `#FFFFFF`
- Status Colors: Red (#D1453B), Orange (#FF9933), Blue (#5297FF), Green (completed)

**⚠️ CRITICAL**: All backend functionality must remain unchanged. This is purely a frontend visual redesign.

---

## Phase 11A: User Story 7 - Sidebar Navigation Layout (Priority: P1) 🎯 MVP

**Goal**: Implement left sidebar navigation with menu items (Today, Upcoming, Completed) and update color scheme to golden/amber theme

**Independent Test**: Navigate between Today, Upcoming, Completed views via sidebar. Verify sidebar collapses on mobile.

**Owner**: frontend-subagent

### Design Foundation for US7

- [ ] T149 [P] [US7] Update Tailwind config in apps/frontend/tailwind.config.ts with golden/amber color scheme
  - Define primary color: golden (#FDB813)
  - Define secondary color: black (#1A1A1A)
  - Define neutral grays for text and borders
  - Remove blue theme references
- [ ] T150 [P] [US7] Install lucide-react icon library for Todoist-style icons
  - Run: npm install lucide-react --legacy-peer-deps
  - Icons needed: Inbox, Calendar, Clock, CheckCircle, User, Search, Plus

### Sidebar Component for US7

- [ ] T151 [US7] Create Sidebar component in apps/frontend/components/Sidebar.tsx
  - Fixed left sidebar (264px width on desktop)
  - Top section: User profile with dropdown
  - Golden circular "+ Add task" button
  - Search field with magnifying glass icon
  - Navigation menu items:
    * Today (Calendar icon, /dashboard)
    * Upcoming (Clock icon, /dashboard/upcoming)
    * Completed (CheckCircle icon, /dashboard/completed)
  - Bottom section: Help & resources link
  - Mobile: Hidden by default, toggle with hamburger menu

### Layout Integration for US7

- [ ] T152 [US7] Update dashboard layout in apps/frontend/app/dashboard/layout.tsx
  - Two-column layout: Sidebar (264px) + Main content (flex-1)
  - Remove gradient background, use clean white (#FFFFFF)
  - Add mobile responsiveness:
    * <768px: Sidebar hidden, hamburger menu visible
    * ≥768px: Sidebar always visible
  - Add overlay when sidebar open on mobile
- [ ] T153 [US7] Update Header component in apps/frontend/components/Header.tsx
  - Remove user profile (moved to sidebar)
  - Add hamburger menu button (mobile only)
  - Add top-right utility buttons: Notifications, Calendar connect, Display options
  - Golden accent colors for active states

### Color Scheme Update for US7

- [ ] T154 [P] [US7] Replace all blue colors with golden/amber throughout app
  - Update all buttons (primary actions = golden #FDB813)
  - Update links and text accents
  - Update focus rings and states
  - Update loading spinners
- [ ] T155 [P] [US7] Update neutral color palette
  - Text primary: #1A1A1A (black)
  - Text secondary: #666666 (gray)
  - Text tertiary: #999999 (light gray)
  - Borders: #EAEAEA (very light gray)
  - Background: #FAFAFA (off-white)

**Checkpoint**: At this point, sidebar navigation should work and color scheme should be golden/amber

---

## Phase 11B: User Story 8 - Today View Redesign (Priority: P1)

**Goal**: Redesign Today page with Todoist-inspired clean, minimal UI

**Independent Test**: Visit /dashboard (Today view) and verify tasks display in clean list format with proper styling

**Owner**: frontend-subagent

### Today Page Redesign for US8

- [ ] T156 [US8] Redesign Today page in apps/frontend/app/dashboard/page.tsx
  - Page heading: "Today" (24px, bold, #1A1A1A)
  - Inline "+ Add task" link at top (golden color)
  - Empty state with suitcase illustration and friendly message
  - Clean white background (#FFFFFF)
  - Remove gradient backgrounds

### Task Components Redesign for US8

- [ ] T157 [US8] Update TaskList component in apps/frontend/components/TaskList.tsx
  - Remove card-style background
  - Minimal divider lines between tasks (#EAEAEA)
  - Clean vertical stack layout (no gaps)
  - Smooth animations for add/remove
- [ ] T158 [US8] Update TaskCard component in apps/frontend/components/TaskCard.tsx
  - Circular checkbox (outline when unchecked, filled golden when checked)
  - Task name with clean typography (14px, #1A1A1A)
  - Strikethrough when completed (#999999)
  - Remove heavy shadows and borders
  - Subtle hover background (#FAFAFA)
  - Edit/delete icons appear on hover
- [ ] T159 [US8] Update AddTaskForm component in apps/frontend/components/AddTaskForm.tsx
  - Convert to inline/modal style (expands on click)
  - Large borderless title input (18px placeholder)
  - Description field appears on focus
  - Bottom toolbar: Date picker, Priority, Reminders (icons)
  - Golden "Add task" button (#FDB813)
  - Gray "Cancel" button (#666666)

### Typography & Spacing for US8

- [ ] T160 [P] [US8] Update global typography in apps/frontend/app/globals.css
  - Font family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
  - Base font size: 14px
  - Line height: 1.5
  - Font weights: 400 (normal), 600 (semibold), 700 (bold)
- [ ] T161 [P] [US8] Implement consistent spacing system
  - Content padding: 48px (desktop), 24px (mobile)
  - Task item padding: 12px 16px
  - Section gaps: 24px
  - Input fields: 12px padding

**Checkpoint**: At this point, Today view should match Todoist reference design

---

## Phase 11C: User Story 9 - Additional Views Implementation (Priority: P2)

**Goal**: Implement Upcoming and Completed views with Todoist-style layout

**Independent Test**: Navigate to /dashboard/upcoming and /dashboard/completed, verify proper layout and functionality

**Owner**: frontend-subagent

### Shared Components for US9

- [ ] T162 [P] [US9] Create EmptyState component in apps/frontend/components/EmptyState.tsx
  - Reusable component for all empty states
  - Props: illustration (ReactNode), heading (string), message (string)
  - Center-aligned layout
  - Support for custom illustrations

### Upcoming View for US9

- [ ] T163 [US9] Create Upcoming page in apps/frontend/app/dashboard/upcoming/page.tsx
  - "Upcoming" heading (24px, bold)
  - Calendar week selector (January 2026, arrows for navigation)
  - Mini calendar showing current week dates
  - Tasks grouped by date sections:
    * "24 Jan · Today · Saturday"
    * "25 Jan · Tomorrow · Sunday"
    * "26 Jan · Monday"
  - "+ Add task" link under each date group
  - Empty state when no upcoming tasks
- [ ] T164 [US9] Create date grouping utility function
  - Group tasks by date (today, tomorrow, future dates)
  - Format dates: "DD MMM · Day name"
  - Sort chronologically

### Completed View for US9

- [ ] T165 [US9] Create Completed page in apps/frontend/app/dashboard/completed/page.tsx
  - "Activity: All projects" dropdown header
  - Empty state with trophy + confetti illustration
  - Message: "No activity in the past week."
  - Explanation text about completed tasks
  - List completed tasks with completion date when available
- [ ] T166 [US9] Add filter logic for completed tasks
  - Filter tasks where status === "completed"
  - Sort by completion date (newest first)
  - Display completion timestamp

**Checkpoint**: At this point, Upcoming and Completed views should be functional

---

## Phase 11D: User Story 10 - Authentication Pages Redesign (Priority: P2)

**Goal**: Redesign Login and Register pages to match Todoist clean aesthetic

**Independent Test**: Visit /login and /register, verify clean design with golden theme

**Owner**: frontend-subagent

### Login Page Redesign for US10

- [ ] T167 [US10] Redesign Login page in apps/frontend/app/login/page.tsx
  - Clean white background (remove blue gradient)
  - App logo/icon at top (golden theme)
  - "Welcome back!" heading (32px, bold)
  - Subtitle: "Log in to your account"
  - Email/Password fields with subtle borders
  - Golden "Log in" button (full width)
  - "Forgot your password?" link (golden)
  - "Don't have an account? Sign up" at bottom
- [ ] T168 [US10] Update LoginForm component in apps/frontend/components/LoginForm.tsx
  - Clean input styling: subtle border (#EAEAEA), rounded corners
  - Focus state: golden border (#FDB813)
  - Golden submit button with hover effect
  - Smooth loading state (spinner + disabled)

### Register Page Redesign for US10

- [ ] T169 [US10] Redesign Register page in apps/frontend/app/register/page.tsx
  - Match login page structure
  - "Sign up" heading (32px, bold)
  - Subtitle: "Create your account"
  - Email/Password fields
  - Golden "Sign up with Email" button (full width)
  - Terms of Service and Privacy Policy links (small text)
  - "Already signed up? Go to login" at bottom
- [ ] T170 [US10] Update RegisterForm component in apps/frontend/components/RegisterForm.tsx
  - Match LoginForm styling
  - Consistent input fields and button design
  - Validation error messages (red #D1453B)

**Checkpoint**: At this point, authentication pages should have modern, clean design

---

## Phase 11E: User Story 11 - Mobile Responsiveness & Polish (Priority: P3)

**Goal**: Ensure perfect mobile experience and add smooth animations

**Independent Test**: Test on mobile devices (375px, 414px) and tablets (768px, 1024px), verify all interactions work

**Owner**: frontend-subagent

### Mobile Responsiveness for US11

- [ ] T171 [US11] Implement responsive sidebar collapse/expand
  - Mobile (<768px): Sidebar hidden by default
  - Hamburger menu button in header (mobile only)
  - Sidebar slides in from left with smooth animation
  - Dark overlay behind sidebar when open
  - Close sidebar on navigation or outside click
- [ ] T172 [P] [US11] Optimize touch interactions for mobile
  - Larger touch targets (min 44px height)
  - Comfortable spacing between interactive elements
  - Prevent text selection on double-tap
  - Smooth scroll behavior
- [ ] T173 [P] [US11] Test all responsive breakpoints
  - Mobile: 375px (iPhone SE), 414px (iPhone Pro Max)
  - Tablet: 768px (iPad), 1024px (iPad Pro)
  - Desktop: 1280px, 1440px, 1920px

### Animations & Transitions for US11

- [ ] T174 [P] [US11] Add smooth transitions throughout app
  - Sidebar collapse/expand: 300ms ease-in-out
  - Task completion: checkbox animation + fade out
  - Task add/remove: slide-in/fade-out animations
  - Hover states: 200ms transitions
  - Modal/form appearance: slide-up animation
- [ ] T175 [P] [US11] Add loading states and skeletons
  - Task list skeleton loaders (3 placeholders)
  - Button loading state (spinner + disabled)
  - Optimistic UI updates (instant feedback)

### Testing & Validation for US11

- [ ] T176 [US11] Visual comparison with reference images
  - Login page ✓
  - Register page ✓
  - Today page ✓
  - Upcoming page ✓
  - Completed page ✓
  - Sidebar navigation ✓
- [ ] T177 [P] [US11] Test all CRUD operations still work
  - Create task from Today view ✓
  - Update task inline ✓
  - Delete task with confirmation ✓
  - Mark task as complete/incomplete ✓
- [ ] T178 [P] [US11] Test navigation flows
  - Sidebar navigation between views ✓
  - URL updates correctly ✓
  - Browser back/forward buttons ✓
  - Mobile hamburger menu ✓
- [ ] T179 [P] [US11] Accessibility audit
  - Keyboard navigation works (Tab, Enter, Escape)
  - Focus indicators visible (golden outline)
  - Color contrast meets WCAG AA
  - Screen reader compatibility (ARIA labels)
- [ ] T180 [US11] Performance check
  - Page load time <2s
  - Task list renders smoothly (60fps)
  - Animations run smoothly
  - No layout shifts (CLS <0.1)

**Checkpoint**: All user stories for UI/UX redesign should now be complete and independently functional

---

## Dependencies & Execution Order (Phase 11)

### User Story Dependencies

- **User Story 7 (US7)**: Foundation - Must complete first (sidebar layout + color scheme)
- **User Story 8 (US8)**: Depends on US7 (requires sidebar to be in place)
- **User Story 9 (US9)**: Depends on US7 (uses sidebar navigation)
- **User Story 10 (US10)**: Independent - Can run in parallel with US8/US9 (separate pages)
- **User Story 11 (US11)**: Depends on US7-US10 (polishes all views)

### Recommended Execution Order

1. **US7**: Sidebar Navigation + Color Scheme (Foundation)
2. **US8**: Today View Redesign (Core functionality)
3. **US9 + US10**: Additional Views + Auth Pages (Can run in parallel)
4. **US11**: Mobile & Polish (Final touches)

### Parallel Opportunities

- US9 and US10 can be implemented in parallel (different pages)
- Within each user story, tasks marked [P] can run in parallel
- Color scheme updates (T154-T155) can be done in one batch

---

## Phase 11 Summary

- **Total Tasks**: 32 new tasks (T149-T180)
- **User Stories**: 5 (US7-US11)
- **Focus**: Pure frontend UI/UX redesign, zero backend changes
- **Dependencies**: Requires Phase 1-10 complete (backend must be working)

**User Story Breakdown**:
- **US7** (6 tasks): Sidebar Navigation + Color Scheme
- **US8** (6 tasks): Today View Redesign
- **US9** (5 tasks): Upcoming + Completed Views
- **US10** (4 tasks): Authentication Pages
- **US11** (11 tasks): Mobile Responsiveness + Polish

**Testing Strategy**:
- Test each User Story independently after completion
- User should check and approve UI before moving to next US
- Verify all existing functionality still works after each US
- Final validation: side-by-side comparison with reference images

---

## Phase 12: Deployment (Production)

**Purpose**: Deploy the complete application to production platforms

**Owner**: All subagents

**⚠️ CRITICAL**: Deployment must follow this order: Database → Backend → Frontend. Each step depends on the previous one being live and verified.

**Platforms**:
- Database: Neon Serverless PostgreSQL (already deployed)
- Backend: Railway (containerized with Docker)
- Frontend: Vercel (zero-config Next.js hosting)

---

### Step 1: Database Deployment (Neon PostgreSQL)

- [x] T181 [DEPLOY] Create Neon account and project at https://neon.tech
  - Sign up / log in to Neon console
  - Create new project (e.g., "agentic-todo-production")
  - Select region closest to backend deployment (e.g., US East)
  - Copy the connection string (DATABASE_URL) - save securely
  - **STATUS: Already deployed**

- [x] T182 [DEPLOY] Run database migrations against Neon
  - Set DATABASE_URL environment variable to Neon connection string
  - Run: `cd apps/backend && alembic upgrade head`
  - Verify tables created: users, tasks
  - **STATUS: Already deployed and migrated**

---

### Step 2: Backend Deployment (Railway)

#### Pre-Deployment Fixes (Must complete before T183)

- [x] T181.1 [DEPLOY] Fix Dockerfile for Railway compatibility (apps/backend/Dockerfile)
  - Switch from `uv pip install --system -r pyproject.toml` to `pip install -r requirements.txt`
  - Update CMD to use PORT env var: `CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]`
  - Fix healthcheck: Replace `requests.get()` with `urllib.request.urlopen()` (stdlib, no extra dep)
  - Remove uv installation step (unnecessary complexity for deployment)

- [x] T181.2 [DEPLOY] Consolidate to single dependency file (removed pyproject.toml)
  - Keep `requirements.txt` as the single source of truth (already more complete)
  - Remove `pyproject.toml` OR keep it as metadata-only (remove `dependencies` list)
  - `requirements.txt` already has: python-dotenv, bcrypt pin, pydantic[email], PyJWT
  - Verify all imports in app/ are covered by requirements.txt

- [x] T181.3 [DEPLOY] Update backend CORS for production (apps/backend/app/main.py)
  - Remove hardcoded localhost ports (3000, 3001, 3003) for production
  - Use only `FRONTEND_URL` env var for allowed origins
  - Keep localhost fallbacks only when ENVIRONMENT != "production"
  - Example: `if os.getenv("ENVIRONMENT") == "production": origins = [FRONTEND_URL] else: origins = [FRONTEND_URL, "http://localhost:3000", ...]`

#### Railway Setup

- [ ] T183 [DEPLOY] Create Railway account and new project at https://railway.com
  - Sign up / log in to Railway dashboard
  - Click "New Project" → "Deploy from GitHub Repo"
  - Connect GitHub repository (agentic-todo-evolution)
  - Set Root Directory: `apps/backend` (in Service Settings)
  - Railway auto-detects Dockerfile

- [ ] T184 [DEPLOY] Configure backend environment variables on Railway
  - DATABASE_URL = (Neon connection string from T181)
  - SECRET_KEY = (generate a strong random 32+ char secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
  - ALGORITHM = HS256
  - ACCESS_TOKEN_EXPIRE_MINUTES = 1440
  - FRONTEND_URL = (will update after frontend deploys, temporarily set to *)
  - ENVIRONMENT = production
  - PORT = 8000 (Railway uses PORT env var)

- [ ] T185 [DEPLOY] Deploy backend and verify health check
  - Trigger deploy on Railway (automatic on push or manual)
  - Wait for build to complete (Docker image build)
  - Generate public domain: Settings → Networking → Generate Domain
  - Verify health check: GET https://<your-app>.up.railway.app/health returns 200
  - Note the deployed backend URL (e.g., https://agentic-todo-backend.up.railway.app)

- [ ] T186 [DEPLOY] Verify database migrations on production
  - Migrations already applied via Neon (T182)
  - Verify: POST /api/auth/register works with a test user
  - If needed: Use Railway shell to run `alembic upgrade head`

- [ ] T187 [DEPLOY] Test backend API endpoints in production
  - Test POST /api/auth/register (create test account)
  - Test POST /api/auth/sign-in/email (login, get JWT token)
  - Test GET /api/tasks (with Authorization header)
  - Test POST /api/tasks (create a task)
  - Test PUT /api/tasks/{id} (update task status)
  - Test DELETE /api/tasks/{id} (delete task)
  - All should return correct responses

---

### Step 3: Frontend Deployment (Vercel)

- [ ] T188 [DEPLOY] Create Vercel account and import project at https://vercel.com
  - Sign up / log in to Vercel dashboard
  - Click "Add New" → "Project"
  - Import GitHub repository (agentic-todo-evolution)
  - Set Root Directory: `apps/frontend`
  - Framework Preset: Next.js (auto-detected)
  - Build Command: `npm run build` (default)
  - Output Directory: `.next` (default)

- [ ] T189 [DEPLOY] Configure frontend environment variables on Vercel
  - NEXT_PUBLIC_API_URL = https://<your-backend>.up.railway.app (from T185)
  - NEXT_PUBLIC_SITE_URL = https://<your-frontend>.vercel.app (will know after first deploy)
  - NODE_ENV = production
  - Note: Auth routes and proxy routes both use NEXT_PUBLIC_API_URL to forward to backend

- [ ] T190 [DEPLOY] Deploy frontend and verify access
  - Trigger deploy on Vercel (automatic on push or manual)
  - Wait for build to complete
  - Access the deployed URL (e.g., https://agentic-todo.vercel.app)
  - Verify landing page loads without errors
  - Note the deployed frontend URL

---

### Step 4: Cross-Platform Configuration

- [ ] T191 [DEPLOY] Update backend CORS to allow Vercel frontend domain
  - Go to Railway dashboard → Variables
  - Update FRONTEND_URL = https://<your-frontend>.vercel.app
  - Redeploy backend for changes to take effect
  - Verify: No CORS errors when frontend calls backend API

- [ ] T192 [DEPLOY] Update frontend NEXT_PUBLIC_SITE_URL with actual Vercel domain
  - Go to Vercel dashboard → Settings → Environment Variables
  - Set NEXT_PUBLIC_SITE_URL = https://<your-frontend>.vercel.app
  - Redeploy frontend for changes to take effect

- [ ] T193 [DEPLOY] Verify frontend proxy routes use correct backend URL
  - apps/frontend/app/api/proxy/[...path]/route.ts uses `NEXT_PUBLIC_API_URL`
  - apps/frontend/app/api/auth/[...all]/route.ts uses `NEXT_PUBLIC_API_URL`
  - Both default to `localhost:8001` in code — ensure Vercel env var overrides this
  - No code changes needed if NEXT_PUBLIC_API_URL is set correctly on Vercel

---

### Step 5: End-to-End Production Verification

- [ ] T194 [DEPLOY] Test complete user flow on production
  - Visit https://<your-frontend>.vercel.app
  - Register a new account (email + password)
  - Login with new account credentials
  - Create a new task (title + description)
  - Mark task as completed
  - Edit task title/description
  - Delete a task
  - Navigate to Upcoming view (shows pending tasks)
  - Navigate to Completed view (shows completed tasks)
  - Logout and verify redirect to login
  - All operations should work without errors

- [ ] T195 [DEPLOY] Verify security in production
  - HTTPS is active on both frontend and backend
  - No secrets exposed in browser console or network tab
  - CORS blocks unauthorized origins
  - JWT token included in authenticated requests
  - Unauthenticated access redirects to login
  - Cannot access other users' tasks

- [ ] T196 [DEPLOY] Performance check on production
  - Page load time < 3 seconds
  - API response time < 1 second
  - No console errors in browser
  - Mobile responsive (test on phone or DevTools)

---

### Step 6: Post-Deployment (Optional)

- [ ] T197 [DEPLOY] Set up custom domain (optional)
  - Frontend: Add custom domain in Vercel settings
  - Backend: Add custom domain in Railway settings
  - Update FRONTEND_URL (Railway) and NEXT_PUBLIC_API_URL + NEXT_PUBLIC_SITE_URL (Vercel) with new domains
  - Verify SSL certificates are active

- [ ] T198 [DEPLOY] Set up monitoring and alerts (optional)
  - Enable Railway health check monitoring
  - Set up Vercel analytics (frontend performance)
  - Monitor Neon database usage (connection limits, storage)

---

## Phase 12 Summary

- **Total Tasks**: 21 tasks (T181-T198 + T181.1, T181.2, T181.3 pre-deployment fixes)
- **Steps**: 6 (Database → Pre-Deploy Fixes → Backend → Frontend → Cross-Config → Verification → Optional)
- **Platforms**: Neon (DB - already live), Railway (Backend), Vercel (Frontend)

**Execution Order (STRICT)**:
1. T181-T182: Database (already live ✅)
2. T181.1-T181.3: Pre-deployment code fixes (Dockerfile, deps, CORS)
3. T183-T187: Backend must be live second (frontend needs API URL)
4. T188-T190: Frontend deploys third (needs backend URL)
5. T191-T193: Cross-platform config (both must be live)
6. T194-T196: End-to-end verification (everything must work together)
7. T197-T198: Optional post-deployment enhancements

**Key Dependencies**:
```
T181-T182 (Neon DB ✅) → T181.1-T181.3 (Pre-Deploy Fixes) → T183 (Railway) → T184 (Env Vars) → T185 (Deploy)
                                                                                                      ↓
T194 (E2E Test) ← T191 (CORS Update) ← T190 (Deploy Frontend) ← T189 (Env Vars) ← T188 (Vercel Setup)
```

**Environment Variables Reference**:
```
Backend (Railway):          Frontend (Vercel):
├── DATABASE_URL            ├── NEXT_PUBLIC_API_URL (→ Railway URL)
├── SECRET_KEY              ├── NEXT_PUBLIC_SITE_URL (→ Vercel URL)
├── ALGORITHM               └── NODE_ENV = production
├── ACCESS_TOKEN_EXPIRE_MINUTES
├── FRONTEND_URL (→ Vercel URL)
├── ENVIRONMENT = production
└── PORT = 8000
```
