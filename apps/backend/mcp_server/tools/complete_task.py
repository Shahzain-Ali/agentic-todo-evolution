"""
Complete Task MCP Tool

[Task]: T031
[From]: specs/003-ai-chatbot/spec.md §3.3 (US3), specs/003-ai-chatbot/contracts/mcp-tools.yaml

This tool marks a todo task as complete for the authenticated user.

Usage examples:
  User: "Mark task 1 as done"
  Agent: Calls complete_task(jwt_token=<token>, task_id=1)

  User: "I finished the first one"
  Agent: Calls complete_task(jwt_token=<token>, task_id=1)
"""

import logging
from typing import Dict, Any, Optional
from sqlmodel import Session, select

from app.models.task import Task
from ..utils.auth import require_authentication
from ..utils.errors import (
    create_success_response,
    create_error_response,
    ErrorCode,
    NotFoundError,
    AuthorizationError,
    MCPToolError
)
from ..server import get_db_session

logger = logging.getLogger(__name__)


async def complete_task(
    task_id: int,
    jwt_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Mark a todo task as complete

    Args:
        task_id: ID of the task to complete
        jwt_token: Optional JWT authentication token (for testing, uses demo user if not provided)

    Returns:
        Success response with updated task or error response

    Example:
        >>> result = await complete_task(
        ...     jwt_token="eyJ...",
        ...     task_id=1
        ... )
        >>> print(result)
        {
            "success": True,
            "task": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": True,
                "user_id": 1,
                "created_at": "2026-02-04T...",
                "updated_at": "2026-02-04T..."
            }
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

        logger.info(f"complete_task called by user_id={user_id}, task_id={task_id}")

        # Get database session
        db_session = get_db_session()

        try:
            # Find task
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id  # Enforce user isolation
            )
            task = db_session.exec(statement).first()

            if not task:
                # Task not found OR belongs to different user
                # Return NOT_FOUND for security (don't reveal if task exists for other user)
                raise NotFoundError(
                    resource="Task",
                    details={"task_id": task_id}
                )

            # Mark task as complete
            task.completed = True

            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)

            logger.info(f"Task {task_id} marked as complete by user_id={user_id}")

            # Return success response
            return create_success_response({
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "user_id": task.user_id,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                }
            })

        except MCPToolError:
            # Re-raise MCP errors (NotFoundError, etc.)
            raise

        except Exception as db_error:
            db_session.rollback()
            logger.error(f"Database error in complete_task: {str(db_error)}")
            return create_error_response(
                ErrorCode.DATABASE_ERROR,
                f"Failed to complete task: {str(db_error)}"
            )
        finally:
            db_session.close()

    except MCPToolError as e:
        # Handle known MCP errors
        logger.warning(f"MCP tool error in complete_task: {e.message}")
        return e.to_response()

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in complete_task: {str(e)}", exc_info=True)
        return create_error_response(
            ErrorCode.INTERNAL_ERROR,
            "An unexpected error occurred while completing the task"
        )
