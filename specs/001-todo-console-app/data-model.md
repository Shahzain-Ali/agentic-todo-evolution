# Data Model: Console Todo Application

**Feature**: 001-todo-console-app
**Date**: 2026-01-08
**Purpose**: Define entity structures, relationships, and state transitions

---

## Entity Definitions

### Entity 1: Todo

**Purpose**: Represents a single task that needs to be tracked

**Attributes**:

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| id | int | Yes | Auto-generated | Unique identifier for the task |
| title | str | Yes | - | Brief description of the task (max 200 chars) |
| description | str | No | "" | Detailed information about the task (max 1000 chars) |
| status | str | Yes | "pending" | Current state: "pending" or "completed" |
| created_at | datetime | Yes | Auto-generated | Timestamp when task was created |
| updated_at | datetime | Yes | Auto-generated | Timestamp when task was last modified |

**Visual Representation**:
- **Pending Status**: Displayed with ⏳ symbol and normal text formatting
- **Completed Status**: Displayed with ✅ symbol and strikethrough formatting
- **Table Format**: Organized in rich table with color-coded columns
- **Sorting**: Tasks sorted by creation date (newest first)

**Validation Rules**:
- `title`: Cannot be empty, max length 200 characters
- `description`: Optional, max length 1000 characters
- `status`: Must be one of ["pending", "completed"]
- `id`: Positive integer, unique within the application session
- Timestamps: Auto-managed, not user-editable

**Example Instance**:
```python
Todo(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread, and cheese",
    status="pending",
    created_at=datetime(2026, 1, 8, 10, 30, 0),
    updated_at=datetime(2026, 1, 8, 10, 30, 0)
)
```

---

### Entity 2: TodoStorage

**Purpose**: Manages the collection of all todos in memory

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| _todos | List[Todo] | Internal list storing all todo instances |
| _next_id | int | Counter for generating unique IDs |

**Operations**:

| Operation | Parameters | Returns | Description |
|-----------|-----------|---------|-------------|
| add() | title: str, description: str = "" | Todo | Creates new todo and adds to storage |
| get_by_id() | id: int | Optional[Todo] | Retrieves todo by ID, returns None if not found |
| get_all() | - | List[Todo] | Returns all todos in storage |
| update() | id: int, **kwargs | bool | Updates todo fields, returns success status |
| delete() | id: int | bool | Removes todo from storage, returns success status |
| toggle_status() | id: int | bool | Toggles between pending/completed, returns success status |

**Internal State**:
- Maintains list of todos in memory
- Tracks next available ID
- Handles concurrent modifications during single-user session

---

## Relationships

```
TodoStorage (1) ─────── has many ─────────> (n) Todo
    │
    ├─ Manages lifecycle of all todos
    ├─ Assigns unique IDs
    └─ Provides CRUD operations
```

**Relationship Rules**:
- TodoStorage owns all Todo instances
- Each Todo belongs to exactly one TodoStorage instance
- TodoStorage is responsible for ID generation and uniqueness
- Deleting a Todo removes it from TodoStorage (no cascading deletes needed)

---

## State Transitions

### Todo Status Lifecycle

```
         [Creation]
             │
             ↓
         ┌─────────┐
    ┌───→│ Pending │←───┐
    │    └─────────┘    │
    │         │         │
    │    [Mark Complete]│ [Mark Incomplete]
    │         │         │
    │         ↓         │
    │    ┌───────────┐  │
    └────│ Completed │──┘
         └───────────┘
              │
         [Delete]
              │
              ↓
          [Removed]
```

**Transition Rules**:

1. **Creation → Pending**:
   - Triggered by: `TodoStorage.add()`
   - Validates: Title non-empty
   - Side effects: Assigns ID, sets timestamps, adds to storage

2. **Pending → Completed**:
   - Triggered by: `TodoStorage.toggle_status()` or `update(status="completed")`
   - Validates: Todo exists, status is "pending"
   - Side effects: Updates `status`, updates `updated_at` timestamp

3. **Completed → Pending**:
   - Triggered by: `TodoStorage.toggle_status()` or `update(status="pending")`
   - Validates: Todo exists, status is "completed"
   - Side effects: Updates `status`, updates `updated_at` timestamp

4. **Any State → Removed**:
   - Triggered by: `TodoStorage.delete()`
   - Validates: Todo exists
   - Side effects: Removes from storage, ID is not reused

**Invalid Transitions**:
- Cannot transition to any state without existing in storage first
- Cannot have status other than "pending" or "completed"
- Cannot resurrect deleted todos (permanent removal)

---

## Data Constraints

### Uniqueness Constraints
- `Todo.id` must be unique across all todos in storage
- No two todos can have the same ID

### Referential Integrity
- All operations on Todo must go through TodoStorage
- Direct Todo instantiation bypasses ID generation (not recommended)

### Business Rules
- Title is mandatory (empty titles rejected)
- Description is optional (defaults to empty string)
- Status must be valid value ("pending" or "completed")
- Timestamps auto-managed (created_at on creation, updated_at on any modification)
- IDs are sequential integers starting from 1
- Deleted todo IDs are never reused in the same session

---

## Storage Characteristics

### In-Memory Storage Properties

**Advantages**:
- Instant read/write operations (O(1) for ID lookups with dict, O(n) with list)
- No I/O overhead
- Simple implementation
- No database setup required

**Limitations**:
- Data lost on application exit
- No persistence across sessions
- Limited by available RAM
- Single-user only (no concurrent access from multiple processes)

**Capacity**: Designed to handle hundreds of todos efficiently in memory

---

## Data Access Patterns

### Primary Access Patterns

1. **Create Todo**: `storage.add(title, description)` → O(1)
2. **Read All Todos**: `storage.get_all()` → O(n)
3. **Read Single Todo**: `storage.get_by_id(id)` → O(n) with list, O(1) with dict
4. **Update Todo**: `storage.update(id, **fields)` → O(n)
5. **Delete Todo**: `storage.delete(id)` → O(n)
6. **Toggle Status**: `storage.toggle_status(id)` → O(n)

**Optimization Opportunity**: If performance becomes an issue, maintain internal dict mapping ID → Todo for O(1) lookups while keeping list for ordered iteration.

---

## Example Usage Scenarios

### Scenario 1: Create and View

```python
storage = TodoStorage()

# Create todos
todo1 = storage.add("Buy groceries", "Milk, eggs, bread")
todo2 = storage.add("Finish report")

# View all
all_todos = storage.get_all()  # Returns [todo1, todo2]
```

### Scenario 2: Update and Complete

```python
# Update description
storage.update(1, description="Milk, eggs, bread, cheese")

# Mark complete
storage.toggle_status(1)

# Verify
todo = storage.get_by_id(1)
assert todo.status == "completed"
```

### Scenario 3: Delete

```python
# Delete todo
success = storage.delete(1)

# Verify removal
all_todos = storage.get_all()  # Returns [todo2]
```

---

## Future Extensibility

**Phase II Considerations** (when adding persistence):
- Add `save()` and `load()` methods to TodoStorage
- Introduce serialization layer (JSON/pickle)
- Add database adapter pattern
- Keep current interface intact (add methods, don't change existing)

**Phase III Considerations** (when adding AI features):
- Add `tags` field to Todo for categorization
- Add `priority` field for importance ranking
- Add `due_date` field for scheduling

**Design Note**: Current structure supports these additions without breaking changes—simply add new optional fields to Todo dataclass.
