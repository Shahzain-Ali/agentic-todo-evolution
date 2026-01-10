"""
Todo Console Application - Output formatting
"""
from typing import List
from .models import Todo


def format_todo_list(todos: List[Todo]) -> str:
    """
    Format a list of todos for display
    """
    if not todos:
        return "ℹ No todos found. Use 'python main.py add \"<title>\"' to create your first todo."

    # Create table header
    output = "Your Todos:\n"
    output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    output += "ID | Status | Title                  | Description\n"
    output += "───┼────────┼────────────────────────┼──────────────────────────────\n"

    # Add each todo to the table
    for todo in todos:
        status_symbol = "✓" if todo.status == "completed" else "○"
        title = todo.title[:22] if len(todo.title) > 22 else todo.title
        description = todo.description[:28] if len(todo.description) > 28 else todo.description
        output += f"{todo.id:2d} | {status_symbol}      | {title:<22} | {description}\n"

    output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    # Add summary
    total = len(todos)
    completed = len([t for t in todos if t.status == "completed"])
    pending = total - completed
    output += f"\nTotal: {total} todos ({completed} completed, {pending} pending)"

    return output


def format_single_todo(todo: Todo) -> str:
    """
    Format a single todo for display
    """
    status_symbol = "✓" if todo.status == "completed" else "○"
    return f"  ID: {todo.id}\n  Title: {todo.title}\n  Description: {todo.description}\n  Status: {todo.status.title()}"


def format_add_success(todo: Todo) -> str:
    """
    Format success message for add operation
    """
    return f"✓ Todo created successfully.\n{format_single_todo(todo)}"


def format_complete_success(todo: Todo) -> str:
    """
    Format success message for complete operation
    """
    return f"✓ Todo #{todo.id} marked as completed.\n  Title: {todo.title}"


def format_incomplete_success(todo: Todo) -> str:
    """
    Format success message for incomplete operation
    """
    return f"✓ Todo #{todo.id} marked as pending.\n  Title: {todo.title}"


def format_update_success(todo: Todo) -> str:
    """
    Format success message for update operation
    """
    return f"✓ Todo #{todo.id} updated successfully.\n{format_single_todo(todo)}"


def format_delete_success(todo_id: int) -> str:
    """
    Format success message for delete operation
    """
    return f"✓ Todo #{todo_id} deleted successfully."


def format_info_already_completed(todo: Todo) -> str:
    """
    Format info message when todo is already completed
    """
    return f"ℹ Todo #{todo.id} is already completed."


def format_info_already_pending(todo: Todo) -> str:
    """
    Format info message when todo is already pending
    """
    return f"ℹ Todo #{todo.id} is already pending."


def format_info_deletion_cancelled() -> str:
    """
    Format info message when deletion is cancelled
    """
    return "ℹ Deletion cancelled."