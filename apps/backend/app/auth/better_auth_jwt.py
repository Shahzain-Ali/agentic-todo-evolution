"""
Better Auth JWT Token Verification

This module handles JWT token validation for tokens issued by Better Auth.
Better Auth (frontend) generates JWT tokens that need to be validated by FastAPI backend.
"""

import os
import jwt
from datetime import datetime, timezone
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, InvalidIssuerError, InvalidAudienceError
from typing import Optional, Dict, Any


# Better Auth JWT Configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-long-for-production-use")
BETTER_AUTH_ISSUER = os.getenv("BETTER_AUTH_ISSUER", "todo-app")
BETTER_AUTH_AUDIENCE = os.getenv("BETTER_AUTH_AUDIENCE", "todo-api")
ALGORITHM = "HS256"


def verify_better_auth_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode Better Auth JWT token.

    Args:
        token: JWT token string from Better Auth

    Returns:
        Decoded token payload containing user information

    Raises:
        ValueError: If token is invalid, expired, or has wrong issuer/audience
    """
    try:
        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM],
            audience=BETTER_AUTH_AUDIENCE,
            issuer=BETTER_AUTH_ISSUER,
        )

        return payload

    except ExpiredSignatureError:
        raise ValueError("Token has expired. Please log in again.")

    except InvalidIssuerError:
        raise ValueError(f"Invalid token issuer. Expected: {BETTER_AUTH_ISSUER}")

    except InvalidAudienceError:
        raise ValueError(f"Invalid token audience. Expected: {BETTER_AUTH_AUDIENCE}")

    except InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")


def extract_user_id_from_token(token: str) -> str:
    """
    Extract user ID from Better Auth JWT token.

    Better Auth stores user information in the token payload.
    This function extracts the user ID for database queries.

    Args:
        token: JWT token string from Better Auth

    Returns:
        User ID as string

    Raises:
        ValueError: If token is invalid or doesn't contain user ID
    """
    try:
        payload = verify_better_auth_token(token)

        # Better Auth typically uses 'sub' (subject) claim for user ID
        # Also check for 'user_id', 'userId', or 'id' as fallbacks
        user_id = (
            payload.get("sub") or
            payload.get("user_id") or
            payload.get("userId") or
            payload.get("id")
        )

        if not user_id:
            raise ValueError("Token does not contain user ID")

        return str(user_id)

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to extract user ID from token: {str(e)}")


def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Get full token payload without verification (for debugging).

    WARNING: This does NOT verify the token signature!
    Only use for debugging/logging purposes.

    Args:
        token: JWT token string

    Returns:
        Token payload as dict, or None if decoding fails
    """
    try:
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        return payload
    except Exception:
        return None
