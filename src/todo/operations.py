"""
Todo Console Application - Business operations
"""
from typing import Optional, List
from .models import Todo, TodoStorage


def add_todo(storage: TodoStorage, title: str, description: str = "") -> Optional[Todo]:
    """
    Create a new todo and add to storage
    """
    try:
        return storage.add(title, description)
    except ValueError as e:
        print(f"✗ Error: {e}")
        return None


def list_todos(storage: TodoStorage, status_filter: Optional[str] = None) -> List[Todo]:
    """
    Get all todos, optionally filtered by status
    """
    todos = storage.get_all()

    if status_filter == "pending":
        return [todo for todo in todos if todo.status == "pending"]
    elif status_filter == "completed":
        return [todo for todo in todos if todo.status == "completed"]
    else:
        # Return all todos (no filter)
        return todos


def complete_todo(storage: TodoStorage, id: int) -> bool:
    """
    Mark a todo as completed
    """
    return storage.toggle_status(id)


def incomplete_todo(storage: TodoStorage, id: int) -> bool:
    """
    Mark a completed todo as pending
    """
    return storage.toggle_status(id)


def update_todo(storage: TodoStorage, id: int, title: Optional[str] = None,
                description: Optional[str] = None) -> bool:
    """
    Update todo title or description
    """
    if title is None and description is None:
        return False

    updates = {}
    if title is not None:
        updates['title'] = title
    if description is not None:
        updates['description'] = description

    return storage.update(id, **updates)


def delete_todo(storage: TodoStorage, id: int) -> bool:
    """
    Remove a todo from storage
    """
    return storage.delete(id)