# Implementation Plan: Console Todo Application

**Branch**: `001-todo-console-app` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a command-line todo application with in-memory storage supporting five core operations: add tasks with title/description, view all tasks with status indicators, mark tasks complete/incomplete, update task details, and delete tasks by ID. The application will use Python 3.13+ with UV for package management, following clean code principles and proper project structure. Data persists only during runtime (lost on application exit). The focus is on providing immediate user feedback, clear error messages, and intuitive command-line interactions.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (built-in libraries only for Phase I)
**Storage**: In-memory (Python lists/dictionaries)
**Testing**: pytest
**Target Platform**: Cross-platform console (Linux, macOS, Windows)
**Project Type**: Single console application
**Performance Goals**: Instant response (<1 second) for all operations regardless of list size
**Constraints**: Single-user usage, no data persistence, command-line–readable output, and a clean, visually appealing interface.
**Scale/Scope**: Small-scale console app (~500-1000 LOC), support for hundreds of tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: Constitution file not yet created for this project. The following principles will guide development:

### Proposed Principles for Phase I:

1. **Simplicity First**: Use only built-in Python libraries; no external dependencies except development tools (pytest, UV)
2. **Clean Code**: Follow PEP 8 style guide; clear function names; single responsibility principle
3. **Test-Driven Development**: Write tests before implementation; aim for >80% code coverage
4. **User-Centric Error Handling**: All errors provide clear, actionable messages; no stack traces exposed to users
5. **Idempotent Operations**: Operations can be repeated safely; clear confirmation/error feedback for all actions

**Status**: ✅ No violations - Phase I aligns with proposed principles

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command - CLI command contracts)
├── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
└── checklists/
    └── requirements.md  # Spec quality checklist (completed)
```

### Source Code (repository root)

```text
src/
├── todo/
│   ├── __init__.py
│   ├── models.py        # Todo entity and TodoList collection
│   ├── storage.py       # In-memory storage manager
│   ├── operations.py    # CRUD operations logic
│   ├── cli.py           # Command-line interface and user interactions
│   ├── validators.py    # Input validation logic
│   └── formatters.py    # Output formatting for display
└── main.py              # Application entry point

tests/
├── unit/
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_operations.py
│   ├── test_validators.py
│   └── test_formatters.py
├── integration/
│   └── test_cli_integration.py
└── conftest.py          # Pytest fixtures

pyproject.toml           # UV/pip configuration
README.md                # Setup and usage instructions
CLAUDE.md                # Claude Code development instructions (already exists)
.specify/                # Spec-Kit Plus configuration (already exists)
```

**Structure Decision**: Using Option 1 (Single project) structure. This is a standalone console application with no backend/frontend separation needed. The `src/todo/` package contains all business logic, and `main.py` serves as the entry point. This structure supports:
- Clear separation of concerns (models, storage, operations, CLI)
- Easy testing (unit + integration)
- Simple deployment (single Python package)
- Future extensibility (can add features without restructuring)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - structure is minimal and appropriate for Phase I requirements.

---

## Phase 0: Research & Technical Decisions

### Research Areas

Since the requirements are clear and we're using only built-in Python libraries, minimal research is needed. Key decisions to document:

1. **CLI Framework**: Built-in `argparse` vs `sys.argv` vs `cmd` module
2. **Data Structure**: List of dicts vs custom classes vs dataclasses
3. **ID Generation**: Sequential integers vs UUID
4. **Status Representation**: Boolean vs Enum vs String
5. **Testing Strategy**: Unit vs integration test coverage approach

### Research Questions (to be answered in research.md)

- How to structure a maintainable CLI application in Python?
- What are best practices for in-memory data structures for CRUD operations?
- How to design user-friendly command-line interfaces?
- What validation patterns work best for console input?
- How to format console output for readability (status indicators, tables)?

---

## Phase 1: Design Artifacts

### 1. Data Model (data-model.md)

**Core Entities**:
- **Todo**: Individual task with id, title, description, status, created_at, updated_at
- **TodoStorage**: In-memory collection managing all todos

**Key Relationships**:
- TodoStorage has-many Todos
- Each Todo has unique identifier

**State Transitions**:
- New → Pending (on creation)
- Pending ↔ Completed (on status toggle)
- Any State → Deleted (on deletion)

### 2. CLI Contracts (contracts/)

Command-line interface contracts defining:
- Available commands and their arguments
- Expected input formats
- Output formats (success/error messages)
- Exit codes

Examples:
- `add <title> [description]` → Returns task ID and confirmation
- `list` → Returns formatted task list with status indicators
- `complete <id>` → Updates status and confirms
- `update <id> <field> <value>` → Updates field and confirms
- `delete <id>` → Removes task and confirms

### 3. Quickstart Guide (quickstart.md)

Step-by-step guide for:
- Installing UV and Python 3.13+
- Setting up the development environment
- Running the application
- Running tests
- Basic usage examples

---

## Next Steps

After completing Phase 0 & Phase 1 artifacts:

1. **Generate research.md** - Document technical decisions
2. **Generate data-model.md** - Define entity structures
3. **Generate contracts/** - Define CLI command contracts
4. **Generate quickstart.md** - Setup and usage guide
5. **Run /sp.tasks** - Break down implementation into atomic tasks
6. **Run /sp.implement** - Execute implementation following TDD workflow
