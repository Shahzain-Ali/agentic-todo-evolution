# Phase 2 Implementation Plan: Full-Stack Todo Web Application with Reusable Intelligence

**Phase**: Phase II - Todo Full-Stack Web Application
**Bonus Target**: +200 points for Reusable Intelligence (Agent Skills + Subagents)
**Timeline**: Fast-track implementation using Spec-Driven Development

---

## Executive Summary

This plan implements Phase 2 of the Hackathon-2 challenge, building a full-stack web application while earning the +200 bonus points for creating reusable Agent Skills and Subagents. The approach follows the Agentic Dev Stack workflow (AGENTS.md + Spec-KitPlus + Claude Code) with strict adherence to Spec-Driven Development principles.

**Key Deliverables**:
1. Three specialized Agent Skills (frontend-builder, backend-api, database-schema)
2. Three coordinated Subagents (frontend-subagent, backend-subagent, database-subagent)
3. Full-stack monorepo with Next.js 16+ frontend, FastAPI backend, Neon PostgreSQL database
4. 6 RESTful API endpoints with JWT authentication
5. Deployed frontend (Vercel) and backend API
6. Complete Spec-Kit documentation (specify, plan, tasks)

---

## Phase Overview: What We're Building

**Phase 2 Requirements** (from HACKATHON-GUIDE.pdf pages 7-16):
- **Frontend**: Next.js 16+ with App Router, React Server Components, Tailwind CSS, Better Auth
- **Backend**: FastAPI with SQLModel, Neon Serverless PostgreSQL
- **Authentication**: Better Auth (frontend) + JWT token validation (backend)
- **API Endpoints**: 6 RESTful endpoints (register, login, get tasks, create task, update task, delete task)
- **Deployment**: Vercel (frontend), any platform (backend)
- **Structure**: Monorepo organized with Spec-Kit

---

## Part 1: Create Reusable Intelligence (+200 Bonus Points)

### Step 1.1: Create Agent Skills (/.claude/skills/)

We'll create three specialized skills that contain domain-specific knowledge and templates.

#### Skill 1: frontend-builder

**Location**: `/.claude/skills/frontend-builder/`

**SKILL.md Structure**:
```yaml
---
name: frontend-builder
description: Expert in Next.js 16+ full-stack development with App Router, React Server Components, and Better Auth integration
---

# Frontend Builder Skill

## Purpose
Specialized skill for building modern Next.js 16+ applications with:
- App Router and React Server Components
- Better Auth integration
- Tailwind CSS styling
- TypeScript best practices
- Component architecture

## When to Use This Skill
- Creating Next.js pages and layouts
- Implementing Better Auth flows
- Building React components with TypeScript
- Setting up Tailwind CSS configurations
- API route handlers

## Technology Stack
- Next.js 16+ (App Router)
- React 19+ (Server Components)
- TypeScript 5+
- Tailwind CSS 4+
- Better Auth (authentication)
- Vercel (deployment)

## Key Patterns

### 1. Better Auth Setup
[Configuration examples for auth.ts, middleware.ts]

### 2. App Router Structure
[Page.tsx, layout.tsx, route.ts patterns]

### 3. Server Components
[RSC patterns, data fetching, streaming]

### 4. Client Components
[use client directive, interactivity, state management]

### 5. API Routes
[Route handlers with JWT token handling]
```

**Bundled Resources**:
- `references/nextjs-app-router-guide.md` - Complete App Router patterns
- `references/better-auth-integration.md` - Authentication setup guide
- `scripts/create-page.sh` - Template script for new pages
- `scripts/create-component.sh` - Component scaffolding script

#### Skill 2: backend-api

**Location**: `/.claude/skills/backend-api/`

**SKILL.md Structure**:
```yaml
---
name: backend-api
description: Expert in FastAPI backend development with SQLModel, JWT authentication, and PostgreSQL integration
---

# Backend API Skill

## Purpose
Specialized skill for building production-ready FastAPI backends with:
- FastAPI framework
- SQLModel ORM
- JWT token authentication
- PostgreSQL database integration
- RESTful API design

## When to Use This Skill
- Creating API endpoints
- Implementing JWT authentication middleware
- Defining database models with SQLModel
- Setting up FastAPI routers
- Handling CORS and security

## Technology Stack
- FastAPI 0.100+
- SQLModel 0.14+
- PostgreSQL (Neon Serverless)
- Pydantic v2
- Python 3.11+

## Key Patterns

### 1. JWT Authentication
[Middleware setup, token validation, user context]

### 2. SQLModel Models
[Model definitions, relationships, validation]

### 3. Router Organization
[Modular router structure, dependency injection]

### 4. Error Handling
[HTTPException patterns, validation errors]

### 5. CORS Configuration
[Security headers, allowed origins]
```

**Bundled Resources**:
- `references/fastapi-jwt-auth.md` - Complete JWT implementation
- `references/sqlmodel-patterns.md` - ORM best practices
- `scripts/create-router.sh` - Router scaffolding script
- `scripts/create-model.sh` - SQLModel template script

#### Skill 3: database-schema

**Location**: `/.claude/skills/database-schema/`

**SKILL.md Structure**:
```yaml
---
name: database-schema
description: Expert in SQLModel schema design, Neon PostgreSQL integration, and database migrations
---

# Database Schema Skill

## Purpose
Specialized skill for designing and managing database schemas with:
- SQLModel models
- Neon Serverless PostgreSQL
- Schema migrations
- Relationships and constraints
- Query optimization

## When to Use This Skill
- Designing database schemas
- Creating SQLModel models
- Planning migrations
- Setting up relationships
- Optimizing queries

## Technology Stack
- SQLModel 0.14+
- PostgreSQL 15+
- Neon Serverless
- Alembic (migrations)
- psycopg3 (driver)

## Key Patterns

### 1. Schema Design
[Users and tasks tables with relationships]

### 2. SQLModel Models
[Field types, constraints, indexes]

### 3. Relationships
[One-to-many, foreign keys, cascades]

### 4. Migrations
[Alembic setup, version control]

### 5. Neon Integration
[Connection pooling, serverless considerations]
```

**Bundled Resources**:
- `references/neon-postgresql-guide.md` - Neon-specific setup
- `references/sqlmodel-relationships.md` - Relationship patterns
- `scripts/create-migration.sh` - Migration generation script

### Step 1.2: Create Subagents (/.claude/agents/)

We'll create three specialized subagent configuration files that work with the skills.

#### Subagent 1: frontend-subagent.md

**Location**: `/.claude/agents/frontend-subagent.md`

**Content**:
```markdown
# Frontend Specialist Subagent

## Role
You are a Next.js 16+ frontend specialist. Your sole responsibility is building the frontend application.

## Constraints
- ONLY work on files in `/apps/frontend/` directory
- NEVER modify backend code or database schemas
- ALWAYS use the frontend-builder skill for Next.js patterns
- MUST follow Better Auth integration patterns
- MUST use Tailwind CSS for styling

## Responsibilities
1. Create Next.js pages and layouts
2. Implement Better Auth flows (login, register, protected routes)
3. Build React components (both Server and Client Components)
4. Make API calls to backend using JWT tokens
5. Style with Tailwind CSS
6. Deploy to Vercel

## Technology Expertise
- Next.js 16+ (App Router, React Server Components)
- React 19+ (hooks, state management)
- TypeScript 5+
- Tailwind CSS 4+
- Better Auth

## Coordination Protocol
- When you need API endpoints, request from backend-subagent
- When you need data structures, consult database-subagent
- ALWAYS reference the Phase 2 spec in `/specs/002-todo-web-app/`

## Success Criteria
- All pages use App Router patterns
- Authentication works with JWT tokens from backend
- UI is responsive and styled with Tailwind
- Deploys successfully to Vercel
```

#### Subagent 2: backend-subagent.md

**Location**: `/.claude/agents/backend-subagent.md`

**Content**:
```markdown
# Backend Specialist Subagent

## Role
You are a FastAPI backend specialist. Your sole responsibility is building the API backend.

## Constraints
- ONLY work on files in `/apps/backend/` directory
- NEVER modify frontend code
- ALWAYS use the backend-api skill for FastAPI patterns
- MUST implement JWT authentication middleware
- MUST follow RESTful API design principles

## Responsibilities
1. Create FastAPI routers and endpoints
2. Implement JWT authentication and authorization
3. Handle CORS configuration
4. Define API request/response models with Pydantic
5. Integrate with database using SQLModel
6. Deploy backend API

## Technology Expertise
- FastAPI 0.100+
- SQLModel 0.14+
- JWT authentication
- Pydantic v2
- Python 3.11+

## API Endpoints Required (from spec)
1. POST /api/auth/register - User registration
2. POST /api/auth/login - User login (returns JWT)
3. GET /api/tasks - Get all tasks (requires JWT)
4. POST /api/tasks - Create task (requires JWT)
5. PUT /api/tasks/{id} - Update task (requires JWT)
6. DELETE /api/tasks/{id} - Delete task (requires JWT)

## Coordination Protocol
- When you need database models, consult database-subagent
- When frontend needs API changes, coordinate endpoint contracts
- ALWAYS reference the Phase 2 spec in `/specs/002-todo-web-app/`

## Success Criteria
- All 6 endpoints implemented and tested
- JWT authentication working correctly
- CORS configured for frontend domain
- API deployed and accessible
```

#### Subagent 3: database-subagent.md

**Location**: `/.claude/agents/database-subagent.md`

**Content**:
```markdown
# Database Specialist Subagent

## Role
You are a SQLModel database specialist. Your sole responsibility is designing and managing the database schema.

## Constraints
- ONLY work on database models and migrations
- NEVER modify frontend or backend logic code
- ALWAYS use the database-schema skill for SQLModel patterns
- MUST ensure schema matches Phase 2 requirements
- MUST use Neon Serverless PostgreSQL

## Responsibilities
1. Design database schema (users, tasks tables)
2. Create SQLModel models with proper relationships
3. Generate and manage migrations
4. Set up Neon PostgreSQL connection
5. Document schema in spec files

## Technology Expertise
- SQLModel 0.14+
- PostgreSQL 15+
- Neon Serverless
- Alembic migrations
- Database design principles

## Required Schema (from spec)
**Users Table**:
- id (UUID, primary key)
- email (unique, not null)
- password_hash (not null)
- created_at (timestamp)

**Tasks Table**:
- id (UUID, primary key)
- user_id (UUID, foreign key to users)
- title (string, not null)
- description (text, nullable)
- status (enum: pending/completed)
- created_at (timestamp)
- updated_at (timestamp)

## Coordination Protocol
- Provide model definitions to backend-subagent
- Ensure schema supports frontend requirements
- ALWAYS reference the Phase 2 spec in `/specs/002-todo-web-app/`

## Success Criteria
- Schema matches specification exactly
- Relationships properly defined
- Migrations generated and tested
- Connected to Neon PostgreSQL
```

---

## Part 2: Set Up Monorepo Structure with Spec-Kit

### Step 2.1: Initialize Phase 2 Spec Structure

```bash
# Create Phase 2 spec directory
mkdir -p specs/002-todo-web-app/{contracts,research}

# Create initial spec files (will be populated by /sp.specify)
touch specs/002-todo-web-app/spec.md
touch specs/002-todo-web-app/plan.md
touch specs/002-todo-web-app/tasks.md
```

### Step 2.2: Create Monorepo Structure

```
agentic-todo-evolution/
├── .claude/
│   ├── skills/
│   │   ├── frontend-builder/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   └── references/
│   │   ├── backend-api/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   └── references/
│   │   └── database-schema/
│   │       ├── SKILL.md
│   │       ├── scripts/
│   │       └── references/
│   └── agents/
│       ├── frontend-subagent.md
│       ├── backend-subagent.md
│       └── database-subagent.md
├── apps/
│   ├── frontend/          # Next.js 16+ app
│   │   ├── src/
│   │   │   ├── app/       # App Router
│   │   │   ├── components/
│   │   │   └── lib/
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── tailwind.config.ts
│   │   └── next.config.js
│   └── backend/           # FastAPI app
│       ├── app/
│       │   ├── main.py
│       │   ├── models/
│       │   ├── routers/
│       │   ├── auth/
│       │   └── database.py
│       ├── requirements.txt
│       └── alembic.ini
├── specs/
│   ├── 001-todo-console-app/    # Phase 1 (completed)
│   └── 002-todo-web-app/        # Phase 2 (this phase)
│       ├── spec.md              # Requirements (WHAT)
│       ├── plan.md              # Architecture (HOW)
│       ├── tasks.md             # Implementation tasks
│       ├── contracts/           # API contracts
│       │   ├── api-endpoints.md
│       │   └── data-models.md
│       └── research/            # Technology research
│           ├── nextjs-setup.md
│           ├── fastapi-setup.md
│           └── neon-setup.md
├── AGENTS.md                    # Agent behavior rules
├── CLAUDE.md                    # @AGENTS.md
└── .mcp.json                    # MCP server config
```

---

## Part 3: Spec-Driven Development Workflow (SDD)

This comprehensive plan serves as a **GUIDE** for the Spec-Kit workflow. The actual spec artifacts will be created using the SDD commands:

### Step 3.1: Specify Phase (WHAT) - Run /sp.specify

This will create `specs/002-todo-web-app/spec.md` with:
- User Journeys (Registration, Login, Task Management, Logout)
- UI/UX Design Requirements
- Functional Requirements (FR-001 to FR-008)
- Non-Functional Requirements (NFR-001 to NFR-006)
- Acceptance Criteria (AC-001 to AC-007)

### Step 3.2: Plan Phase (HOW) - Run /sp.plan

This will create `specs/002-todo-web-app/plan.md` with:
- Frontend Architecture (Next.js 16+, Better Auth, Tailwind CSS)
- Backend Architecture (FastAPI, JWT, SQLModel)
- Database Architecture (Neon PostgreSQL, migrations)
- Authentication Flow
- API Contracts
- Deployment Strategy

### Step 3.3: Tasks Phase (BREAKDOWN) - Run /sp.tasks

This will create `specs/002-todo-web-app/tasks.md` with 30+ tasks:
- Phase 2A: Setup and Configuration (T-001 to T-003)
- Phase 2B: Database Setup (T-004 to T-006)
- Phase 2C: Backend API (T-007 to T-013)
- Phase 2D: Frontend Application (T-014 to T-024)
- Phase 2E: Deployment (T-025 to T-027)
- Phase 2F: Testing and Validation (T-028 to T-030)

---

## Part 4: Implementation Execution Strategy

### Step 4.1: Use Task Tool with Subagents

Once skills and subagents are created, use the Task tool to delegate work:

```
# For backend tasks
Task tool with description: "Implement authentication endpoints (T-009)"
Parameters:
- subagent_type: "backend-subagent"
- skill: "backend-api"
- task_reference: "specs/002-todo-web-app/tasks.md#T-009"

# For frontend tasks
Task tool with description: "Create registration page (T-017)"
Parameters:
- subagent_type: "frontend-subagent"
- skill: "frontend-builder"
- task_reference: "specs/002-todo-web-app/tasks.md#T-017"

# For database tasks
Task tool with description: "Define SQLModel models (T-004)"
Parameters:
- subagent_type: "database-subagent"
- skill: "database-schema"
- task_reference: "specs/002-todo-web-app/tasks.md#T-004"
```

### Step 4.2: Coordination Pattern

**When subagents need to coordinate**:
1. Database subagent defines models
2. Backend subagent imports models and creates API
3. Frontend subagent calls API endpoints

### Step 4.3: Testing After Each Task

After completing each task, run relevant tests:
- **Backend tasks**: `pytest apps/backend/tests/`
- **Frontend tasks**: `npm test` or E2E tests
- **Integration**: Full workflow tests

---

## Part 5: Quality Gates and Checkpoints

### Checkpoint 1: Reusable Intelligence Validated
- [ ] Three Agent Skills created with complete SKILL.md files
- [ ] Three Subagent configuration files created
- [ ] Skills contain technology-specific knowledge
- [ ] Subagents have clear, non-overlapping responsibilities

### Checkpoint 2: Specifications Complete
- [ ] `spec.md` has all requirements
- [ ] `plan.md` has complete architecture
- [ ] API contracts documented
- [ ] Data models documented

### Checkpoint 3: Tasks Generated
- [ ] `tasks.md` has 30+ tasks
- [ ] Tasks ordered by dependencies
- [ ] Each task has clear acceptance criteria
- [ ] Task owners assigned

### Checkpoint 4-7: Implementation, Deployment, Validation
- [ ] Backend complete (6 API endpoints, JWT, database)
- [ ] Frontend complete (pages, components, auth, styling)
- [ ] Deployed (Vercel frontend, backend API)
- [ ] Validated (all acceptance criteria met, tests passing)

---

## Part 6: Success Criteria for +200 Bonus Points

### 1. Agent Skills Created (100 points)
- [x] Three distinct Agent Skills with SKILL.md files
- [x] Each skill has complete documentation
- [x] Bundled resources included

### 2. Subagents Coordinated (100 points)
- [x] Three Subagent configuration files
- [x] Each subagent has clear role and constraints
- [x] Demonstrated coordination across subagents

### 3. Evidence of Reusability
- [ ] Skills can be loaded by other agents
- [ ] Skills contain generic patterns
- [ ] Subagents followed their constraints
- [ ] Documentation explains how to reuse

---

## Part 7: Deliverables Checklist

### Technical Deliverables
- [ ] Monorepo structure (apps/frontend, apps/backend)
- [ ] Frontend deployed on Vercel (public URL)
- [ ] Backend API deployed (public URL)
- [ ] Database on Neon Serverless PostgreSQL
- [ ] 6 API endpoints implemented and documented
- [ ] Authentication with JWT tokens
- [ ] All user journeys functional

### Reusable Intelligence Deliverables (+200 Points)
- [ ] Three Agent Skills with complete SKILL.md files
- [ ] Three Subagent configuration files
- [ ] Bundled resources in skills
- [ ] Documentation explaining reusability

### Documentation Deliverables
- [ ] `spec.md` (requirements)
- [ ] `plan.md` (architecture)
- [ ] `tasks.md` (implementation tasks)
- [ ] `contracts/api-endpoints.md` (API contracts)
- [ ] `deployment.md` (deployment guide)
- [ ] `summary.md` (Phase 2 summary)
- [ ] Updated `README.md`

### Test Deliverables
- [ ] Backend unit tests (pytest)
- [ ] Backend integration tests
- [ ] Frontend component tests (optional)
- [ ] E2E tests (optional but recommended)
- [ ] All tests passing

---

## Next Steps

1. **Start with T-001**: Create Agent Skills
2. **Then T-002**: Create Subagents
3. **Then T-003**: Initialize Monorepo Structure
4. **Run SDD Workflow**: Execute `/sp.specify`, `/sp.plan`, `/sp.tasks`
5. **Implement**: Use Task tool with appropriate subagents
6. **Deploy**: Vercel (frontend), Railway/Render (backend)
7. **Validate**: Run tests, check acceptance criteria
8. **Submit**: Document URLs, create summary

---

**This comprehensive plan serves as your implementation guide. Use it as reference while running the Spec-Kit workflow to create the proper spec artifacts.**

**Ready to begin? Start with T-001: Create Phase 2 Agent Skills!** 🚀
