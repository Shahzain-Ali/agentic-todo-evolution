# Import all models for Alembic to detect
from app.models.user import User
from app.models.task import Task

__all__ = ["User", "Task"]
