"""
Unit tests for the models module
"""
import pytest
from datetime import datetime
from src.todo.models import Todo, TodoStorage


def test_todo_creation():
    """Test creating a todo with valid data"""
    todo = Todo(id=1, title="Test title", description="Test description")
    assert todo.id == 1
    assert todo.title == "Test title"
    assert todo.description == "Test description"
    assert todo.status == "pending"
    assert isinstance(todo.created_at, datetime)
    assert isinstance(todo.updated_at, datetime)


def test_todo_creation_defaults():
    """Test creating a todo with minimal data"""
    todo = Todo(id=1, title="Test title")
    assert todo.id == 1
    assert todo.title == "Test title"
    assert todo.description == ""
    assert todo.status == "pending"


def test_todo_validation_empty_title():
    """Test that empty title raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Todo(id=1, title="")


def test_todo_validation_long_title():
    """Test that long title raises ValueError"""
    with pytest.raises(ValueError, match="Title exceeds maximum length"):
        Todo(id=1, title="x" * 201)


def test_todo_validation_long_description():
    """Test that long description raises ValueError"""
    with pytest.raises(ValueError, match="Description exceeds maximum length"):
        Todo(id=1, title="Test", description="x" * 1001)


def test_todo_validation_invalid_status():
    """Test that invalid status raises ValueError"""
    with pytest.raises(ValueError, match="Status must be 'pending' or 'completed'"):
        Todo(id=1, title="Test", status="invalid")


def test_todo_complete():
    """Test marking todo as complete"""
    todo = Todo(id=1, title="Test title")
    assert todo.status == "pending"
    todo.complete()
    assert todo.status == "completed"


def test_todo_incomplete():
    """Test marking todo as pending"""
    todo = Todo(id=1, title="Test title", status="completed")
    assert todo.status == "completed"
    todo.incomplete()
    assert todo.status == "pending"


def test_todo_update():
    """Test updating todo fields"""
    todo = Todo(id=1, title="Test title", description="Test description")
    original_updated_at = todo.updated_at

    todo.update(title="New title", description="New description")
    assert todo.title == "New title"
    assert todo.description == "New description"
    assert todo.updated_at > original_updated_at


def test_todo_storage_add():
    """Test adding todos to storage"""
    storage = TodoStorage()
    todo = storage.add("Test title", "Test description")

    assert todo.id == 1
    assert todo.title == "Test title"
    assert todo.description == "Test description"
    assert len(storage.get_all()) == 1


def test_todo_storage_get_by_id():
    """Test getting a specific todo by ID"""
    storage = TodoStorage()
    todo = storage.add("Test title", "Test description")

    retrieved = storage.get_by_id(1)
    assert retrieved is not None
    assert retrieved.id == 1
    assert retrieved.title == "Test title"

    assert storage.get_by_id(999) is None


def test_todo_storage_get_all():
    """Test getting all todos"""
    storage = TodoStorage()
    storage.add("Test title 1", "Test description 1")
    storage.add("Test title 2", "Test description 2")

    todos = storage.get_all()
    assert len(todos) == 2
    assert todos[0].title == "Test title 1"
    assert todos[1].title == "Test title 2"


def test_todo_storage_update():
    """Test updating a todo in storage"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")

    success = storage.update(1, title="New title", description="New description")
    assert success is True

    updated_todo = storage.get_by_id(1)
    assert updated_todo.title == "New title"
    assert updated_todo.description == "New description"


def test_todo_storage_update_nonexistent():
    """Test updating a non-existent todo"""
    storage = TodoStorage()
    success = storage.update(999, title="New title")
    assert success is False


def test_todo_storage_delete():
    """Test deleting a todo from storage"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")

    success = storage.delete(1)
    assert success is True
    assert len(storage.get_all()) == 0


def test_todo_storage_delete_nonexistent():
    """Test deleting a non-existent todo"""
    storage = TodoStorage()
    success = storage.delete(999)
    assert success is False


def test_todo_storage_toggle_status():
    """Test toggling todo status"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")

    todo = storage.get_by_id(1)
    assert todo.status == "pending"

    success = storage.toggle_status(1)
    assert success is True

    todo = storage.get_by_id(1)
    assert todo.status == "completed"

    success = storage.toggle_status(1)
    assert success is True

    todo = storage.get_by_id(1)
    assert todo.status == "pending"


def test_todo_storage_toggle_status_nonexistent():
    """Test toggling status of non-existent todo"""
    storage = TodoStorage()
    success = storage.toggle_status(999)
    assert success is False