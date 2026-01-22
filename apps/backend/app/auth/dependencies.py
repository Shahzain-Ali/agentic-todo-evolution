from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from uuid import UUID

from app.models.user import User
from app.database import get_session
from app.auth.jwt import decode_access_token

# OAuth2 scheme for token extraction
# Note: tokenUrl is not used anymore since Better Auth handles authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/[...all]")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)]
) -> User:
    """
    Dependency to get the current authenticated user from Better Auth JWT token.

    This function validates JWT tokens issued by Better Auth (frontend)
    and retrieves the corresponding user from the database.

    Args:
        token: JWT token from Authorization header (Better Auth token)
        session: Database session

    Returns:
        User object for the authenticated user

    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # Decode JWT token and extract user ID from 'sub' claim
        payload = decode_access_token(token)
        user_id_str: str = payload.get("sub")

        if not user_id_str:
            raise credentials_exception

        # Parse as UUID
        user_id = UUID(user_id_str)
        user = session.get(User, user_id)

    except ValueError as e:
        # JWT validation failed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Please register first.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

# Type annotation for dependency injection
CurrentUserDep = Annotated[User, Depends(get_current_user)]
