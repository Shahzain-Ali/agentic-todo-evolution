"""
Pytest Fixtures for MCP Tool Tests

[Task]: T018
[From]: specs/003-ai-chatbot/spec.md §Success Criteria, specs/003-ai-chatbot/plan.md §Testing Strategy

This module provides shared fixtures for testing MCP tools including:
- Test database setup
- JWT token generation
- Test user creation
- Database session management
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
from jose import jwt
from datetime import datetime, timedelta
from typing import Generator

from app.models.user import User
from app.models.task import Task
from mcp_server.config import config


@pytest.fixture(scope="function")
def test_engine():
    """
    Create in-memory SQLite database for testing
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    SQLModel.metadata.create_all(engine)

    yield engine

    # Cleanup
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_session(test_engine) -> Generator[Session, None, None]:
    """
    Create test database session
    """
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function")
def test_user(test_session: Session) -> User:
    """
    Create a test user in the database
    """
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyAa4F8OHgOy"  # hashed "testpassword"
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)

    return user


@pytest.fixture(scope="function")
def second_test_user(test_session: Session) -> User:
    """
    Create a second test user for testing user isolation
    """
    user = User(
        email="test2@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyAa4F8OHgOy"
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)

    return user


@pytest.fixture(scope="function")
def test_jwt_token(test_user: User) -> str:
    """
    Generate valid JWT token for test user
    """
    payload = {
        "user_id": test_user.id,
        "email": test_user.email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    token = jwt.encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )

    return token


@pytest.fixture(scope="function")
def second_user_jwt_token(second_test_user: User) -> str:
    """
    Generate valid JWT token for second test user
    """
    payload = {
        "user_id": second_test_user.id,
        "email": second_test_user.email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    token = jwt.encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )

    return token


@pytest.fixture(scope="function")
def expired_jwt_token(test_user: User) -> str:
    """
    Generate expired JWT token for testing authentication failures
    """
    payload = {
        "user_id": test_user.id,
        "email": test_user.email,
        "exp": datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago
    }

    token = jwt.encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )

    return token


@pytest.fixture(scope="function")
def invalid_jwt_token() -> str:
    """
    Generate invalid JWT token for testing authentication failures
    """
    return "invalid.jwt.token.format"


@pytest.fixture(scope="function")
def test_task(test_session: Session, test_user: User) -> Task:
    """
    Create a test task for the test user
    """
    task = Task(
        title="Test Task",
        description="This is a test task",
        completed=False,
        user_id=test_user.id
    )
    test_session.add(task)
    test_session.commit()
    test_session.refresh(task)

    return task


@pytest.fixture(scope="function")
def completed_test_task(test_session: Session, test_user: User) -> Task:
    """
    Create a completed test task
    """
    task = Task(
        title="Completed Test Task",
        description="This task is already completed",
        completed=True,
        user_id=test_user.id
    )
    test_session.add(task)
    test_session.commit()
    test_session.refresh(task)

    return task


@pytest.fixture(scope="function")
def multiple_test_tasks(test_session: Session, test_user: User) -> list[Task]:
    """
    Create multiple test tasks for testing list operations
    """
    tasks = [
        Task(title="Task 1", description="First task", completed=False, user_id=test_user.id),
        Task(title="Task 2", description="Second task", completed=True, user_id=test_user.id),
        Task(title="Task 3", description="Third task", completed=False, user_id=test_user.id),
    ]

    for task in tasks:
        test_session.add(task)

    test_session.commit()

    for task in tasks:
        test_session.refresh(task)

    return tasks


@pytest.fixture(scope="function")
def other_user_task(test_session: Session, second_test_user: User) -> Task:
    """
    Create a task belonging to a different user for testing user isolation
    """
    task = Task(
        title="Other User Task",
        description="This task belongs to a different user",
        completed=False,
        user_id=second_test_user.id
    )
    test_session.add(task)
    test_session.commit()
    test_session.refresh(task)

    return task
