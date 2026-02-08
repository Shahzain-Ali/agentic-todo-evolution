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

from app.models.task import Task
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
    jwt_token: str,
    filter: FilterType = "all"
) -> Dict[str, Any]:
    """
    List and filter todo tasks

    Args:
        jwt_token: JWT authentication token
        filter: Filter tasks by status ("all", "completed", "pending")

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
        # Authenticate user
        user_id = require_authentication(jwt_token)
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
                statement = statement.where(Task.completed == True)
            elif filter == "pending":
                statement = statement.where(Task.completed == False)
            # "all" filter doesn't add additional conditions

            # Order by created_at descending (newest first)
            statement = statement.order_by(Task.created_at.desc())

            # Execute query
            tasks = db_session.exec(statement).all()

            logger.info(f"Retrieved {len(tasks)} tasks for user_id={user_id}, filter={filter}")

            # Format tasks for response
            tasks_data = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "user_id": task.user_id,
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
