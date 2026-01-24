---
name: hackathon-2
description: Guide for building a 5-phase Todo application using the Agentic Dev Stack workflow (AGENTS.md + Spec-KitPlus + Claude Code). MUST be read before starting each phase.
---

# Hackathon-2: 5-Phase Todo Application

## ⚠️ CRITICAL: Read This Before Starting ANY Phase

**This skill MUST be activated and read completely before beginning each phase.**

When user says:
- "Start Phase I" / "Begin Phase 1" / "Let's do Phase I"
- "Start Phase II" / "Begin Phase 2" / "Let's do Phase II"
- (Similar for Phase III, IV, V)

**Claude MUST**:
1. ✅ Read this entire SKILL.md file
2. ✅ **READ HACKATHON-GUIDE.pdf** (47-page reference guide in this folder)
3. ✅ Confirm phase-specific requirements below
4. ✅ Verify Agentic Dev Stack is set up
5. ✅ Follow the SDD workflow (Specify → Plan → Tasks → Implement)
6. ✅ **NEVER write code without approved specs**

---

## Overview

Build a complete Todo application across 5 progressive phases using the **Agentic Dev Stack** workflow. This skill guides you through a professional, spec-driven engineering pipeline where **no code is written until specifications are complete and approved**.

## 5 Development Phases

### Phase I: Todo In-Memory Python Console App
Basic console application with in-memory storage for learning core concepts.

### Phase II: Todo Full-Stack Web Application
Expand to a full web stack with persistent storage and frontend interface.

### Phase III: Todo AI Chatbot
Integrate AI capabilities for natural language interaction with the Todo system.

### Phase IV: Local Kubernetes Deployment
Deploy locally using Minikube, Helm Charts, kubectl-ai, Kagent, Docker Desktop, and Gordon.

### Phase V: Advanced Cloud Deployment
Production-grade cloud deployment with scalability and monitoring.

---

## The Agentic Dev Stack Workflow

This workflow integrates three key components:

| Component | Role | Responsibility |
|-----------|------|----------------|
| **AGENTS.md** | The Brain | Cross-agent truth. Defines how agents should behave, what tools to use, and coding standards. |
| **Spec-KitPlus** | The Architect | Manages spec artifacts (.specify, .plan, .tasks). Ensures technical rigor before coding starts. |
| **Claude Code** | The Executor | The agentic environment. Reads the project memory and executes Spec-Kit tools via MCP. |

**Key Principle**: Claude reads AGENTS.md via CLAUDE.md and interacts with Spec-KitPlus. Every line of code maps back to a validated task.

---

## Step 1: Initialize Spec-KitPlus

Scaffold the spec-driven structure in your project root:

```bash
uv specifyplus init <project_name>
```

This enables the core pipeline:
- `/specify` → Captures requirements in speckit.specify
- `/plan` → Generates the technical approach in speckit.plan
- `/tasks` → Breaks the plan into actionable speckit.tasks
- `/implement` → Executes the code changes

---

## Step 2: Create a Spec-Aware AGENTS.md

Create `AGENTS.md` in your root. This file teaches all AI agents how to use your Spec-Kit workflow.

```markdown
# AGENTS.md

## Purpose

This project uses **Spec-Driven Development (SDD)** — a workflow where **no agent is allowed to write code until the specification is complete and approved**.

All AI agents must follow the **Spec-Kit lifecycle**:

> **Specify → Plan → Tasks → Implement**

This prevents "vibe coding," ensures alignment across agents, and guarantees that every implementation step maps back to an explicit requirement.

---

## How Agents Must Work

Every agent in this project MUST obey these rules:

1. **Never generate code without a referenced Task ID.**
2. **Never modify architecture without updating `speckit.plan`.**
3. **Never propose features without updating `speckit.specify` (WHAT).**
4. **Never change approach without updating `speckit.constitution` (Principles).**
5. **Every code file must contain a comment linking it to the Task and Spec sections.**

If an agent cannot find the required spec, it must **stop and request it**, not improvise.

---

## Spec-Kit Workflow (Source of Truth)

### 1. Constitution (WHY — Principles & Constraints)

**File**: `speckit.constitution`

Defines the project's non-negotiables: architecture values, security rules, tech stack constraints, performance expectations, and patterns allowed.

Agents must check this before proposing solutions.

---

### 2. Specify (WHAT — Requirements, Journeys & Acceptance Criteria)

**File**: `speckit.specify`

Contains:
- User journeys
- Requirements
- Acceptance criteria
- Domain rules
- Business constraints

Agents must not infer missing requirements — they must request clarification or propose specification updates.

---

### 3. Plan (HOW — Architecture, Components, Interfaces)

**File**: `speckit.plan`

Includes:
- Component breakdown
- APIs & schema diagrams
- Service boundaries
- System responsibilities
- High-level sequencing

All architectural output MUST be generated from the Specify file.

---

### 4. Tasks (BREAKDOWN — Atomic, Testable Work Units)

**File**: `speckit.tasks`

Each Task must contain:
- Task ID
- Clear description
- Preconditions
- Expected outputs
- Artifacts to modify
- Links back to Specify + Plan sections

Agents **implement only what these tasks define**.

---

### 5. Implement (CODE — Write Only What the Tasks Authorize)

Agents now write code, but must:
- Reference Task IDs
- Follow the Plan exactly
- Not invent new features or flows
- Stop and request clarification if anything is underspecified

> **The golden rule: No task = No code.**

---

## Agent Behavior in This Project

### When generating code:

```
[Task]: T-001
[From]: speckit.specify §2.1, speckit.plan §3.4
```

### When proposing architecture:

```
Update required in speckit.plan → add component X
```

### When proposing new behavior or a new feature:

```
Requires update in speckit.specify (WHAT)
```

### When changing principles:

```
Modify constitution.md → Principle #X
```

---

## Agent Failure Modes (What Agents MUST Avoid)

Agents are NOT allowed to:
- Freestyle code or architecture
- Generate missing requirements
- Create tasks on their own
- Alter stack choices without justification
- Add endpoints, fields, or flows that aren't in the spec
- Ignore acceptance criteria
- Produce "creative" implementations that violate the plan

**Hierarchy**: Constitution > Specify > Plan > Tasks

---

## Developer–Agent Alignment

Humans and agents collaborate, but the **spec is the single source of truth**.

Before every session, agents should re-read:
1. `.memory/constitution.md`

This ensures predictable, deterministic development.
```

---

## Step 3: Wire Spec-KitPlus into Claude via MCP

Set up an MCP server to let Claude Code run Spec-KitPlus commands.

### 3.1 Install SpecKitPlus and Create MCP Server

```bash
uv init specifyplus <project_name>
```

1. Create your Constitution
2. Add Anthropic's official MCP Builder Skill
3. Using SDD Loop (Specify, Plan, Tasks, Implement), set up an MCP server with prompts present in `.claude/commands`

**Prompt for MCP Setup**:
```
We have specifyplus commands on @.claude/commands/**
Each command takes user input and updates its prompt variable before sending it to the agent.
Now you will use your mcp builder skill and create an mcp server where these commands are available as prompts.

Goal: Now we can run this MCP server and connect with any agent and IDE.
```

4. Test the MCP server

### 3.2 Register with Claude Code

Add the server to your Claude Code config (`.mcp.json` at your project root):

```json
{
  "mcpServers": {
    "spec-kit": {
      "command": "spec-kitplus-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

**Success**: After running MCP Server and connecting it with Claude Code, the same commands are available as MCP prompts.

---

## Step 4: Connect Claude Code via the "Shim"

Copy the default `CLAUDE.md` file and integrate the content within `AGENTS.md`.

Create `CLAUDE.md` in your root:

```markdown
@AGENTS.md
```

This "forwarding" ensures Claude Code loads your comprehensive agent instructions into its context window immediately upon startup.

---

## Step 5: The Day-to-Day Workflow

Once configured, your interaction with Claude Code:

1. **Context Loading**: Start Claude Code. It reads `CLAUDE.md` → `AGENTS.md` and realizes it must use Spec-Kit.

2. **Spec Generation**:
   - User: "I need a project dashboard."
   - Claude: Calls `speckit_specify` and `speckit_plan` using the MCP.

3. **Task Breakdown**:
   - Claude: Calls `speckit_tasks` to create a checklist in `speckit.tasks`.

4. **Implementation**:
   - User: "Execute the first two tasks."
   - Claude: Calls `speckit_implement`, writes the code, and checks it against `speckit.constitution`.

---

## Constitution vs. AGENTS.md: The Difference

**AGENTS.md (The "How")**:
- Focuses on the interaction
- "Use these tools, follow this order, use these CLI commands."

**speckit.constitution (The "What")**:
- Focuses on standards
- "We prioritize performance over brevity, we use async/await, we require 90% test coverage."

---

## Summary of Integration

1. **Initialize**: `specify init` creates the structure
2. **Instruct**: `AGENTS.md` defines the rules
3. **Bridge**: `CLAUDE.md` (@AGENTS.md) connects the agent
4. **Empower**: MCP gives the agent the tools to execute

---

## Execution for Each Phase

For each of the 5 phases (I–V):

1. Run `/specify` with phase requirements
2. Run `/plan` to architect the phase
3. Run `/tasks` to break down implementation
4. Run `/implement` to build the phase
5. Validate against constitution and acceptance criteria
6. Move to next phase

**Good luck, and may your specs be clear and your code be clean!**
