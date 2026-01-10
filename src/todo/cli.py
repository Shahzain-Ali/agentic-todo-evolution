"""
Todo Console Application - Command Line Interface
"""
import argparse
import sys
from typing import Optional
from .models import TodoStorage
from .operations import (
    add_todo, list_todos, complete_todo, incomplete_todo,
    update_todo, delete_todo
)
from .validators import (
    validate_title, validate_description, validate_todo_id,
    validate_status_filter, validate_update_fields
)
from .formatters import (
    format_todo_list, format_add_success, format_complete_success,
    format_incomplete_success, format_update_success, format_delete_success,
    format_info_already_completed, format_info_already_pending,
    format_info_deletion_cancelled
)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Todo Console Application - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py add "Buy groceries" "Milk, eggs, bread"
  python main.py list
  python main.py complete 1
  python main.py update 2 --title "New title"
  python main.py delete 3
        """.strip()
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Create a new todo task")
    add_parser.add_argument("title", help="Brief task description", nargs='?')
    add_parser.add_argument("description", help="Detailed task information", nargs='?', default="")

    # List command
    list_parser = subparsers.add_parser("list", help="Display all todos")
    list_parser.add_argument(
        "--status",
        choices=["pending", "completed", "all"],
        default="all",
        help="Filter by status: pending, completed, or all (default: all)"
    )

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as completed")
    complete_parser.add_argument("id", help="ID of the todo to mark as complete")

    # Incomplete command
    incomplete_parser = subparsers.add_parser("incomplete", help="Mark a todo as pending")
    incomplete_parser.add_argument("id", help="ID of the todo to mark as pending")

    # Update command
    update_parser = subparsers.add_parser("update", help="Modify a todo")
    update_parser.add_argument("id", help="ID of the todo to update")
    update_parser.add_argument("--title", help="New title for the todo")
    update_parser.add_argument("--description", help="New description for the todo")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Remove a todo")
    delete_parser.add_argument("id", help="ID of the todo to delete")
    delete_parser.add_argument(
        "--confirm",
        action="store_true",
        help="Skip confirmation prompt"
    )

    return parser


def main(storage: Optional[TodoStorage] = None) -> int:
    """
    Main CLI entry point
    """
    if storage is None:
        storage = TodoStorage()

    parser = create_parser()
    args = parser.parse_args()

    # Handle commands
    if args.command == "add":
        return handle_add_command(args, storage)
    elif args.command == "list":
        return handle_list_command(args, storage)
    elif args.command == "complete":
        return handle_complete_command(args, storage)
    elif args.command == "incomplete":
        return handle_incomplete_command(args, storage)
    elif args.command == "update":
        return handle_update_command(args, storage)
    elif args.command == "delete":
        return handle_delete_command(args, storage)
    elif args.command is None:
        parser.print_help()
        return 0
    else:
        parser.print_help()
        return 1


def handle_add_command(args, storage: TodoStorage) -> int:
    """Handle the add command"""
    # Validate inputs
    if args.title is None:
        print("✗ Error: the following arguments are required: title")
        return 1

    is_valid, error = validate_title(args.title)
    if not is_valid:
        print(f"✗ Error: {error}")
        return 1

    is_valid, error = validate_description(args.description)
    if not is_valid:
        print(f"✗ Error: {error}")
        return 1

    # Add the todo
    todo = add_todo(storage, args.title, args.description)
    if todo is not None:
        print(format_add_success(todo))
        return 0
    else:
        return 1


def handle_list_command(args, storage: TodoStorage) -> int:
    """Handle the list command"""
    is_valid, error = validate_status_filter(args.status)
    if not is_valid:
        print(f"✗ Error: {error}")
        return 1

    todos = list_todos(storage, args.status if args.status != "all" else None)
    print(format_todo_list(todos))
    return 0


def handle_complete_command(args, storage: TodoStorage) -> int:
    """Handle the complete command"""
    is_valid, error, todo_id = validate_todo_id(args.id, storage)
    if not is_valid:
        print(f"✗ Error: {error}")
        return 1

    # Check if already completed
    todo = storage.get_by_id(todo_id)
    if todo.status == "completed":
        print(format_info_already_completed(todo))
        return 0

    success = complete_todo(storage, todo_id)
    if success:
        updated_todo = storage.get_by_id(todo_id)  # Get the updated todo
        print(format_complete_success(updated_todo))
        return 0
    else:
        print(f"✗ Error: Failed to update todo #{todo_id}")
        return 1


def handle_incomplete_command(args, storage: TodoStorage) -> int:
    """Handle the incomplete command"""
    is_valid, error, todo_id = validate_todo_id(args.id, storage)
    if not is_valid:
        print(f"✗ Error: {error}")
        return 1

    # Check if already pending
    todo = storage.get_by_id(todo_id)
    if todo.status == "pending":
        print(format_info_already_pending(todo))
        return 0

    success = incomplete_todo(storage, todo_id)
    if success:
        updated_todo = storage.get_by_id(todo_id)  # Get the updated todo
        print(format_incomplete_success(updated_todo))
        return 0
    else:
        print(f"✗ Error: Failed to update todo #{todo_id}")
        return 1


def handle_update_command(args, storage: TodoStorage) -> int:
    """Handle the update command"""
    is_valid, error, todo_id = validate_todo_id(args.id, storage)
    if not is_valid:
        print(f"✗ Error: {error}")
        return 1

    is_valid, error = validate_update_fields(args.title, args.description)
    if not is_valid:
        print(f"✗ Error: {error}")
        return 1

    success = update_todo(storage, todo_id, args.title, args.description)
    if success:
        updated_todo = storage.get_by_id(todo_id)  # Get the updated todo
        print(format_update_success(updated_todo))
        return 0
    else:
        print(f"✗ Error: Failed to update todo #{todo_id}")
        return 1


def handle_delete_command(args, storage: TodoStorage) -> int:
    """Handle the delete command"""
    is_valid, error, todo_id = validate_todo_id(args.id, storage)
    if not is_valid:
        print(f"✗ Error: {error}")
        return 1

    # Check for confirmation if --confirm flag is not provided
    if not args.confirm:
        todo = storage.get_by_id(todo_id)
        response = input(f"⚠ Are you sure you want to delete todo #{todo_id}: \"{todo.title}\"? (y/n): ")
        if response.lower() not in ['y', 'yes']:
            print(format_info_deletion_cancelled())
            return 0

    success = delete_todo(storage, todo_id)
    if success:
        print(format_delete_success(todo_id))
        return 0
    else:
        print(f"✗ Error: Failed to delete todo #{todo_id}")
        return 1


if __name__ == "__main__":
    sys.exit(main())