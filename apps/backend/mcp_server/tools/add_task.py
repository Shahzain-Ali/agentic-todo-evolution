"""
Add Task MCP Tool

[Task]: T021
[From]: specs/003-ai-chatbot/spec.md §3.1 (US1), specs/003-ai-chatbot/contracts/mcp-tools.yaml

This tool creates a new todo task for the authenticated user via natural language.

Usage example:
  User: "Add buy groceries to my list"
  Agent: Calls add_task(jwt_token=<token>, title="Buy groceries")
"""

import logging
from typing import Dict, Any, Optional
from sqlmodel import Session

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


async def add_task(
    title: str,
    description: Optional[str] = None,
    jwt_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new todo task

    Args:
        title: Task title (max 200 characters)
        description: Optional task description (max 1000 characters)
        jwt_token: Optional JWT authentication token (for testing, uses demo user if not provided)

    Returns:
        Success response with created task or error response

    Example:
        >>> result = await add_task(
        ...     title="Buy groceries",
        ...     description="Milk, eggs, bread"
        ... )
        >>> print(result)
        {
            "success": True,
            "task": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
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

        logger.info(f"add_task called by user_id={user_id}")

        # Validate title
        if not title or not title.strip():
            raise ValidationError(
                message="Title cannot be empty",
                details={"field": "title"}
            )

        if len(title) > 200:
            raise ValidationError(
                message="Title exceeds maximum length of 200 characters",
                details={"field": "title", "max_length": 200, "provided_length": len(title)}
            )

        # Validate description if provided
        if description and len(description) > 1000:
            raise ValidationError(
                message="Description exceeds maximum length of 1000 characters",
                details={"field": "description", "max_length": 1000, "provided_length": len(description)}
            )

        # Get database session
        db_session = get_db_session()

        try:
            # Create task
            task = Task(
                title=title.strip(),
                description=description.strip() if description else None,
                completed=False,
                user_id=user_id
            )

            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)

            logger.info(f"Task created successfully: id={task.id}, user_id={user_id}")

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

        except Exception as db_error:
            db_session.rollback()
            logger.error(f"Database error in add_task: {str(db_error)}")
            return create_error_response(
                ErrorCode.DATABASE_ERROR,
                f"Failed to create task: {str(db_error)}"
            )
        finally:
            db_session.close()

    except MCPToolError as e:
        # Handle known MCP errors
        logger.warning(f"MCP tool error in add_task: {e.message}")
        return e.to_response()

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in add_task: {str(e)}", exc_info=True)
        return create_error_response(
            ErrorCode.INTERNAL_ERROR,
            "An unexpected error occurred while creating the task"
        )
