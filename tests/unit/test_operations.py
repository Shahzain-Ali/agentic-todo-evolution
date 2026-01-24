"""
Unit tests for the operations module
"""
import pytest
from src.todo.models import TodoStorage
from src.todo.operations import (
    add_todo, list_todos, complete_todo, incomplete_todo,
    update_todo, delete_todo
)


def test_add_todo():
    """Test adding a todo"""
    storage = TodoStorage()
    todo = add_todo(storage, "Test title", "Test description")

    assert todo is not None
    assert todo.title == "Test title"
    assert todo.description == "Test description"
    assert len(storage.get_all()) == 1


def test_add_todo_invalid_title():
    """Test adding a todo with invalid title"""
    storage = TodoStorage()
    todo = add_todo(storage, "", "Test description")

    assert todo is None
    assert len(storage.get_all()) == 0


def test_list_todos():
    """Test listing todos"""
    storage = TodoStorage()
    storage.add("Test title 1", "Test description 1")
    storage.add("Test title 2", "Test description 2")

    todos = list_todos(storage)
    assert len(todos) == 2


def test_list_todos_with_filter():
    """Test listing todos with status filter"""
    storage = TodoStorage()
    storage.add("Test title 1", "Test description 1")
    storage.toggle_status(1)  # Mark as complete
    storage.add("Test title 2", "Test description 2")

    completed_todos = list_todos(storage, "completed")
    pending_todos = list_todos(storage, "pending")

    assert len(completed_todos) == 1
    assert len(pending_todos) == 1
    assert completed_todos[0].status == "completed"
    assert pending_todos[0].status == "pending"


def test_complete_todo():
    """Test completing a todo"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")

    success = complete_todo(storage, 1)
    assert success is True

    todo = storage.get_by_id(1)
    assert todo.status == "completed"


def test_complete_todo_nonexistent():
    """Test completing a non-existent todo"""
    storage = TodoStorage()
    success = complete_todo(storage, 999)
    assert success is False


def test_incomplete_todo():
    """Test making a completed todo pending"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")
    storage.toggle_status(1)  # Mark as complete

    todo = storage.get_by_id(1)
    assert todo.status == "completed"

    success = incomplete_todo(storage, 1)
    assert success is True

    todo = storage.get_by_id(1)
    assert todo.status == "pending"


def test_incomplete_todo_nonexistent():
    """Test making a non-existent todo pending"""
    storage = TodoStorage()
    success = incomplete_todo(storage, 999)
    assert success is False


def test_update_todo():
    """Test updating a todo"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")

    success = update_todo(storage, 1, title="New title", description="New description")
    assert success is True

    todo = storage.get_by_id(1)
    assert todo.title == "New title"
    assert todo.description == "New description"


def test_update_todo_partial():
    """Test updating only title or description"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")

    # Update only title
    success = update_todo(storage, 1, title="New title")
    assert success is True

    todo = storage.get_by_id(1)
    assert todo.title == "New title"
    assert todo.description == "Test description"  # Should remain unchanged


def test_update_todo_nonexistent():
    """Test updating a non-existent todo"""
    storage = TodoStorage()
    success = update_todo(storage, 999, title="New title")
    assert success is False


def test_delete_todo():
    """Test deleting a todo"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")

    assert len(storage.get_all()) == 1

    success = delete_todo(storage, 1)
    assert success is True
    assert len(storage.get_all()) == 0


def test_delete_todo_nonexistent():
    """Test deleting a non-existent todo"""
    storage = TodoStorage()
    success = delete_todo(storage, 999)
    assert success is False