"""
Error Handling Utilities for MCP Tools

[Task]: T008
[From]: specs/003-ai-chatbot/spec.md §2.6 (FR-012), specs/003-ai-chatbot/plan.md §Phase 2
"""

import logging
from enum import Enum
from typing import Any, Dict, Optional

# Configure logger
logger = logging.getLogger(__name__)


class ErrorCode(str, Enum):
    """Standard error codes for MCP tools"""

    # Authentication errors
    INVALID_TOKEN = "INVALID_TOKEN"
    EXPIRED_TOKEN = "EXPIRED_TOKEN"
    MISSING_TOKEN = "MISSING_TOKEN"

    # Authorization errors
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"

    # Resource errors
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"

    # Validation errors
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_PARAMETER = "MISSING_PARAMETER"

    # System errors
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def create_error_response(
    error_code: ErrorCode,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create standardized error response for MCP tools

    Args:
        error_code: Error code from ErrorCode enum
        message: Human-readable error message
        details: Optional additional error details (sanitized)

    Returns:
        Dictionary with error information
    """
    error_response = {
        "success": False,
        "error": {
            "code": error_code.value,
            "message": message
        }
    }

    if details:
        # Sanitize details - remove sensitive information
        safe_details = {k: v for k, v in details.items()
                        if k not in ["password", "token", "secret"]}
        error_response["error"]["details"] = safe_details

    # Log error for debugging (without sensitive data)
    logger.error(
        f"MCP Tool Error: {error_code.value} - {message}",
        extra={"details": details} if details else {}
    )

    return error_response


def create_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create standardized success response for MCP tools

    Args:
        data: Response data

    Returns:
        Dictionary with success flag and data
    """
    return {
        "success": True,
        **data
    }


class MCPToolError(Exception):
    """Base exception for MCP tool errors"""

    def __init__(self, error_code: ErrorCode, message: str, details: Optional[Dict[str, Any]] = None):
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(message)

    def to_response(self) -> Dict[str, Any]:
        """Convert exception to error response"""
        return create_error_response(self.error_code, self.message, self.details)


class AuthenticationError(MCPToolError):
    """Raised when authentication fails"""

    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorCode.INVALID_TOKEN, message, details)


class AuthorizationError(MCPToolError):
    """Raised when user is not authorized"""

    def __init__(self, message: str = "Not authorized to access this resource", details: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorCode.FORBIDDEN, message, details)


class NotFoundError(MCPToolError):
    """Raised when resource is not found"""

    def __init__(self, resource: str = "Resource", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            ErrorCode.NOT_FOUND,
            f"{resource} not found",
            details
        )


class ValidationError(MCPToolError):
    """Raised when input validation fails"""

    def __init__(self, message: str = "Invalid input", details: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorCode.INVALID_INPUT, message, details)
