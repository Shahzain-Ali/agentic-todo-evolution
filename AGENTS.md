# AGENTS.md

## Purpose

This project uses **Spec-Driven Development (SDD)** — a workflow where **no agent is allowed to write code until the specification is complete and approved**.

All AI agents (Claude, Copilot, Gemini, local LLMs, etc.) must follow the **Spec-Kit lifecycle**:

> **Specify → Plan → Tasks → Implement**

This prevents "vibe coding," ensures alignment across agents, and guarantees that every implementation step maps back to an explicit requirement.

---

## How Agents Must Work

Every agent in this project MUST obey these rules:

1. **Never generate code without a referenced Task ID.**
2. **Never modify architecture without updating `specs/<feature>/plan.md`.**
3. **Never propose features without updating `specs/<feature>/spec.md` (WHAT).**
4. **Never change approach without updating `.specify/memory/constitution.md` (Principles).**
5. **Every code file must contain a comment linking it to the Task and Spec sections.**

If an agent cannot find the required spec, it must **stop and request it**, not improvise.

---

## Spec-Kit Workflow (Source of Truth)

### 1. Constitution (WHY — Principles & Constraints)

**File**: `.specify/memory/constitution.md`

Defines the project's non-negotiables: architecture values, security rules, tech stack constraints, performance expectations, and patterns allowed.

Agents must check this before proposing solutions.

---

### 2. Specify (WHAT — Requirements, Journeys & Acceptance Criteria)

**File**: `specs/<feature>/spec.md`

Contains:
* User journeys
* Requirements
* Acceptance criteria
* Domain rules
* Business constraints

Agents must not infer missing requirements — they must request clarification or propose specification updates.

---

### 3. Plan (HOW — Architecture, Components, Interfaces)

**File**: `specs/<feature>/plan.md`

Includes:
* Component breakdown
* APIs & schema diagrams
* Service boundaries
* System responsibilities
* High-level sequencing

All architectural output MUST be generated from the Specify file.

---

### 4. Tasks (BREAKDOWN — Atomic, Testable Work Units)

**File**: `specs/<feature>/tasks.md`

Each Task must contain:
* Task ID
* Clear description
* Preconditions
* Expected outputs
* Artifacts to modify
* Links back to Specify + Plan sections

Agents **implement only what these tasks define**.

---

### 5. Implement (CODE — Write Only What the Tasks Authorize)

Agents now write code, but must:
* Reference Task IDs
* Follow the Plan exactly
* Not invent new features or flows
* Stop and request clarification if anything is underspecified

> The golden rule: **No task = No code.**

---

## Agent Behavior in This Project

### When generating code:

Agents must reference:

```
[Task]: T-001
[From]: specs/<feature>/spec.md §2.1, specs/<feature>/plan.md §3.4
```

### When proposing architecture:

Agents must reference:

```
Update required in specs/<feature>/plan.md → add component X
```

### When proposing new behavior or a new feature:

Agents must reference:

```
Requires update in specs/<feature>/spec.md (WHAT)
```

### When changing principles:

Agents must reference:

```
Modify .specify/memory/constitution.md → Principle #X
```

---

## Agent Failure Modes (What Agents MUST Avoid)

Agents are NOT allowed to:

* Freestyle code or architecture
* Generate missing requirements
* Create tasks on their own
* Alter stack choices without justification
* Add endpoints, fields, or flows that aren't in the spec
* Ignore acceptance criteria
* Produce "creative" implementations that violate the plan

If a conflict arises between spec files, the **Constitution > Specify > Plan > Tasks** hierarchy applies.

---

## Developer–Agent Alignment

Humans and agents collaborate, but the **spec is the single source of truth**.

Before every session, agents should re-read:

1. `.specify/memory/constitution.md`

This ensures predictable, deterministic development.

---

## Available Tools & Commands

This project provides specialized commands and sub-agents to help you follow the Spec-Kit workflow efficiently.

### Spec-Kit Commands (`.claude/commands/`)

These commands guide you through the SDD lifecycle:

#### 1. Specification Phase
- **`/sp.specify`** - Create or update feature specification (`specs/<feature>/spec.md`)
- **`/sp.clarify`** - Identify underspecified areas and ask targeted clarification questions
- **`/sp.constitution`** - Create or update project constitution (`.specify/memory/constitution.md`)

#### 2. Planning Phase
- **`/sp.plan`** - Generate architectural plan from specification (`specs/<feature>/plan.md`)
- **`/sp.adr`** - Create Architectural Decision Records for significant decisions (`history/adr/`)

#### 3. Task Breakdown Phase
- **`/sp.tasks`** - Generate actionable, dependency-ordered tasks (`specs/<feature>/tasks.md`)
- **`/sp.taskstoissues`** - Convert tasks to GitHub issues
- **`/sp.checklist`** - Generate custom checklist for current feature

#### 4. Implementation Phase
- **`/sp.implement`** - Execute implementation plan by processing tasks
- **`/sp.git.commit_pr`** - Intelligently execute git workflows (commit + PR)

#### 5. Analysis & Documentation
- **`/sp.analyze`** - Cross-artifact consistency analysis (spec, plan, tasks)
- **`/sp.phr`** - Record Prompt History Record for learning and traceability
- **`/sp.reverse-engineer`** - Reverse engineer codebase into SDD-RI artifacts

### Specialized Sub-Agents (`.claude/agents/`)

When working on specific tech stack layers, these sub-agents provide specialized knowledge:

- **`backend-subagent.md`** - Python, FastAPI, SQLModel, Alembic expertise
- **`frontend-subagent.md`** - Next.js, React, TypeScript, Tailwind CSS expertise
- **`database-subagent.md`** - PostgreSQL, Neon Serverless, data modeling expertise

### Skills (`.claude/skills/`)

- **`hackathon-2`** - 5-Phase Todo Application guide (must read before each phase)
- **`backend-api`** - Backend API development patterns
- **`database-schema`** - Database schema design patterns
- **`frontend-builder`** - Frontend component building patterns
- **`skill-generator`** - Guide for creating new skills

### How to Use These Tools

1. **Starting a new feature**: Run `/sp.specify` to create specification
2. **Planning architecture**: Run `/sp.plan` to generate technical plan
3. **Breaking down work**: Run `/sp.tasks` to create actionable tasks
4. **Implementing**: Run `/sp.implement` to execute tasks with proper references
5. **Documenting decisions**: Run `/sp.adr` when architectural choices are made
6. **Recording work**: Run `/sp.phr` to document AI interactions
7. **Git workflow**: Run `/sp.git.commit_pr` to commit and create PR

### Example Workflow

```bash
# Phase start
/sp.specify "Add user authentication feature"

# Review and approve spec, then plan
/sp.plan

# Review and approve plan, then create tasks
/sp.tasks

# Implement tasks
/sp.implement

# Document significant decisions
/sp.adr "JWT vs Session-based Authentication"

# Record the work
/sp.phr

# Commit and create PR
/sp.git.commit_pr
```

Reply Me:Roman urdu

---

**Version**: 1.0.0
**Last Updated**: 2026-01-24
**Maintained By**: Project Team
