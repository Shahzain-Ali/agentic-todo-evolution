# AGENTS.md

## Purpose

This project uses **Spec-Driven Development (SDD)** — a workflow where **no agent is allowed to write code until the specification is complete and approved**.

All AI agents must follow the **Spec-Kit lifecycle**:

> **Specify → Plan → Tasks → Implement**

This prevents "vibe coding," ensures alignment across agents, and guarantees that every implementation step maps back to an explicit requirement.

---

## Project Context: 5-Phase Todo Application

This is a hackathon project building a Todo application across 5 progressive phases:

- **Phase I**: Todo In-Memory Python Console App ✅ (Completed)
- **Phase II**: Todo Full-Stack Web Application 🔄 (In Progress)
- **Phase III**: Todo AI Chatbot (Upcoming)
- **Phase IV**: Local Kubernetes Deployment (Upcoming)
- **Phase V**: Advanced Cloud Deployment (Upcoming)

Each phase builds upon the previous one, following the same SDD workflow.

---

## How Agents Must Work

Every agent in this project MUST obey these rules:

### 1. **Never generate code without a referenced Task ID**
Every code change must trace back to a specific task in `specs/<feature>/tasks.md`.

### 2. **Never modify architecture without updating the plan**
All architectural changes must be reflected in `specs/<feature>/plan.md`.

### 3. **Never propose features without updating the spec**
New features require updates to `specs/<feature>/spec.md` (WHAT).

### 4. **Never change principles without updating the constitution**
Core principles are defined in `.specify/memory/constitution.md`.

### 5. **Every code file must contain a comment linking it to the Task and Spec sections**
Example:
```python
# Task: T-001 | Spec: §2.1 | Plan: §3.4
# Purpose: Implement task creation with validation
```

### 6. **If an agent cannot find the required spec, it must STOP and request it**
Never improvise. Never assume. Always verify against the spec.

---

## Spec-Kit Workflow (Source of Truth)

### 1. Constitution (WHY — Principles & Constraints)

**File**: `.specify/memory/constitution.md`

Defines the project's non-negotiables:
- Architecture values
- Security rules
- Tech stack constraints
- Performance expectations
- Testing requirements
- Patterns allowed/forbidden

**Agent Responsibility**: Check this before proposing solutions.

---

### 2. Specify (WHAT — Requirements, Journeys & Acceptance Criteria)

**File**: `specs/<feature>/spec.md`

Contains:
- User journeys
- Requirements
- Acceptance criteria
- Domain rules
- Business constraints
- Success metrics

**Agent Responsibility**: Do not infer missing requirements — request clarification or propose specification updates.

**MCP Command**: `/sp.specify` or `sp.specify` (via MCP)

---

### 3. Plan (HOW — Architecture, Components, Interfaces)

**File**: `specs/<feature>/plan.md`

Includes:
- Component breakdown
- APIs & schema diagrams
- Service boundaries
- System responsibilities
- High-level sequencing
- Technology choices
- Data flow diagrams

**Agent Responsibility**: All architectural output MUST be generated from the Specify file.

**MCP Command**: `/sp.plan` or `sp.plan` (via MCP)

---

### 4. Tasks (BREAKDOWN — Atomic, Testable Work Units)

**File**: `specs/<feature>/tasks.md`

Each Task must contain:
- Task ID (e.g., T-001, T-002)
- Clear description
- Preconditions
- Expected outputs
- Artifacts to modify
- Test cases
- Links back to Specify + Plan sections

**Agent Responsibility**: Implement only what these tasks define.

**MCP Command**: `/sp.tasks` or `sp.tasks` (via MCP)

---

### 5. Implement (CODE — Write Only What the Tasks Authorize)

Agents now write code, but must:
- Reference Task IDs in comments
- Follow the Plan exactly
- Not invent new features or flows
- Stop and request clarification if anything is underspecified
- Run tests after each task
- Update documentation

**Agent Responsibility**: The golden rule: **No task = No code.**

**MCP Command**: `/sp.implement` or `sp.implement` (via MCP)

---

## Agent Behavior in This Project

### When generating code:

```python
# [Task]: T-001
# [From]: specs/002-todo-web-app/spec.md §2.1, plan.md §3.4
# [Purpose]: Implement user authentication endpoint
```

### When proposing architecture:

```
⚠️ Update required in specs/<feature>/plan.md → add component X
Reason: [explain why this component is needed]
```

### When proposing new behavior or a new feature:

```
⚠️ Requires update in specs/<feature>/spec.md (WHAT)
Reason: [explain the new requirement]
```

### When changing principles:

```
⚠️ Modify .specify/memory/constitution.md → Principle #X
Reason: [explain why this principle needs to change]
```

---

## Agent Failure Modes (What Agents MUST Avoid)

Agents are NOT allowed to:

❌ Freestyle code or architecture
❌ Generate missing requirements
❌ Create tasks on their own
❌ Alter stack choices without justification
❌ Add endpoints, fields, or flows that aren't in the spec
❌ Ignore acceptance criteria
❌ Produce "creative" implementations that violate the plan
❌ Skip tests
❌ Commit code without running tests
❌ Hardcode secrets or credentials
❌ Refactor unrelated code

**Hierarchy**: Constitution > Specify > Plan > Tasks > Code

---

## MCP Tools Available

This project uses MCP (Model Context Protocol) to expose Spec-Kit commands:

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `sp.specify` | Create/update feature specification | Starting a new feature or phase |
| `sp.plan` | Generate architectural plan | After spec is approved |
| `sp.tasks` | Break down plan into tasks | After plan is approved |
| `sp.implement` | Execute tasks and write code | After tasks are approved |
| `sp.clarify` | Ask clarifying questions about spec | When requirements are unclear |
| `sp.analyze` | Analyze cross-artifact consistency | After generating tasks |
| `sp.adr` | Create Architectural Decision Record | For significant architectural decisions |
| `sp.phr` | Create Prompt History Record | After completing any work |
| `sp.git.commit_pr` | Commit and create PR | After implementation is complete |
| `sp.constitution` | Update project constitution | When principles need to change |
| `sp.checklist` | Generate custom checklist | For validation and testing |
| `sp.reverse-engineer` | Reverse engineer codebase | Understanding existing code |
| `sp.taskstoissues` | Convert tasks to GitHub issues | For project management |

**Important**: Always use MCP commands instead of manually creating/editing spec files.

---

## Phase-Specific Guidelines

### Phase I: Console App (Completed ✅)
- **Tech Stack**: Python 3.13+, built-in libraries only
- **Storage**: In-memory (lists/dictionaries)
- **Focus**: Core CRUD operations, CLI interface
- **Location**: `src/todo/`, `specs/001-todo-console-app/`

### Phase II: Full-Stack Web App (In Progress 🔄)
- **Tech Stack**:
  - Backend: FastAPI, SQLModel, Alembic
  - Frontend: Next.js 15, React 19, TypeScript, Tailwind CSS
  - Database: Neon Serverless PostgreSQL 15+
  - Auth: Better Auth with JWT
- **Focus**: REST API, authentication, persistent storage, web UI
- **Location**: `apps/backend/`, `apps/frontend/`, `specs/002-todo-web-app/`

### Phase III: AI Chatbot (Upcoming)
- **Tech Stack**: TBD (likely Claude API, LangChain)
- **Focus**: Natural language interaction with Todo system
- **Location**: `specs/003-todo-ai-chatbot/`

### Phase IV: Local Kubernetes (Upcoming)
- **Tech Stack**: Minikube, Helm, kubectl-ai, Docker Desktop
- **Focus**: Container orchestration, local deployment
- **Location**: `specs/004-todo-k8s-local/`

### Phase V: Cloud Deployment (Upcoming)
- **Tech Stack**: TBD (AWS/GCP/Azure)
- **Focus**: Production-grade deployment, monitoring, scaling
- **Location**: `specs/005-todo-cloud/`

---

## Developer–Agent Alignment

Humans and agents collaborate, but the **spec is the single source of truth**.

### Before Every Session

Agents should re-read:
1. `.specify/memory/constitution.md` (project principles)
2. `AGENTS.md` (this file - workflow rules)
3. `specs/<current-feature>/spec.md` (current requirements)
4. `specs/<current-feature>/plan.md` (current architecture)
5. `specs/<current-feature>/tasks.md` (current tasks)

### During Development

1. **Start with Spec**: Always begin with `/sp.specify`
2. **Plan Architecture**: Run `/sp.plan` after spec approval
3. **Break Down Tasks**: Run `/sp.tasks` after plan approval
4. **Implement**: Run `/sp.implement` to execute tasks
5. **Test**: Run tests after each task
6. **Document**: Create PHR with `/sp.phr`
7. **Commit**: Use `/sp.git.commit_pr` for version control

### After Completion

1. **Validate**: Check all acceptance criteria
2. **Test**: Run full test suite
3. **Document**: Update README, API docs
4. **Record**: Create PHR and ADR if needed
5. **Review**: Get human approval before merging

---

## Testing Requirements

All code must follow Test-Driven Development (TDD):

1. **Write Tests First**: Before implementing any feature
2. **Red-Green-Refactor**:
   - Red: Write failing test
   - Green: Make test pass with minimal code
   - Refactor: Improve code while keeping tests green
3. **Test Coverage**: Minimum 80% coverage
4. **Test Types**:
   - Unit tests: Test individual functions/methods
   - Integration tests: Test component interactions
   - E2E tests: Test full user journeys

**Location**: `tests/unit/`, `tests/integration/`, `tests/e2e/`

---

## Security Requirements

1. **Never commit secrets**: Use `.env` files (gitignored)
2. **Validate all inputs**: Prevent injection attacks
3. **Use parameterized queries**: Prevent SQL injection
4. **Hash passwords**: Use bcrypt or similar
5. **Implement CORS**: Restrict origins in production
6. **Use HTTPS**: In production environments
7. **Rate limiting**: Prevent abuse
8. **Authentication**: JWT tokens with expiration
9. **Authorization**: Role-based access control

---

## Code Quality Standards

1. **Type Hints**: Use Python type hints everywhere
2. **Docstrings**: Document all public functions/classes
3. **Linting**: Pass ruff/pylint checks
4. **Formatting**: Use black/prettier
5. **Naming**: Clear, descriptive names
6. **DRY**: Don't Repeat Yourself
7. **SOLID**: Follow SOLID principles
8. **Error Handling**: Explicit error handling, no silent failures
9. **Logging**: Use structured logging
10. **Comments**: Explain WHY, not WHAT

---

## Git Workflow

1. **Branch Naming**: `feature/<feature-name>`, `fix/<bug-name>`
2. **Commit Messages**:
   - Format: `<type>: <description>`
   - Types: feat, fix, docs, test, refactor, chore
   - Example: `feat: add user authentication endpoint`
3. **Pull Requests**:
   - Link to spec/task
   - Include test results
   - Request review
4. **Co-Authoring**: Always include Claude in commits:
   ```
   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   ```

---

## Communication Protocol

### Agent → Human

- **Ask Questions**: When requirements are unclear
- **Propose Options**: When multiple approaches exist
- **Report Progress**: After completing tasks
- **Flag Risks**: When detecting potential issues
- **Request Approval**: Before major changes

### Human → Agent

- **Provide Context**: Share domain knowledge
- **Make Decisions**: Choose between options
- **Approve Specs**: Review and approve specifications
- **Validate Output**: Test and verify implementations
- **Give Feedback**: Improve agent performance

---

## Prompt History Records (PHR)

After every significant interaction, create a PHR:

**Command**: `/sp.phr` or `sp.phr`

**Location**: `history/prompts/<feature-name>/` or `history/prompts/general/`

**Purpose**:
- Track all user inputs and agent responses
- Create learning history
- Enable traceability
- Support debugging

**Format**: See `.specify/templates/phr-template.prompt.md`

---

## Architectural Decision Records (ADR)

For significant architectural decisions, create an ADR:

**Command**: `/sp.adr <decision-title>`

**Location**: `history/adr/`

**When to Create**:
- Choosing frameworks/libraries
- Designing data models
- Selecting deployment strategies
- Implementing security patterns
- Making performance tradeoffs

**Format**: See `.specify/templates/adr-template.md`

---

## Success Criteria

An agent is successful when:

✅ All code traces back to approved specs
✅ All tests pass
✅ All acceptance criteria met
✅ No security vulnerabilities
✅ Code follows quality standards
✅ Documentation is complete
✅ PHR is created
✅ ADR is created (if applicable)
✅ Human approves the output

---

## Emergency Protocols

### When Stuck

1. **Stop**: Don't guess or improvise
2. **Review**: Re-read spec, plan, tasks
3. **Ask**: Request clarification from human
4. **Document**: Record the blocker in PHR

### When Spec is Incomplete

1. **Identify Gaps**: List missing requirements
2. **Ask Questions**: Use `/sp.clarify`
3. **Propose Updates**: Suggest spec additions
4. **Wait for Approval**: Don't proceed without approval

### When Tests Fail

1. **Analyze**: Understand the failure
2. **Fix**: Correct the implementation
3. **Verify**: Re-run tests
4. **Document**: Record the fix in PHR

### When Conflicts Arise

1. **Hierarchy**: Constitution > Spec > Plan > Tasks
2. **Escalate**: Ask human to resolve
3. **Document**: Record the conflict and resolution

---

## Summary

This project follows a strict Spec-Driven Development workflow:

1. **No code without specs**
2. **No specs without approval**
3. **No tasks without plans**
4. **No plans without requirements**
5. **No requirements without validation**

**The spec is the single source of truth. Always.**

---

**Version**: 1.0.0
**Last Updated**: 2026-01-22
**Maintained By**: Project Team
**Questions?**: Ask the human or consult the hackathon guide
