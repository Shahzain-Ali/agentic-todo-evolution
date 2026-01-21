from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import timedelta

from app.database import get_session
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, Token
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

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
