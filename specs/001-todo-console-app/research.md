# Technical Research: Console Todo Application

**Feature**: 001-todo-console-app
**Date**: 2026-01-08
**Purpose**: Document technical decisions and rationale for implementation approach

---

## Research Question 1: CLI Framework Selection

**Decision**: Use Python's `argparse` module

**Rationale**:
- Built-in library (no external dependencies)
- Robust argument parsing with automatic help generation
- Supports subcommands pattern (add, list, delete, etc.)
- Better error messages than raw sys.argv parsing
- Industry standard for Python CLI applications

**Alternatives Considered**:
1. **Raw sys.argv**: Too low-level, requires manual parsing and validation
2. **cmd module**: Interactive shell pattern - overkill for simple CRUD operations
3. **click/typer**: External dependencies (violates Phase I simplicity principle)

**References**:
- Python argparse documentation: https://docs.python.org/3/library/argparse.html
- CLI best practices emphasize argparse for standard command-line tools

---

## Research Question 2: Data Structure for Todo Storage

**Decision**: Use Python dataclasses with in-memory list storage

**Rationale**:
- Dataclasses provide clean, type-annotated entity definitions (PEP 557)
- Built-in (Python 3.7+), no external dependencies
- Automatic __init__, __repr__, __eq__ methods
- Easy to serialize/deserialize for future persistence
- Clear separation between data (dataclass) and operations (TodoStorage class)

**Alternatives Considered**:
1. **Dictionary-based**: Less type-safe, harder to maintain, no IDE support
2. **Plain classes**: More boilerplate code than dataclasses
3. **Named tuples**: Immutable (problematic for updates)

**Implementation Pattern**:
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Todo:
    id: int
    title: str
    description: str = ""
    status: str = "pending"  # "pending" or "completed"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

class TodoStorage:
    def __init__(self):
        self._todos: List[Todo] = []
        self._next_id: int = 1
```

---

## Research Question 3: ID Generation Strategy

**Decision**: Sequential integers starting from 1

**Rationale**:
- Simple and predictable for users
- Easy to type in CLI (short numbers)
- Sufficient for in-memory, single-user application
- No collision risk in single-process context
- Human-readable in output displays

**Alternatives Considered**:
1. **UUID**: Overkill for non-distributed, in-memory storage; hard to type
2. **Hash-based**: Unnecessary complexity; longer identifiers
3. **Timestamp-based**: Potential collisions with rapid operations

**Implementation**: Maintain counter in TodoStorage, increment on each add

---

## Research Question 4: Status Representation

**Decision**: String literals ("pending", "completed")

**Rationale**:
- Simple and readable in code and output
- Easy to extend with additional statuses in future phases
- No need for Enum overhead in Phase I
- Direct mapping to user-facing display

**Alternatives Considered**:
1. **Boolean**: Limited to 2 states; not extensible
2. **Enum**: Adds complexity for only 2 states; can refactor later if needed
3. **Integer codes**: Less readable; requires mapping layer

**Validation**: Status setter validates against allowed values ["pending", "completed"]

---

## Research Question 5: Testing Strategy

**Decision**: Pytest with >80% code coverage, unit + integration tests

**Rationale**:
- Pytest is Python standard for testing
- Supports fixtures for reusable test data
- Clear, readable test syntax
- Excellent error reporting
- Supports parametrized tests for edge cases

**Coverage Approach**:
- **Unit tests**: Individual functions/methods in models, storage, operations, validators, formatters
- **Integration tests**: Full CLI workflows (add → list → update → delete)
- **Edge case tests**: Empty lists, invalid IDs, empty titles, long inputs

**Test Organization**:
```
tests/
├── unit/          # Fast, isolated tests
├── integration/   # End-to-end CLI scenarios
└── conftest.py    # Shared fixtures (sample todos, storage instances)
```

---

## Research Question 6: Console Output Formatting

**Decision**: Use string formatting with Unicode symbols for status indicators

**Rationale**:
- Cross-platform Unicode support in modern terminals
- Clear visual differentiation (✓ for completed, ○ for pending)
- Lightweight formatting without external libraries
- Readable output with consistent column alignment

**Format Pattern**:
```
ID | Status | Title                  | Description
---+--------+------------------------+---------------------------
1  | ✓      | Buy groceries         | Milk, eggs, bread
2  | ○      | Finish report         | Q4 financial summary
```

**Alternatives Considered**:
1. **Rich/tabulate libraries**: External dependencies (violates Phase I principle)
2. **Plain text**: Less visual clarity
3. **ANSI colors**: Compatibility issues on some terminals

**Fallback**: If Unicode fails, use ASCII alternatives (✓ → [X], ○ → [ ])

---

## Research Question 7: Input Validation Approach

**Decision**: Centralized validator module with clear error messages

**Rationale**:
- Single responsibility: validation logic separated from business logic
- Reusable validation functions across CLI commands
- Consistent error message formatting
- Easy to test in isolation

**Validation Rules**:
- **Title**: Non-empty string, max 200 characters
- **Description**: Optional, max 1000 characters
- **ID**: Positive integer, must exist in storage
- **Status**: Must be "pending" or "completed"

**Error Message Pattern**: `Error: [specific issue]. [actionable guidance]`
Example: `Error: Task title cannot be empty. Please provide a title for your task.`

---

## Summary of Technical Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.13+ | Modern Python features, type hints, dataclasses |
| CLI Framework | argparse (built-in) | Standard, robust, no dependencies |
| Data Structure | dataclasses + list | Type-safe, clean, built-in |
| ID Generation | Sequential integers | Simple, user-friendly |
| Status Model | String literals | Readable, extensible |
| Testing | pytest | Industry standard, excellent DX |
| Output Format | Unicode + string formatting | Clear, cross-platform |
| Validation | Centralized validators | Maintainable, reusable |

---

## Architectural Decisions

### Decision 1: Layered Architecture

**Chosen Approach**: Separate layers for models, storage, operations, CLI, validators, formatters

**Why**:
- Clear separation of concerns
- Easy to test each layer independently
- Supports future refactoring (e.g., swapping in-memory storage for database)
- Follows single responsibility principle

**Impact**: Slightly more files, but significantly better maintainability

---

### Decision 2: Immutability vs Mutability

**Chosen Approach**: Mutable Todo objects with explicit update tracking (updated_at field)

**Why**:
- Simpler implementation for CRUD operations
- Matches user mental model (tasks change over time)
- No performance concerns for in-memory operations
- Easier to track modifications with updated_at timestamp

**Trade-off**: Less functional purity, but more pragmatic for CRUD use case

---

### Decision 3: Error Handling Philosophy

**Chosen Approach**: Fail fast with user-friendly messages, never expose stack traces to CLI users

**Why**:
- Better user experience
- Clear error messages guide users to correct input
- Internal errors logged but not displayed
- Supports debugging without overwhelming users

**Implementation**: Try-except blocks at CLI boundary, structured error types internally

---

## Next Steps

With these technical decisions documented:
1. ✅ Phase 0 complete - all research questions answered
2. ➡️ Proceed to Phase 1: Create data-model.md, contracts/, quickstart.md
3. ➡️ Then run /sp.tasks to generate implementation tasks
