"""
Authentication Utilities for MCP Tools

[Task]: T009
[From]: specs/003-ai-chatbot/spec.md §2.2 (FR-007), specs/003-ai-chatbot/plan.md §Phase 2
"""

import logging
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from datetime import datetime

from ..config import config
from .errors import AuthenticationError, ErrorCode

logger = logging.getLogger(__name__)


def validate_jwt_token(token: str) -> Dict[str, Any]:
    """
    Validate JWT token and extract payload

    Args:
        token: JWT token string

    Returns:
        Decoded token payload containing user_id and other claims

    Raises:
        AuthenticationError: If token is invalid, expired, or malformed
    """
    if not token:
        raise AuthenticationError(
            message="Missing authentication token",
            details={"error_code": ErrorCode.MISSING_TOKEN}
        )

    try:
        # Decode and validate JWT token
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )

        # Verify required claims (support both "sub" and "user_id" formats)
        if "sub" not in payload and "user_id" not in payload:
            raise AuthenticationError(
                message="Invalid token: missing user identifier claim",
                details={"error_code": ErrorCode.INVALID_TOKEN}
            )

        # Normalize: if "sub" exists but "user_id" doesn't, copy it
        if "sub" in payload and "user_id" not in payload:
            payload["user_id"] = payload["sub"]

        # Check expiration (exp claim)
        if "exp" in payload:
            exp_timestamp = payload["exp"]
            if datetime.utcnow().timestamp() > exp_timestamp:
                raise AuthenticationError(
                    message="Token has expired",
                    details={"error_code": ErrorCode.EXPIRED_TOKEN}
                )

        logger.info(f"JWT token validated successfully for user_id={payload.get('user_id')}")
        return payload

    except JWTError as e:
        logger.warning(f"JWT validation failed: {str(e)}")
        raise AuthenticationError(
            message=f"Invalid authentication token: {str(e)}",
            details={"error_code": ErrorCode.INVALID_TOKEN}
        )


def extract_user_id(token: str):
    """
    Extract user_id from JWT token

    Args:
        token: JWT token string

    Returns:
        User ID (UUID or integer)

    Raises:
        AuthenticationError: If token is invalid or user_id cannot be extracted
    """
    from uuid import UUID

    payload = validate_jwt_token(token)

    # Support both "user_id" and "sub" claims
    user_id = payload.get("user_id") or payload.get("sub")

    if user_id is None:
        raise AuthenticationError(
            message="Token does not contain user_id",
            details={"error_code": ErrorCode.INVALID_TOKEN}
        )

    # Try UUID first, then int
    try:
        return UUID(str(user_id))
    except ValueError:
        try:
            return int(user_id)
        except (ValueError, TypeError):
            raise AuthenticationError(
                message="Invalid user_id format in token",
                details={"error_code": ErrorCode.INVALID_TOKEN}
            )


def require_authentication(token: Optional[str]):
    """
    Require authentication and return user ID

    Args:
        token: JWT token string (optional)

    Returns:
        User ID (UUID or integer) if authentication succeeds

    Raises:
        AuthenticationError: If authentication fails
    """
    if not token:
        raise AuthenticationError(
            message="Authentication required",
            details={"error_code": ErrorCode.MISSING_TOKEN}
        )

    return extract_user_id(token)
