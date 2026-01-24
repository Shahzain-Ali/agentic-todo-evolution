# Implementation Plan: Full-Stack Todo Web Application

**Branch**: `002-todo-web-app` | **Date**: 2026-01-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-web-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a full-stack todo application enabling users to register, authenticate, and manage personal tasks through a responsive web interface. The system implements user isolation, JWT-based authentication, and CRUD operations for tasks. Frontend built with Next.js 16+ and Better Auth, backend with FastAPI and SQLModel, database on Neon Serverless PostgreSQL. Deployed as a monorepo with frontend on Vercel and backend API on cloud platform (Railway/Render/Fly.io).

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5+ with Next.js 16+, React 19+
- Backend: Python 3.11+ with FastAPI 0.100+

**Primary Dependencies**:
- Frontend: Next.js 16+ (App Router), React 19+ (Server Components), Tailwind CSS 4+, Better Auth
- Backend: FastAPI 0.100+, SQLModel 0.14+, Pydantic v2, python-jose (JWT), passlib (bcrypt), uvicorn

**Storage**: Neon Serverless PostgreSQL 15+ with SQLModel ORM and Alembic migrations

**Testing**:
- Backend: pytest with pytest-asyncio for async tests
- Frontend: Jest + React Testing Library (unit), Playwright (E2E - optional)

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions), responsive (375px+)
- Backend: Linux server (containerized with Docker)

**Project Type**: Web application (monorepo with separate frontend and backend)

**Performance Goals**:
- API response time: <500ms p95 latency
- Frontend load time: <2 seconds for task list display
- Support 100 concurrent users without degradation

**Constraints**:
- JWT tokens expire after 24 hours
- Password minimum 8 characters with bcrypt hashing
- Title max 200 characters, description max 2000 characters
- WCAG 2.1 Level AA accessibility compliance
- HTTPS/TLS required for all communications

**Scale/Scope**:
- Initial launch: 100 concurrent users
- Database: 2 tables (users, tasks) with one-to-many relationship
- API: 6 RESTful endpoints
- Frontend: 4 main pages (login, register, dashboard, task management)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Status**: No constitution.md file exists yet. This is the first feature implementation for the hackathon project.

**Recommended Principles** (to be added to constitution.md):
1. **Security First**: All passwords hashed with bcrypt, JWT tokens for authentication, user isolation enforced
2. **Test-Driven Development**: Write tests before implementation (pytest for backend, Jest for frontend)
3. **Accessibility**: WCAG 2.1 Level AA compliance mandatory
4. **Simplicity**: Start with minimal viable features, avoid over-engineering
5. **Monorepo Organization**: Clear separation between frontend and backend with shared contracts

**Gates**:
- ✅ No unnecessary complexity (using standard REST API, no microservices)
- ✅ Security requirements defined (JWT, bcrypt, HTTPS, user isolation)
- ✅ Testing strategy defined (pytest, optional E2E)
- ✅ Clear deployment targets (Vercel, Railway/Render/Fly.io, Neon)

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-web-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts)
│   ├── api-endpoints.md # OpenAPI-style endpoint documentation
│   └── data-models.md   # Request/response schemas
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
agentic-todo-evolution/
├── apps/
│   ├── frontend/                    # Next.js 16+ application
│   │   ├── src/
│   │   │   ├── app/                 # App Router pages
│   │   │   │   ├── layout.tsx       # Root layout
│   │   │   │   ├── page.tsx         # Landing/redirect page
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx     # Login page
│   │   │   │   ├── register/
│   │   │   │   │   └── page.tsx     # Registration page
│   │   │   │   ├── dashboard/
│   │   │   │   │   ├── layout.tsx   # Dashboard layout (protected)
│   │   │   │   │   └── page.tsx     # Task list page
│   │   │   │   └── api/
│   │   │   │       └── auth/
│   │   │   │           └── [...all]/route.ts  # Better Auth API routes
│   │   │   ├── components/          # React components
│   │   │   │   ├── TaskCard.tsx
│   │   │   │   ├── TaskList.tsx
│   │   │   │   ├── AddTaskForm.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── RegisterForm.tsx
│   │   │   └── lib/                 # Utilities
│   │   │       ├── auth.ts          # Better Auth configuration
│   │   │       └── api-client.ts    # API client with JWT handling
│   │   ├── middleware.ts            # Route protection middleware
│   │   ├── tailwind.config.ts       # Tailwind CSS configuration
│   │   ├── tsconfig.json            # TypeScript configuration
│   │   ├── next.config.js           # Next.js configuration
│   │   ├── package.json             # Dependencies
│   │   └── .env.local               # Environment variables (not committed)
│   │
│   └── backend/                     # FastAPI application
│       ├── app/
│       │   ├── main.py              # FastAPI app entry point
│       │   ├── database.py          # Database connection and session
│       │   ├── models/              # SQLModel models
│       │   │   ├── __init__.py
│       │   │   ├── user.py          # User model
│       │   │   └── task.py          # Task model
│       │   ├── schemas/             # Pydantic request/response schemas
│       │   │   ├── __init__.py
│       │   │   ├── auth.py          # Auth schemas (register, login)
│       │   │   └── task.py          # Task schemas (create, update, response)
│       │   ├── routers/             # API route handlers
│       │   │   ├── __init__.py
│       │   │   ├── auth.py          # Authentication endpoints
│       │   │   └── tasks.py         # Task CRUD endpoints
│       │   └── auth/                # Authentication utilities
│       │       ├── __init__.py
│       │       ├── jwt.py           # JWT token creation/verification
│       │       ├── password.py      # Password hashing/verification
│       │       └── dependencies.py  # FastAPI dependencies (get_current_user)
│       ├── tests/                   # Test suite
│       │   ├── __init__.py
│       │   ├── conftest.py          # Pytest fixtures
│       │   ├── unit/
│       │   │   ├── test_auth.py     # Auth utility tests
│       │   │   └── test_models.py   # Model validation tests
│       │   └── integration/
│       │       ├── test_auth_flow.py    # Registration/login tests
│       │       └── test_task_crud.py    # Task CRUD tests
│       ├── alembic/                 # Database migrations
│       │   ├── versions/
│       │   └── env.py
│       ├── alembic.ini              # Alembic configuration
│       ├── requirements.txt         # Python dependencies
│       ├── Dockerfile               # Container image
│       └── .env                     # Environment variables (not committed)
│
├── .claude/                         # Agent Skills and Subagents
│   ├── skills/
│   │   ├── frontend-builder/        # Next.js expertise
│   │   ├── backend-api/             # FastAPI expertise
│   │   └── database-schema/         # SQLModel expertise
│   └── agents/
│       ├── frontend-subagent.md     # Frontend specialist
│       ├── backend-subagent.md      # Backend specialist
│       └── database-subagent.md     # Database specialist
│
├── specs/                           # Feature specifications
│   ├── 001-todo-console-app/        # Phase 1 (completed)
│   └── 002-todo-web-app/            # Phase 2 (this feature)
│
├── history/                         # Prompt History Records
│   └── prompts/
│       └── 002-todo-web-app/
│
├── README.md                        # Project documentation
└── .gitignore                       # Git ignore rules
```

**Structure Decision**: Web application monorepo structure selected. Frontend and backend are separate applications with clear boundaries. Frontend communicates with backend via REST API. Database accessed only by backend. This structure supports independent deployment, clear separation of concerns, and enables specialized subagents to work on their respective domains without conflicts.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. This is a straightforward web application with standard architecture patterns.

## Architecture Decisions

### 1. Frontend Architecture (Next.js 16+ with App Router)

**Technology Stack**:
- Next.js 16+ with App Router (file-based routing in `src/app/`)
- React 19+ with Server Components (default) and Client Components (for interactivity)
- TypeScript 5+ (strict mode enabled)
- Tailwind CSS 4+ (utility-first styling)
- Better Auth (authentication library with JWT support)

**Key Patterns**:

**App Router Structure**:
- Server Components by default (pages, layouts)
- Client Components marked with `'use client'` directive (forms, interactive elements)
- Route protection via middleware.ts
- API routes in `app/api/` directory

**Better Auth Integration**:
- Configuration in `src/lib/auth.ts`
- JWT tokens stored in httpOnly cookies
- Middleware protects `/dashboard` routes
- Auth API routes at `/api/auth/[...all]`

**API Communication**:
- Centralized API client in `src/lib/api-client.ts`
- Automatically adds `Authorization: Bearer <token>` header
- Handles 401 responses (redirect to login)
- Supports all CRUD operations

**Component Architecture**:
- Presentational components (TaskCard, TaskList)
- Form components (LoginForm, RegisterForm, AddTaskForm)
- Layout components (Header, Dashboard layout)
- Reusable, composable, testable

**Styling Strategy**:
- Tailwind CSS utility classes
- Custom theme in `tailwind.config.ts` (colors, spacing, typography)
- Responsive design (mobile-first)
- Accessibility (WCAG 2.1 AA)

### 2. Backend Architecture (FastAPI with SQLModel)

**Technology Stack**:
- FastAPI 0.100+ (async web framework)
- SQLModel 0.14+ (ORM combining SQLAlchemy + Pydantic)
- Pydantic v2 (request/response validation)
- python-jose (JWT token handling)
- passlib with bcrypt (password hashing)
- uvicorn (ASGI server)

**Key Patterns**:

**Async Endpoints**:
- All route handlers use `async def`
- Async database sessions with SQLModel
- Non-blocking I/O for better performance

**JWT Authentication**:
- Token generation in `app/auth/jwt.py`
- Token verification via FastAPI dependency injection
- `get_current_user` dependency extracts user from token
- Applied to all `/api/tasks` endpoints

**Router Organization**:
- Modular structure with separate routers
- `/api/auth` router (register, login)
- `/api/tasks` router (CRUD operations)
- Registered in `main.py`

**Request/Response Validation**:
- Pydantic schemas in `app/schemas/`
- Automatic validation and serialization
- Clear error messages for invalid input

**Error Handling**:
- HTTPException for API errors
- 401 Unauthorized (invalid/missing token)
- 403 Forbidden (user doesn't own resource)
- 404 Not Found (resource doesn't exist)
- 409 Conflict (duplicate email)
- 422 Unprocessable Entity (validation errors)

**CORS Configuration**:
- Configured in `main.py`
- Allow frontend origin (Vercel domain)
- Allow credentials (cookies)
- Restrict to necessary methods and headers

### 3. Database Architecture (Neon Serverless PostgreSQL)

**Technology Stack**:
- Neon Serverless PostgreSQL 15+
- SQLModel 0.14+ (ORM)
- Alembic (migration tool)
- psycopg3 (PostgreSQL driver)

**Schema Design**:

**Users Table**:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Tasks Table**:
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

**Relationships**:
- One-to-many: User → Tasks
- Foreign key constraint with CASCADE delete
- Indexes on user_id and status for query performance

**SQLModel Models**:
- Type-safe models with Pydantic validation
- Automatic serialization to/from database
- Relationship definitions for ORM queries

**Migration Strategy**:
- Alembic for version-controlled schema changes
- Initial migration creates both tables
- Future migrations for schema evolution

**Connection Management**:
- Connection pooling via SQLModel engine
- Async sessions for non-blocking database access
- Environment variable for DATABASE_URL
- Health check endpoint verifies connection

### 4. Authentication Flow

**Registration Flow**:
1. User submits email + password to frontend form
2. Frontend validates input (email format, password length)
3. Frontend sends POST to `/api/auth/register`
4. Backend validates uniqueness of email
5. Backend hashes password with bcrypt (12 rounds)
6. Backend creates user record in database
7. Backend returns user object (without password)
8. Frontend redirects to login page with success message

**Login Flow**:
1. User submits email + password to frontend form
2. Frontend sends POST to `/api/auth/login`
3. Backend queries user by email
4. Backend verifies password with bcrypt
5. Backend generates JWT token (24-hour expiration)
6. Backend returns `{ access_token, token_type: "bearer" }`
7. Frontend stores token (Better Auth handles storage)
8. Frontend redirects to dashboard

**Protected Request Flow**:
1. Frontend makes request to protected endpoint
2. API client adds `Authorization: Bearer <token>` header
3. Backend middleware extracts token from header
4. Backend verifies token signature and expiration
5. Backend extracts user_id from token payload
6. Backend queries database filtered by user_id
7. Backend returns user-specific data
8. Frontend displays data

**Logout Flow**:
1. User clicks logout button
2. Frontend clears token (Better Auth handles)
3. Frontend redirects to login page

**Token Expiration Handling**:
1. Backend detects expired token
2. Backend returns 401 Unauthorized
3. Frontend API client catches 401
4. Frontend redirects to login page with message

### 5. API Contracts

**Base URL**: `https://api.example.com` (backend deployment URL)

**Authentication Endpoints**:

```
POST /api/auth/register
Request:
  Content-Type: application/json
  Body: {
    "email": "user@example.com",
    "password": "securepassword123"
  }
Response: 201 Created
  Body: {
    "id": "uuid",
    "email": "user@example.com",
    "created_at": "2026-01-14T12:00:00Z"
  }
Errors:
  409 Conflict - Email already registered
  422 Unprocessable Entity - Validation error

POST /api/auth/login
Request:
  Content-Type: application/json
  Body: {
    "email": "user@example.com",
    "password": "securepassword123"
  }
Response: 200 OK
  Body: {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
Errors:
  401 Unauthorized - Invalid credentials
  422 Unprocessable Entity - Validation error
```

**Task Endpoints** (all require JWT authentication):

```
GET /api/tasks
Request:
  Headers:
    Authorization: Bearer <token>
Response: 200 OK
  Body: [
    {
      "id": "uuid",
      "user_id": "uuid",
      "title": "Task title",
      "description": "Task description",
      "status": "pending",
      "created_at": "2026-01-14T12:00:00Z",
      "updated_at": "2026-01-14T12:00:00Z"
    }
  ]
Errors:
  401 Unauthorized - Missing/invalid token

POST /api/tasks
Request:
  Headers:
    Authorization: Bearer <token>
  Content-Type: application/json
  Body: {
    "title": "New task",
    "description": "Optional description"
  }
Response: 201 Created
  Body: {
    "id": "uuid",
    "user_id": "uuid",
    "title": "New task",
    "description": "Optional description",
    "status": "pending",
    "created_at": "2026-01-14T12:00:00Z",
    "updated_at": "2026-01-14T12:00:00Z"
  }
Errors:
  401 Unauthorized - Missing/invalid token
  422 Unprocessable Entity - Validation error (empty title)

PUT /api/tasks/{id}
Request:
  Headers:
    Authorization: Bearer <token>
  Content-Type: application/json
  Body: {
    "title": "Updated title",
    "description": "Updated description",
    "status": "completed"
  }
Response: 200 OK
  Body: {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Updated title",
    "description": "Updated description",
    "status": "completed",
    "created_at": "2026-01-14T12:00:00Z",
    "updated_at": "2026-01-14T13:00:00Z"
  }
Errors:
  401 Unauthorized - Missing/invalid token
  403 Forbidden - User doesn't own this task
  404 Not Found - Task doesn't exist
  422 Unprocessable Entity - Validation error

DELETE /api/tasks/{id}
Request:
  Headers:
    Authorization: Bearer <token>
Response: 200 OK
  Body: {
    "message": "Task deleted successfully"
  }
Errors:
  401 Unauthorized - Missing/invalid token
  403 Forbidden - User doesn't own this task
  404 Not Found - Task doesn't exist
```

### 6. Deployment Strategy

**Frontend Deployment (Vercel)**:
- Platform: Vercel (zero-config Next.js deployment)
- Build command: `npm run build`
- Output directory: `.next`
- Environment variables:
  - `NEXT_PUBLIC_API_URL` - Backend API URL
  - `BETTER_AUTH_SECRET` - Auth secret key
- Automatic HTTPS/TLS
- CDN distribution
- Preview deployments for branches

**Backend Deployment (Railway/Render/Fly.io)**:
- Platform: Railway, Render, or Fly.io (containerized)
- Dockerfile for consistent deployment
- Environment variables:
  - `DATABASE_URL` - Neon PostgreSQL connection string
  - `JWT_SECRET_KEY` - JWT signing key
  - `JWT_ALGORITHM` - HS256
  - `ACCESS_TOKEN_EXPIRE_MINUTES` - 1440 (24 hours)
  - `CORS_ORIGINS` - Frontend URL (Vercel domain)
- Health check endpoint: `GET /health`
- Automatic HTTPS/TLS
- Container restart on failure

**Database Deployment (Neon)**:
- Platform: Neon Serverless PostgreSQL
- Managed service (no manual setup)
- Connection pooling enabled
- Automatic backups
- Connection string in environment variable

**Deployment Workflow**:
1. Commit code to git repository
2. Push to GitHub
3. Vercel auto-deploys frontend on push to main
4. Railway/Render auto-deploys backend on push to main
5. Run database migrations: `alembic upgrade head`
6. Verify health checks pass
7. Test deployed application

### 7. Security Considerations

**Password Security**:
- Bcrypt hashing with 12 salt rounds
- Passwords never stored in plain text
- Passwords never returned in API responses
- Minimum 8 characters enforced

**JWT Token Security**:
- HS256 algorithm (symmetric signing)
- Secret key stored in environment variable
- 24-hour expiration
- Tokens include user_id in payload
- Signature verification on every request

**User Isolation**:
- All task queries filtered by user_id
- User_id extracted from JWT token (not request body)
- 403 Forbidden if user attempts to access another user's task
- Database foreign key constraints enforce relationships

**Input Validation**:
- Client-side validation (immediate feedback)
- Server-side validation (security boundary)
- Pydantic schemas validate all input
- SQL injection prevented by SQLModel parameterized queries
- XSS prevented by React's automatic escaping

**CORS Configuration**:
- Restrict to frontend origin only
- Allow credentials (cookies)
- Restrict HTTP methods (GET, POST, PUT, DELETE)
- No wildcard origins in production

**HTTPS/TLS**:
- Required for all communications
- Automatic via Vercel and Railway/Render
- Protects tokens in transit

**Environment Variables**:
- Secrets never committed to git
- `.env` files in `.gitignore`
- Different secrets for dev/staging/production

### 8. Testing Strategy

**Backend Testing (pytest)**:
- Unit tests for auth utilities (JWT, password hashing)
- Unit tests for model validation
- Integration tests for authentication flow
- Integration tests for task CRUD operations
- Test database with SQLite in-memory
- Fixtures for test users and tasks
- Coverage target: 80%+

**Frontend Testing (Jest + React Testing Library)**:
- Component tests for forms (LoginForm, RegisterForm, AddTaskForm)
- Component tests for task display (TaskCard, TaskList)
- Mock API responses
- Test user interactions (form submission, button clicks)
- Test validation errors
- Coverage target: 70%+

**E2E Testing (Playwright - Optional)**:
- Full user journeys (register → login → create task → logout)
- Cross-browser testing (Chrome, Firefox, Safari)
- Mobile responsive testing
- Accessibility testing

**Manual Testing Checklist**:
- Registration with valid/invalid inputs
- Login with correct/incorrect credentials
- Create task with title only and with description
- Update task title, description, status
- Delete task with confirmation
- Logout and verify session cleared
- Token expiration handling
- Responsive design on mobile/tablet/desktop
- Keyboard navigation
- Screen reader compatibility

## Next Steps

1. **Phase 0: Research** - Generate `research.md` with technology decisions and best practices
2. **Phase 1: Design** - Generate `data-model.md`, `contracts/`, and `quickstart.md`
3. **Phase 2: Tasks** - Run `/sp.tasks` to generate implementation task breakdown
4. **Phase 3: Implementation** - Execute tasks using specialized subagents
5. **Phase 4: Deployment** - Deploy to Vercel and Railway/Render
6. **Phase 5: Validation** - Run tests and verify acceptance criteria
