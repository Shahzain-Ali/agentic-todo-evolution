"""
List Tasks MCP Tool

[Task]: T026
[From]: specs/003-ai-chatbot/spec.md §3.2 (US2), specs/003-ai-chatbot/contracts/mcp-tools.yaml

This tool retrieves and filters todo tasks for the authenticated user.

Usage examples:
  User: "Show me all my tasks"
  Agent: Calls list_tasks(jwt_token=<token>, filter="all")

  User: "What tasks do I have left to do?"
  Agent: Calls list_tasks(jwt_token=<token>, filter="pending")
"""

import logging
from typing import Dict, Any, Optional, Literal
from sqlmodel import Session, select

from app.models.task import Task, TaskStatus
from ..utils.auth import require_authentication
from ..utils.errors import (
    create_success_response,
    create_error_response,
    ErrorCode,
    ValidationError,
    MCPToolError
)
from ..server import get_db_session

logger = logging.getLogger(__name__)

# Type for filter parameter
FilterType = Literal["all", "completed", "pending"]


async def list_tasks(
    filter: FilterType = "all",
    jwt_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    List and filter todo tasks

    Args:
        filter: Filter tasks by status ("all", "completed", "pending")
        jwt_token: Optional JWT authentication token (for testing, uses demo user if not provided)

    Returns:
        Success response with tasks list or error response

    Example:
        >>> result = await list_tasks(
        ...     jwt_token="eyJ...",
        ...     filter="pending"
        ... )
        >>> print(result)
        {
            "success": True,
            "tasks": [
                {
                    "id": 1,
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                    "completed": False,
                    "user_id": 1,
                    "created_at": "2026-02-04T...",
                    "updated_at": "2026-02-04T..."
                }
            ],
            "count": 1
        }
    """
    try:
        # Authenticate user (use demo UUID if no token provided)
        if jwt_token:
            user_id = require_authentication(jwt_token)
        else:
            # Demo UUID for testing (matches database UUID type)
            from uuid import UUID
            user_id = UUID("625460a4-b5f7-4c64-ba84-66da5dabfd3c")
            logger.info(f"Using demo user_id={user_id} (no JWT token provided)")

        logger.info(f"list_tasks called by user_id={user_id}, filter={filter}")

        # Validate filter parameter
        valid_filters = ["all", "completed", "pending"]
        if filter not in valid_filters:
            raise ValidationError(
                message=f"Invalid filter value. Must be one of: {', '.join(valid_filters)}",
                details={"field": "filter", "provided": filter, "valid_values": valid_filters}
            )

        # Get database session
        db_session = get_db_session()

        try:
            # Build query
            statement = select(Task).where(Task.user_id == user_id)

            # Apply filter
            if filter == "completed":
                statement = statement.where(Task.status == TaskStatus.COMPLETED)
            elif filter == "pending":
                statement = statement.where(Task.status == TaskStatus.PENDING)
            # "all" filter doesn't add additional conditions

            # Order by created_at descending (newest first)
            statement = statement.order_by(Task.created_at.desc())

            # Execute query
            tasks = db_session.exec(statement).all()

            logger.info(f"Retrieved {len(tasks)} tasks for user_id={user_id}, filter={filter}")

            # Format tasks for response
            tasks_data = [
                {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.status == TaskStatus.COMPLETED,
                    "user_id": str(task.user_id),
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                }
                for task in tasks
            ]

            # Return success response
            return create_success_response({
                "tasks": tasks_data,
                "count": len(tasks_data)
            })

        except Exception as db_error:
            logger.error(f"Database error in list_tasks: {str(db_error)}")
            return create_error_response(
                ErrorCode.DATABASE_ERROR,
                f"Failed to retrieve tasks: {str(db_error)}"
            )
        finally:
            db_session.close()

    except MCPToolError as e:
        # Handle known MCP errors
        logger.warning(f"MCP tool error in list_tasks: {e.message}")
        return e.to_response()

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in list_tasks: {str(e)}", exc_info=True)
        return create_error_response(
            ErrorCode.INTERNAL_ERROR,
            "An unexpected error occurred while retrieving tasks"
        )
