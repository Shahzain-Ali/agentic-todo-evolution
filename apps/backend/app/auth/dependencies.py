from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from uuid import UUID

from app.models.user import User
from app.database import get_session
from app.auth.better_auth_jwt import verify_better_auth_token, extract_user_id_from_token

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
        # Verify Better Auth JWT token and extract user ID
        user_id_str = extract_user_id_from_token(token)

        if not user_id_str:
            raise credentials_exception

        # Try to parse as UUID (if using UUID primary keys)
        try:
            user_id = UUID(user_id_str)
            user = session.get(User, user_id)
        except ValueError:
            # If not UUID, query by email or other identifier
            # Better Auth might use email as user ID
            statement = select(User).where(User.email == user_id_str)
            user = session.exec(statement).first()

    except ValueError as e:
        # Better Auth JWT validation failed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        # Unexpected error
        raise credentials_exception

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Please register first.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

# Type annotation for dependency injection
CurrentUserDep = Annotated[User, Depends(get_current_user)]
