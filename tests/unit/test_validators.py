"""
Unit tests for the validators module
"""
import pytest
from src.todo.models import TodoStorage
from src.todo.validators import (
    validate_title, validate_description, validate_todo_id,
    validate_status_filter, validate_update_fields
)


def test_validate_title_valid():
    """Test validating a valid title"""
    is_valid, error = validate_title("Valid title")
    assert is_valid is True
    assert error == ""


def test_validate_title_empty():
    """Test validating an empty title"""
    is_valid, error = validate_title("")
    assert is_valid is False
    assert "Task title cannot be empty" in error


def test_validate_title_whitespace_only():
    """Test validating a title with only whitespace"""
    is_valid, error = validate_title("   ")
    assert is_valid is False
    assert "Task title cannot be empty" in error


def test_validate_title_too_long():
    """Test validating a title that's too long"""
    is_valid, error = validate_title("x" * 201)
    assert is_valid is False
    assert "Title exceeds maximum length" in error


def test_validate_description_valid():
    """Test validating a valid description"""
    is_valid, error = validate_description("Valid description")
    assert is_valid is True
    assert error == ""


def test_validate_description_too_long():
    """Test validating a description that's too long"""
    is_valid, error = validate_description("x" * 1001)
    assert is_valid is False
    assert "Description exceeds maximum length" in error


def test_validate_todo_id_valid():
    """Test validating a valid todo ID"""
    storage = TodoStorage()
    storage.add("Test title", "Test description")

    is_valid, error, parsed_id = validate_todo_id("1", storage)
    assert is_valid is True
    assert error == ""
    assert parsed_id == 1


def test_validate_todo_id_invalid_string():
    """Test validating an invalid ID string"""
    storage = TodoStorage()
    is_valid, error, parsed_id = validate_todo_id("abc", storage)
    assert is_valid is False
    assert "Invalid ID 'abc'. ID must be a number" in error
    assert parsed_id is None


def test_validate_todo_id_negative():
    """Test validating a negative ID"""
    storage = TodoStorage()
    is_valid, error, parsed_id = validate_todo_id("-1", storage)
    assert is_valid is False
    assert "Invalid ID '-1'. ID must be a positive number" in error
    assert parsed_id is None


def test_validate_todo_id_zero():
    """Test validating zero ID"""
    storage = TodoStorage()
    is_valid, error, parsed_id = validate_todo_id("0", storage)
    assert is_valid is False
    assert "Invalid ID '0'. ID must be a positive number" in error
    assert parsed_id is None


def test_validate_todo_id_nonexistent():
    """Test validating a non-existent todo ID"""
    storage = TodoStorage()
    is_valid, error, parsed_id = validate_todo_id("999", storage)
    assert is_valid is False
    assert "Todo #999 not found" in error
    assert parsed_id is None


def test_validate_status_filter_valid():
    """Test validating valid status filters"""
    for status in ["pending", "completed", "all"]:
        is_valid, error = validate_status_filter(status)
        assert is_valid is True
        assert error == ""


def test_validate_status_filter_invalid():
    """Test validating an invalid status filter"""
    is_valid, error = validate_status_filter("invalid")
    assert is_valid is False
    assert "Invalid status 'invalid'" in error


def test_validate_update_fields_valid():
    """Test validating valid update fields"""
    # Valid: both fields provided
    is_valid, error = validate_update_fields("New title", "New description")
    assert is_valid is True
    assert error == ""

    # Valid: only title provided
    is_valid, error = validate_update_fields("New title", None)
    assert is_valid is True
    assert error == ""

    # Valid: only description provided
    is_valid, error = validate_update_fields(None, "New description")
    assert is_valid is True
    assert error == ""


def test_validate_update_fields_none_provided():
    """Test validating when no fields are provided"""
    is_valid, error = validate_update_fields(None, None)
    assert is_valid is False
    assert "No update fields provided" in error


def test_validate_update_fields_invalid_title():
    """Test validating update with invalid title"""
    is_valid, error = validate_update_fields("x" * 201, "Valid description")
    assert is_valid is False
    assert "Title exceeds maximum length" in error


def test_validate_update_fields_invalid_description():
    """Test validating update with invalid description"""
    is_valid, error = validate_update_fields("Valid title", "x" * 1001)
    assert is_valid is False
    assert "Description exceeds maximum length" in error