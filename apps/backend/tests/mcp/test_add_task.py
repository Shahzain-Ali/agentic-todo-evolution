"""
Tests for add_task MCP Tool

[Task]: T019
[From]: specs/003-ai-chatbot/spec.md §3.1 (US1), specs/003-ai-chatbot/plan.md §Phase 3

Tests cover:
- Successful task creation with valid JWT
- Task creation with title and description
- Authentication validation
- User isolation
- Input validation
"""

import pytest
from sqlmodel import Session, select

from app.models.task import Task
from app.models.user import User
from mcp_server.tools.add_task import add_task


class TestAddTask:
    """Test suite for add_task MCP tool"""

    @pytest.mark.asyncio
    async def test_add_task_creates_task_for_authenticated_user(
        self,
        test_session: Session,
        test_user: User,
        test_jwt_token: str
    ):
        """Test that add_task creates a task for authenticated user"""
        # Given: Valid JWT token and task details
        title = "Buy groceries"
        description = "Milk, eggs, bread"

        # When: Call add_task tool
        result = await add_task(
            jwt_token=test_jwt_token,
            title=title,
            description=description,
            session=test_session
        )

        # Then: Task created successfully
        assert result["success"] is True
        assert "task" in result
        assert result["task"]["title"] == title
        assert result["task"]["description"] == description
        assert result["task"]["completed"] is False
        assert result["task"]["user_id"] == test_user.id

        # Verify task in database
        statement = select(Task).where(Task.user_id == test_user.id)
        tasks = test_session.exec(statement).all()
        assert len(tasks) == 1
        assert tasks[0].title == title

    @pytest.mark.asyncio
    async def test_add_task_with_title_only(
        self,
        test_session: Session,
        test_user: User,
        test_jwt_token: str
    ):
        """Test task creation with only title (no description)"""
        # Given: Valid JWT and only title
        title = "Call mom"

        # When: Call add_task without description
        result = await add_task(
            jwt_token=test_jwt_token,
            title=title,
            session=test_session
        )

        # Then: Task created with empty description
        assert result["success"] is True
        assert result["task"]["title"] == title
        assert result["task"]["description"] in [None, ""]

    @pytest.mark.asyncio
    async def test_add_task_rejects_invalid_token(
        self,
        test_session: Session,
        invalid_jwt_token: str
    ):
        """Test that add_task rejects invalid JWT token"""
        # Given: Invalid JWT token
        title = "Test task"

        # When: Call add_task with invalid token
        result = await add_task(
            jwt_token=invalid_jwt_token,
            title=title,
            session=test_session
        )

        # Then: Returns error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "INVALID_TOKEN"

        # Verify no task created
        statement = select(Task)
        tasks = test_session.exec(statement).all()
        assert len(tasks) == 0

    @pytest.mark.asyncio
    async def test_add_task_rejects_expired_token(
        self,
        test_session: Session,
        expired_jwt_token: str
    ):
        """Test that add_task rejects expired JWT token"""
        # Given: Expired JWT token
        title = "Test task"

        # When: Call add_task with expired token
        result = await add_task(
            jwt_token=expired_jwt_token,
            title=title,
            session=test_session
        )

        # Then: Returns error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "EXPIRED_TOKEN"

    @pytest.mark.asyncio
    async def test_add_task_rejects_missing_token(
        self,
        test_session: Session
    ):
        """Test that add_task rejects missing JWT token"""
        # Given: No JWT token
        title = "Test task"

        # When: Call add_task without token
        result = await add_task(
            jwt_token="",
            title=title,
            session=test_session
        )

        # Then: Returns error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "MISSING_TOKEN"

    @pytest.mark.asyncio
    async def test_add_task_rejects_empty_title(
        self,
        test_session: Session,
        test_jwt_token: str
    ):
        """Test that add_task rejects empty title"""
        # Given: Valid token but empty title
        title = ""

        # When: Call add_task with empty title
        result = await add_task(
            jwt_token=test_jwt_token,
            title=title,
            session=test_session
        )

        # Then: Returns validation error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "INVALID_INPUT"

    @pytest.mark.asyncio
    async def test_add_task_enforces_user_isolation(
        self,
        test_session: Session,
        test_user: User,
        second_test_user: User,
        test_jwt_token: str,
        second_user_jwt_token: str
    ):
        """Test that tasks are isolated by user"""
        # Given: Two different users
        user1_title = "User 1 task"
        user2_title = "User 2 task"

        # When: Each user creates a task
        result1 = await add_task(
            jwt_token=test_jwt_token,
            title=user1_title,
            session=test_session
        )

        result2 = await add_task(
            jwt_token=second_user_jwt_token,
            title=user2_title,
            session=test_session
        )

        # Then: Both tasks created with correct user_ids
        assert result1["success"] is True
        assert result1["task"]["user_id"] == test_user.id

        assert result2["success"] is True
        assert result2["task"]["user_id"] == second_test_user.id

        # Verify tasks in database
        user1_tasks = test_session.exec(
            select(Task).where(Task.user_id == test_user.id)
        ).all()
        user2_tasks = test_session.exec(
            select(Task).where(Task.user_id == second_test_user.id)
        ).all()

        assert len(user1_tasks) == 1
        assert len(user2_tasks) == 1
        assert user1_tasks[0].title == user1_title
        assert user2_tasks[0].title == user2_title

    @pytest.mark.asyncio
    async def test_add_task_handles_long_title(
        self,
        test_session: Session,
        test_jwt_token: str
    ):
        """Test task creation with maximum length title"""
        # Given: Title at maximum length (200 chars)
        title = "A" * 200

        # When: Call add_task with long title
        result = await add_task(
            jwt_token=test_jwt_token,
            title=title,
            session=test_session
        )

        # Then: Task created successfully
        assert result["success"] is True
        assert result["task"]["title"] == title

    @pytest.mark.asyncio
    async def test_add_task_rejects_title_exceeding_max_length(
        self,
        test_session: Session,
        test_jwt_token: str
    ):
        """Test that add_task rejects title exceeding 200 characters"""
        # Given: Title exceeding maximum length
        title = "A" * 201

        # When: Call add_task with too-long title
        result = await add_task(
            jwt_token=test_jwt_token,
            title=title,
            session=test_session
        )

        # Then: Returns validation error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "INVALID_INPUT"
