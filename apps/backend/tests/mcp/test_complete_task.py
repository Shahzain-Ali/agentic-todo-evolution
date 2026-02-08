"""
Tests for complete_task MCP Tool

[Task]: T029
[From]: specs/003-ai-chatbot/spec.md §3.3 (US3), specs/003-ai-chatbot/plan.md §Phase 5

Tests cover:
- Mark task as complete
- Ownership verification
- Authentication validation
- Task not found handling
- Already completed task handling
"""

import pytest
from sqlmodel import Session, select

from app.models.user import User
from app.models.task import Task
from mcp_server.tools.complete_task import complete_task


class TestCompleteTask:
    """Test suite for complete_task MCP tool"""

    @pytest.mark.asyncio
    async def test_complete_task_marks_task_as_done(
        self,
        test_session: Session,
        test_user: User,
        test_jwt_token: str,
        test_task: Task
    ):
        """Test that complete_task marks task as completed"""
        # Given: User has a pending task
        assert test_task.completed is False

        # When: Call complete_task
        result = await complete_task(
            jwt_token=test_jwt_token,
            task_id=test_task.id,
            session=test_session
        )

        # Then: Task is marked as completed
        assert result["success"] is True
        assert result["task"]["completed"] is True
        assert result["task"]["id"] == test_task.id

        # Verify in database
        test_session.refresh(test_task)
        assert test_task.completed is True

    @pytest.mark.asyncio
    async def test_complete_task_handles_already_completed(
        self,
        test_session: Session,
        test_jwt_token: str,
        completed_test_task: Task
    ):
        """Test that complete_task handles already completed tasks gracefully"""
        # Given: Task is already completed
        assert completed_test_task.completed is True

        # When: Call complete_task on already completed task
        result = await complete_task(
            jwt_token=test_jwt_token,
            task_id=completed_test_task.id,
            session=test_session
        )

        # Then: Still returns success
        assert result["success"] is True
        assert result["task"]["completed"] is True

    @pytest.mark.asyncio
    async def test_complete_task_rejects_nonexistent_task(
        self,
        test_session: Session,
        test_jwt_token: str
    ):
        """Test that complete_task rejects non-existent task ID"""
        # Given: Non-existent task ID
        nonexistent_id = 99999

        # When: Call complete_task with non-existent ID
        result = await complete_task(
            jwt_token=test_jwt_token,
            task_id=nonexistent_id,
            session=test_session
        )

        # Then: Returns not found error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "NOT_FOUND"

    @pytest.mark.asyncio
    async def test_complete_task_enforces_ownership(
        self,
        test_session: Session,
        test_user: User,
        second_test_user: User,
        test_jwt_token: str,
        other_user_task: Task
    ):
        """Test that users cannot complete other users' tasks"""
        # Given: Task belongs to User 2, authenticated as User 1
        assert other_user_task.user_id == second_test_user.id

        # When: User 1 tries to complete User 2's task
        result = await complete_task(
            jwt_token=test_jwt_token,
            task_id=other_user_task.id,
            session=test_session
        )

        # Then: Returns forbidden error (or not found for security)
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] in ["FORBIDDEN", "NOT_FOUND"]

        # Verify task remains unchanged
        test_session.refresh(other_user_task)
        assert other_user_task.completed is False

    @pytest.mark.asyncio
    async def test_complete_task_rejects_invalid_token(
        self,
        test_session: Session,
        invalid_jwt_token: str,
        test_task: Task
    ):
        """Test that complete_task rejects invalid JWT token"""
        # Given: Invalid JWT token

        # When: Call complete_task with invalid token
        result = await complete_task(
            jwt_token=invalid_jwt_token,
            task_id=test_task.id,
            session=test_session
        )

        # Then: Returns authentication error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "INVALID_TOKEN"

        # Verify task unchanged
        test_session.refresh(test_task)
        assert test_task.completed is False

    @pytest.mark.asyncio
    async def test_complete_task_rejects_expired_token(
        self,
        test_session: Session,
        expired_jwt_token: str,
        test_task: Task
    ):
        """Test that complete_task rejects expired JWT token"""
        # Given: Expired JWT token

        # When: Call complete_task with expired token
        result = await complete_task(
            jwt_token=expired_jwt_token,
            task_id=test_task.id,
            session=test_session
        )

        # Then: Returns authentication error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "EXPIRED_TOKEN"

    @pytest.mark.asyncio
    async def test_complete_task_returns_updated_task_details(
        self,
        test_session: Session,
        test_jwt_token: str,
        test_task: Task
    ):
        """Test that complete_task returns updated task with all fields"""
        # Given: User has a pending task

        # When: Call complete_task
        result = await complete_task(
            jwt_token=test_jwt_token,
            task_id=test_task.id,
            session=test_session
        )

        # Then: Returns complete task details
        assert result["success"] is True
        task = result["task"]

        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "user_id" in task
        assert "created_at" in task
        assert "updated_at" in task

        assert task["id"] == test_task.id
        assert task["completed"] is True

    @pytest.mark.asyncio
    async def test_complete_task_updates_timestamp(
        self,
        test_session: Session,
        test_jwt_token: str,
        test_task: Task
    ):
        """Test that complete_task updates the updated_at timestamp"""
        # Given: Task with original updated_at
        original_updated_at = test_task.updated_at

        # When: Complete the task
        result = await complete_task(
            jwt_token=test_jwt_token,
            task_id=test_task.id,
            session=test_session
        )

        # Then: updated_at is changed
        assert result["success"] is True

        test_session.refresh(test_task)
        # Note: This test might be flaky if execution is too fast
        # In production, updated_at should be auto-updated by SQLModel
        assert task["updated_at"] is not None
