# CLI Command Contracts: Console Todo Application

**Feature**: 001-todo-console-app
**Date**: 2026-01-08
**Purpose**: Define command-line interface contracts, inputs, outputs, and error handling

---

## Application Modes

The application operates in two modes:
1. **Interactive Mode** (Default): Launches the rich visual interface when run without arguments
2. **Command-Line Mode**: Executes specific commands when arguments are provided

---

## Command Overview

| Command | Purpose | Priority |
|---------|---------|----------|
| `add` | Create a new todo task | P1 |
| `list` | Display all todos | P1 |
| `complete` | Mark a todo as completed | P2 |
| `incomplete` | Mark a completed todo as pending | P2 |
| `update` | Modify todo title or description | P3 |
| `delete` | Remove a todo | P3 |
| `help` | Display usage information | P1 |

---

## Interactive Mode Features

When launched without arguments, the application provides:
- **ASCII Art Welcome Screen**: Stylish "TODO APP" banner
- **Colorful Menu System**: Emoji-enhanced menu options with color coding
- **Progress Indicators**: Loading spinners during operations
- **Visual Feedback**: Success/error messages with color coding
- **Statistics Dashboard**: Visual completion rates and progress bars
- **Confirmation Dialogs**: Prevent accidental deletions
- **Filtering Options**: Easily view pending, completed, or all todos
- **Responsive Tables**: Well-formatted todo listings with status indicators
- **Keyboard Navigation**: Easy menu navigation with arrow keys

---

## Global Patterns

### Exit Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 0 | Success | Operation completed successfully |
| 1 | User Error | Invalid input, validation failure |
| 2 | Application Error | Internal error (should not normally occur) |

### Output Format Standards

**Success Messages**:
```
✓ [Action completed]. [Details]
```

**Error Messages**:
```
✗ Error: [Specific issue]. [Actionable guidance]
```

**Info Messages**:
```
ℹ [Information]
```

---

## Command: `add`

### Syntax

```bash
python main.py add "<title>" ["<description>"]
# OR
python main.py add --title "<title>" [--description "<description>"]
```

### Parameters

| Parameter | Type | Required | Max Length | Description |
|-----------|------|----------|------------|-------------|
| title | string | Yes | 200 chars | Brief task description |
| description | string | No | 1000 chars | Detailed task information |

### Examples

```bash
# Minimal usage
python main.py add "Buy groceries"

# With description
python main.py add "Buy groceries" "Milk, eggs, bread, cheese"

# Named arguments
python main.py add --title "Finish report" --description "Q4 financial summary"
```

### Success Output

```
✓ Todo created successfully.
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread, cheese
  Status: Pending
```

### Error Scenarios

| Scenario | Output | Exit Code |
|----------|--------|-----------|
| Empty title | `✗ Error: Task title cannot be empty. Please provide a title for your task.` | 1 |
| Title too long (>200 chars) | `✗ Error: Title exceeds maximum length of 200 characters. Please shorten your title.` | 1 |
| Description too long (>1000 chars) | `✗ Error: Description exceeds maximum length of 1000 characters. Please shorten your description.` | 1 |

---

## Command: `list`

### Syntax

```bash
python main.py list
# OR
python main.py list --status [pending|completed|all]
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| --status | enum | No | all | Filter by status: pending, completed, or all |

### Examples

```bash
# List all todos
python main.py list

# List only pending
python main.py list --status pending

# List only completed
python main.py list --status completed
```

### Success Output (with todos)

```
Your Todos:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID | Status | Title                  | Description
───┼────────┼────────────────────────┼──────────────────────────────
1  | ✓      | Buy groceries          | Milk, eggs, bread, cheese
2  | ○      | Finish report          | Q4 financial summary
3  | ○      | Call dentist           |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 3 todos (1 completed, 2 pending)
```

### Success Output (empty list)

```
ℹ No todos found. Use 'python main.py add "<title>"' to create your first todo.
```

### Status Indicators

- `✓` = Completed
- `○` = Pending

### Error Scenarios

| Scenario | Output | Exit Code |
|----------|--------|-----------|
| Invalid status filter | `✗ Error: Invalid status 'done'. Valid options: pending, completed, all.` | 1 |

---

## Command: `complete`

### Syntax

```bash
python main.py complete <id>
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | ID of the todo to mark as complete |

### Examples

```bash
# Mark todo 1 as complete
python main.py complete 1
```

### Success Output

```
✓ Todo #1 marked as completed.
  Title: Buy groceries
```

### Error Scenarios

| Scenario | Output | Exit Code |
|----------|--------|-----------|
| Invalid ID (not a number) | `✗ Error: Invalid ID 'abc'. ID must be a number.` | 1 |
| Todo not found | `✗ Error: Todo #99 not found. Use 'list' to see available todos.` | 1 |
| Already completed | `ℹ Todo #1 is already completed.` | 0 |

---

## Command: `incomplete`

### Syntax

```bash
python main.py incomplete <id>
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | ID of the todo to mark as pending |

### Examples

```bash
# Mark todo 1 as pending
python main.py incomplete 1
```

### Success Output

```
✓ Todo #1 marked as pending.
  Title: Buy groceries
```

### Error Scenarios

| Scenario | Output | Exit Code |
|----------|--------|-----------|
| Invalid ID (not a number) | `✗ Error: Invalid ID 'abc'. ID must be a number.` | 1 |
| Todo not found | `✗ Error: Todo #99 not found. Use 'list' to see available todos.` | 1 |
| Already pending | `ℹ Todo #1 is already pending.` | 0 |

---

## Command: `update`

### Syntax

```bash
python main.py update <id> --title "<new_title>"
python main.py update <id> --description "<new_description>"
python main.py update <id> --title "<new_title>" --description "<new_description>"
```

### Parameters

| Parameter | Type | Required | Max Length | Description |
|-----------|------|----------|------------|-------------|
| id | integer | Yes | - | ID of the todo to update |
| --title | string | No | 200 chars | New title for the todo |
| --description | string | No | 1000 chars | New description for the todo |

**Note**: At least one of `--title` or `--description` must be provided.

### Examples

```bash
# Update title only
python main.py update 1 --title "Buy groceries and supplies"

# Update description only
python main.py update 1 --description "Milk, eggs, bread, cheese, butter"

# Update both
python main.py update 1 --title "Buy groceries" --description "Updated list"
```

### Success Output

```
✓ Todo #1 updated successfully.
  Title: Buy groceries and supplies
  Description: Milk, eggs, bread, cheese, butter
  Status: Pending
```

### Error Scenarios

| Scenario | Output | Exit Code |
|----------|--------|-----------|
| Invalid ID | `✗ Error: Invalid ID 'abc'. ID must be a number.` | 1 |
| Todo not found | `✗ Error: Todo #99 not found. Use 'list' to see available todos.` | 1 |
| No fields provided | `✗ Error: No update fields provided. Specify --title and/or --description.` | 1 |
| Empty title | `✗ Error: Task title cannot be empty. Please provide a valid title.` | 1 |
| Title too long | `✗ Error: Title exceeds maximum length of 200 characters. Please shorten your title.` | 1 |
| Description too long | `✗ Error: Description exceeds maximum length of 1000 characters. Please shorten your description.` | 1 |

---

## Command: `delete`

### Syntax

```bash
python main.py delete <id>
# OR with confirmation prompt
python main.py delete <id> --confirm
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | ID of the todo to delete |
| --confirm | flag | No | Skip confirmation prompt |

### Examples

```bash
# Delete with confirmation
python main.py delete 1

# Delete without confirmation
python main.py delete 1 --confirm
```

### Success Output (with confirmation)

```
⚠ Are you sure you want to delete todo #1: "Buy groceries"? (y/n): y
✓ Todo #1 deleted successfully.
```

### Success Output (--confirm flag)

```
✓ Todo #1 deleted successfully.
```

### Error Scenarios

| Scenario | Output | Exit Code |
|----------|--------|-----------|
| Invalid ID | `✗ Error: Invalid ID 'abc'. ID must be a number.` | 1 |
| Todo not found | `✗ Error: Todo #99 not found. Use 'list' to see available todos.` | 1 |
| User cancels deletion | `ℹ Deletion cancelled.` | 0 |

---

## Command: `help`

### Syntax

```bash
python main.py help
# OR
python main.py --help
# OR
python main.py -h
```

### Output

```
Todo Console Application - Manage your tasks from the command line

Usage:
  python main.py <command> [arguments]

Commands:
  add <title> [description]        Create a new todo task
  list [--status pending|completed|all]  Display all todos (default: all)
  complete <id>                    Mark a todo as completed
  incomplete <id>                  Mark a todo as pending
  update <id> [--title] [--description]  Modify a todo
  delete <id> [--confirm]          Remove a todo
  help                             Show this help message

Examples:
  python main.py add "Buy groceries" "Milk, eggs, bread"
  python main.py list
  python main.py complete 1
  python main.py update 2 --title "New title"
  python main.py delete 3

For more information, see README.md
```

---

## Error Handling Philosophy

### User-Friendly Errors
- **Clear**: State exactly what went wrong
- **Actionable**: Tell user how to fix it
- **Consistent**: Use standard format across all commands

### Internal Error Handling
- Catch all exceptions at CLI boundary
- Log internal errors for debugging
- Display generic message to user: `✗ An unexpected error occurred. Please try again.`
- Exit code 2 for internal errors

### Validation Strategy
- Validate inputs before processing
- Fail fast with specific error messages
- Never expose stack traces to CLI users

---

## Testing Contracts

Each command must have:
1. **Unit tests** for validation logic
2. **Integration tests** for end-to-end workflows
3. **Error case tests** for all documented error scenarios
4. **Edge case tests** (max length inputs, special characters, etc.)

### Test Coverage Requirements
- All success paths tested
- All error scenarios tested
- Exit codes verified
- Output format verified
