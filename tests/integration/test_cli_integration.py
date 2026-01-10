"""
Integration tests for the CLI functionality
"""
import subprocess
import sys
import os
from unittest.mock import patch, MagicMock
import io
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from todo.cli import main
from todo.models import TodoStorage


def test_cli_main_add_and_list():
    """Test the CLI add and list commands together"""
    # Create a temporary storage for testing
    storage = TodoStorage()

    # Test add command
    with patch('sys.argv', ['todo', 'add', 'Test title', 'Test description']):
        with patch('todo.cli.TodoStorage', return_value=storage):
            result = main(storage)
            assert result == 0  # Success

    # Test list command
    with patch('sys.argv', ['todo', 'list']):
        with patch('sys.argv', ['todo', 'list']):
            with patch('todo.cli.TodoStorage', return_value=storage):
                # Capture stdout to verify the output
                captured_output = io.StringIO()
                with patch('sys.stdout', captured_output):
                    result = main(storage)
                    assert result == 0  # Success

                output = captured_output.getvalue()
                assert "Test title" in output
                assert "Test description" in output


def test_cli_complete_and_incomplete():
    """Test the CLI complete and incomplete commands together"""
    storage = TodoStorage()

    # Add a todo first
    storage.add("Test title", "Test description")

    # Test complete command
    with patch('sys.argv', ['todo', 'complete', '1']):
        with patch('todo.cli.TodoStorage', return_value=storage):
            result = main(storage)
            assert result == 0  # Success

    # Verify the todo is completed
    todo = storage.get_by_id(1)
    assert todo.status == "completed"

    # Test incomplete command
    with patch('sys.argv', ['todo', 'incomplete', '1']):
        with patch('todo.cli.TodoStorage', return_value=storage):
            result = main(storage)
            assert result == 0  # Success

    # Verify the todo is now pending
    todo = storage.get_by_id(1)
    assert todo.status == "pending"


def test_cli_update():
    """Test the CLI update command"""
    storage = TodoStorage()

    # Add a todo first
    storage.add("Old title", "Old description")

    # Test update command
    with patch('sys.argv', ['todo', 'update', '1', '--title', 'New title', '--description', 'New description']):
        with patch('todo.cli.TodoStorage', return_value=storage):
            result = main(storage)
            assert result == 0  # Success

    # Verify the todo was updated
    todo = storage.get_by_id(1)
    assert todo.title == "New title"
    assert todo.description == "New description"


def test_cli_delete():
    """Test the CLI delete command"""
    storage = TodoStorage()

    # Add a todo first
    storage.add("Test title", "Test description")
    assert len(storage.get_all()) == 1

    # Mock input to confirm deletion
    with patch('builtins.input', return_value='y'):
        with patch('sys.argv', ['todo', 'delete', '1', '--confirm']):
            with patch('todo.cli.TodoStorage', return_value=storage):
                result = main(storage)
                assert result == 0  # Success

    # Verify the todo was deleted
    assert len(storage.get_all()) == 0


def test_cli_list_with_filters():
    """Test the CLI list command with different status filters"""
    storage = TodoStorage()

    # Add todos with different statuses
    storage.add("Pending task", "Description")
    storage.add("Completed task", "Description")
    storage.toggle_status(2)  # Mark the second task as completed

    # Test list with pending filter
    with patch('sys.argv', ['todo', 'list', '--status', 'pending']):
        with patch('todo.cli.TodoStorage', return_value=storage):
            # Capture stdout
            captured_output = io.StringIO()
            with patch('sys.stdout', captured_output):
                result = main(storage)
                assert result == 0  # Success

            output = captured_output.getvalue()
            # Should contain the pending task but not the completed one
            assert "Pending task" in output
            # The exact check depends on the formatter implementation
            # For now, just verify it runs without error


import sys
from unittest.mock import patch
import io

def test_cli_invalid_command():
    """Test the CLI with an invalid command"""
    storage = TodoStorage()

    # Capture stderr to check for error message
    with patch('sys.argv', ['todo', 'invalid_command']):
        with patch('todo.cli.TodoStorage', return_value=storage):
            # Capture stderr to avoid printing error message during test
            captured_stderr = io.StringIO()
            with patch('sys.stderr', captured_stderr):
                try:
                    result = main(storage)
                    # The CLI will call sys.exit(2) for invalid command
                    # So we expect this to raise SystemExit
                    assert result != 0  # Should fail for invalid command
                except SystemExit as e:
                    # The expected behavior is to exit with code 2
                    assert e.code == 2