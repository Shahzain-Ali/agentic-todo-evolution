from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session, select
from datetime import timedelta
from pydantic import BaseModel
from uuid import UUID

from app.database import get_session
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, Token
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# Better Auth compatible schemas
class BetterAuthSignUp(BaseModel):
    name: str
    email: str
    password: str
    image: str | None = None
    callbackURL: str | None = None

class BetterAuthSignIn(BaseModel):
    email: str
    password: str
    rememberMe: bool = True
    callbackURL: str | None = None

class BetterAuthSession(BaseModel):
    token: str
    expiresAt: str | None = None

class BetterAuthResponse(BaseModel):
    user: UserResponse
    session: BetterAuthSession

# Type annotation for session dependency
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, session: SessionDep):
    """
    Register a new user account.

    - Validates email uniqueness
    - Hashes password with bcrypt
    - Creates user record in database
    - Returns user object (without password)
    """
    # Check if email already exists
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create new user
    db_user = User(
        email=user.email,
        password_hash=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.post("/login", response_model=Token)
def login(user: UserCreate, session: SessionDep):
    """
    Authenticate user and return JWT token.

    - Validates email and password
    - Generates JWT token with 24-hour expiration
    - Returns access token
    """
    # Find user by email
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()

    # Verify credentials
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


# ============================================================================
# Better Auth Compatible Endpoints
# ============================================================================

@router.post("/sign-up/email", response_model=BetterAuthResponse, status_code=status.HTTP_201_CREATED)
def better_auth_signup(user_data: BetterAuthSignUp, session: SessionDep):
    """
    Better Auth compatible sign-up endpoint.

    Endpoint: POST /sign-up/email
    Expected by Better Auth client when calling authClient.signUp.email()

    Returns: { user: {...}, session: { token: "..." } }
    """
    # Check if email already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Create new user (Note: Better Auth sends 'name', but our User model doesn't have it)
    # For now, we'll just use email-based name, or you can update User model to include name
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Create access token for auto-login after registration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )

    # Return Better Auth compatible response
    return BetterAuthResponse(
        user=UserResponse.model_validate(db_user),
        session=BetterAuthSession(
            token=access_token,
            expiresAt=None  # Can add expiration timestamp if needed
        )
    )


@router.post("/sign-in/email", response_model=BetterAuthResponse)
def better_auth_signin(user_data: BetterAuthSignIn, session: SessionDep):
    """
    Better Auth compatible sign-in endpoint.

    Endpoint: POST /sign-in/email
    Expected by Better Auth client when calling authClient.signIn.email()

    Returns: { user: {...}, session: { token: "..." } }
    """
    # Find user by email
    statement = select(User).where(User.email == user_data.email)
    db_user = session.exec(statement).first()

    # Verify credentials
    if not db_user or not verify_password(user_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )

    # Return Better Auth compatible response
    return BetterAuthResponse(
        user=UserResponse.model_validate(db_user),
        session=BetterAuthSession(
            token=access_token,
            expiresAt=None  # Can add expiration timestamp if needed
        )
    )


# ============================================================================
# Session Verification Endpoint
# ============================================================================

class SessionResponse(BaseModel):
    session: Optional[BetterAuthSession] = None
    user: Optional[UserResponse] = None


@router.get("/session", response_model=SessionResponse)
def get_session_info(
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session)
):
    """
    Verify session token and return user info.

    Used by Better Auth client to check session status.
    """
    if not authorization:
        return SessionResponse(session=None, user=None)

    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return SessionResponse(session=None, user=None)
    except ValueError:
        return SessionResponse(session=None, user=None)

    # Decode and verify token
    try:
        payload = decode_access_token(token)
        if payload is None:
            return SessionResponse(session=None, user=None)

        user_id_str = payload.get("sub")
        if not user_id_str:
            return SessionResponse(session=None, user=None)

        # Get user from database
        user_id = UUID(user_id_str)
        db_user = session.get(User, user_id)

        if not db_user:
            return SessionResponse(session=None, user=None)

        return SessionResponse(
            session=BetterAuthSession(token=token, expiresAt=None),
            user=UserResponse.model_validate(db_user)
        )
    except Exception:
        return SessionResponse(session=None, user=None)
