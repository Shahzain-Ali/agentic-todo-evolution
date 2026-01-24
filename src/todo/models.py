"""
Todo Console Application - Data models
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    """
    Represents a single task that needs to be tracked
    """
    id: int
    title: str
    description: str = ""
    status: str = "pending"  # "pending" or "completed"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the todo after initialization"""
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Title exceeds maximum length of 200 characters")
        if len(self.description) > 1000:
            raise ValueError("Description exceeds maximum length of 1000 characters")
        if self.status not in ["pending", "completed"]:
            raise ValueError(f"Status must be 'pending' or 'completed', got '{self.status}'")

    def complete(self):
        """Mark the todo as completed"""
        self.status = "completed"
        self.updated_at = datetime.now()

    def incomplete(self):
        """Mark the todo as pending"""
        self.status = "pending"
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None):
        """Update the todo's title or description"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()


class TodoStorage:
    """
    Manages the collection of all todos in memory
    """
    def __init__(self):
        self._todos = []  # List[Todo]
        self._next_id = 1

    def add(self, title: str, description: str = "") -> Todo:
        """Create new todo and add to storage"""
        todo = Todo(
            id=self._next_id,
            title=title,
            description=description
        )
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def get_by_id(self, id: int) -> Optional[Todo]:
        """Retrieve todo by ID, returns None if not found"""
        for todo in self._todos:
            if todo.id == id:
                return todo
        return None

    def get_all(self) -> list[Todo]:
        """Returns all todos in storage"""
        return self._todos.copy()

    def update(self, id: int, **kwargs) -> bool:
        """Updates todo fields, returns success status"""
        todo = self.get_by_id(id)
        if todo is None:
            return False

        # Allow updating title and description
        if 'title' in kwargs:
            todo.title = kwargs['title']
        if 'description' in kwargs:
            todo.description = kwargs['description']

        todo.updated_at = datetime.now()
        return True

    def delete(self, id: int) -> bool:
        """Removes todo from storage, returns success status"""
        for i, todo in enumerate(self._todos):
            if todo.id == id:
                del self._todos[i]
                return True
        return False

    def toggle_status(self, id: int) -> bool:
        """Toggles between pending/completed, returns success status"""
        todo = self.get_by_id(id)
        if todo is None:
            return False

        if todo.status == "pending":
            todo.complete()
        else:
            todo.incomplete()
        return True