"""
Todo Console Application - Input validation
"""
import re
from typing import Optional
from .models import TodoStorage


def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate todo title
    Returns (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Task title cannot be empty. Please provide a title for your task."

    if len(title) > 200:
        return False, "Title exceeds maximum length of 200 characters. Please shorten your title."

    return True, ""


def validate_description(description: str) -> tuple[bool, str]:
    """
    Validate todo description
    Returns (is_valid, error_message)
    """
    if len(description) > 1000:
        return False, "Description exceeds maximum length of 1000 characters. Please shorten your description."

    return True, ""


def validate_todo_id(id: str, storage: TodoStorage) -> tuple[bool, str, Optional[int]]:
    """
    Validate todo ID
    Returns (is_valid, error_message, parsed_id)
    """
    try:
        parsed_id = int(id)
        if parsed_id <= 0:
            return False, f"Invalid ID '{id}'. ID must be a positive number.", None

        # Check if todo exists
        todo = storage.get_by_id(parsed_id)
        if todo is None:
            return False, f"Todo #{parsed_id} not found. Use 'list' to see available todos.", None

        return True, "", parsed_id
    except ValueError:
        return False, f"Invalid ID '{id}'. ID must be a number.", None


def validate_status_filter(status: str) -> tuple[bool, str]:
    """
    Validate status filter parameter
    Returns (is_valid, error_message)
    """
    if status not in ["pending", "completed", "all"]:
        return False, f"Invalid status '{status}'. Valid options: pending, completed, all."

    return True, ""


def validate_update_fields(title: Optional[str], description: Optional[str]) -> tuple[bool, str]:
    """
    Validate that at least one field is provided for update
    Returns (is_valid, error_message)
    """
    if title is None and description is None:
        return False, "No update fields provided. Specify --title and/or --description."

    # Validate title if provided
    if title is not None:
        is_valid, error = validate_title(title)
        if not is_valid:
            return False, error

    # Validate description if provided
    if description is not None:
        is_valid, error = validate_description(description)
        if not is_valid:
            return False, error

    return True, ""