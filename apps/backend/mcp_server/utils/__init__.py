"""
MCP Utilities Package

[Task]: T013
[From]: specs/003-ai-chatbot/spec.md §2, specs/003-ai-chatbot/plan.md §Phase 2

This package contains utility modules for MCP tools:
- auth: JWT validation and user extraction
- errors: Error handling and response formatting
"""

from .auth import validate_jwt_token, extract_user_id, require_authentication
from .errors import (
    ErrorCode,
    create_error_response,
    create_success_response,
    MCPToolError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
)

__all__ = [
    # Auth utilities
    "validate_jwt_token",
    "extract_user_id",
    "require_authentication",
    # Error utilities
    "ErrorCode",
    "create_error_response",
    "create_success_response",
    "MCPToolError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
]
