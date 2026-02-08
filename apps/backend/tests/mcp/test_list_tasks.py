"""
Tests for list_tasks MCP Tool

[Task]: T024
[From]: specs/003-ai-chatbot/spec.md §3.2 (US2), specs/003-ai-chatbot/plan.md §Phase 4

Tests cover:
- List all tasks for authenticated user
- Filter tasks by status (all/completed/pending)
- User isolation
- Authentication validation
- Empty task list handling
"""

import pytest
from sqlmodel import Session

from app.models.user import User
from app.models.task import Task
from mcp_server.tools.list_tasks import list_tasks


class TestListTasks:
    """Test suite for list_tasks MCP tool"""

    @pytest.mark.asyncio
    async def test_list_tasks_returns_all_user_tasks(
        self,
        test_session: Session,
        test_user: User,
        test_jwt_token: str,
        multiple_test_tasks: list[Task]
    ):
        """Test that list_tasks returns all tasks for the user"""
        # Given: User has multiple tasks (3 tasks: 2 pending, 1 completed)

        # When: Call list_tasks with "all" filter
        result = await list_tasks(
            jwt_token=test_jwt_token,
            filter="all",
            session=test_session
        )

        # Then: Returns all 3 tasks
        assert result["success"] is True
        assert "tasks" in result
        assert len(result["tasks"]) == 3
        assert result["count"] == 3

    @pytest.mark.asyncio
    async def test_list_tasks_filters_completed_tasks(
        self,
        test_session: Session,
        test_user: User,
        test_jwt_token: str,
        multiple_test_tasks: list[Task]
    ):
        """Test that list_tasks filters completed tasks"""
        # Given: User has 3 tasks (1 completed, 2 pending)

        # When: Call list_tasks with "completed" filter
        result = await list_tasks(
            jwt_token=test_jwt_token,
            filter="completed",
            session=test_session
        )

        # Then: Returns only completed task
        assert result["success"] is True
        assert len(result["tasks"]) == 1
        assert result["count"] == 1
        assert result["tasks"][0]["completed"] is True

    @pytest.mark.asyncio
    async def test_list_tasks_filters_pending_tasks(
        self,
        test_session: Session,
        test_user: User,
        test_jwt_token: str,
        multiple_test_tasks: list[Task]
    ):
        """Test that list_tasks filters pending tasks"""
        # Given: User has 3 tasks (2 pending, 1 completed)

        # When: Call list_tasks with "pending" filter
        result = await list_tasks(
            jwt_token=test_jwt_token,
            filter="pending",
            session=test_session
        )

        # Then: Returns only pending tasks
        assert result["success"] is True
        assert len(result["tasks"]) == 2
        assert result["count"] == 2
        assert all(task["completed"] is False for task in result["tasks"])

    @pytest.mark.asyncio
    async def test_list_tasks_returns_empty_list_for_new_user(
        self,
        test_session: Session,
        test_jwt_token: str
    ):
        """Test that list_tasks returns empty list for user with no tasks"""
        # Given: User has no tasks

        # When: Call list_tasks
        result = await list_tasks(
            jwt_token=test_jwt_token,
            filter="all",
            session=test_session
        )

        # Then: Returns empty list
        assert result["success"] is True
        assert result["tasks"] == []
        assert result["count"] == 0

    @pytest.mark.asyncio
    async def test_list_tasks_enforces_user_isolation(
        self,
        test_session: Session,
        test_user: User,
        second_test_user: User,
        test_jwt_token: str,
        multiple_test_tasks: list[Task],
        other_user_task: Task
    ):
        """Test that list_tasks only returns tasks for authenticated user"""
        # Given: User 1 has 3 tasks, User 2 has 1 task

        # When: User 1 calls list_tasks
        result = await list_tasks(
            jwt_token=test_jwt_token,
            filter="all",
            session=test_session
        )

        # Then: Returns only User 1's tasks (3 tasks)
        assert result["success"] is True
        assert len(result["tasks"]) == 3
        assert all(task["user_id"] == test_user.id for task in result["tasks"])

        # Verify User 2's task is not included
        other_task_ids = [task["id"] for task in result["tasks"]]
        assert other_user_task.id not in other_task_ids

    @pytest.mark.asyncio
    async def test_list_tasks_rejects_invalid_token(
        self,
        test_session: Session,
        invalid_jwt_token: str
    ):
        """Test that list_tasks rejects invalid JWT token"""
        # Given: Invalid JWT token

        # When: Call list_tasks with invalid token
        result = await list_tasks(
            jwt_token=invalid_jwt_token,
            filter="all",
            session=test_session
        )

        # Then: Returns authentication error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "INVALID_TOKEN"

    @pytest.mark.asyncio
    async def test_list_tasks_rejects_expired_token(
        self,
        test_session: Session,
        expired_jwt_token: str
    ):
        """Test that list_tasks rejects expired JWT token"""
        # Given: Expired JWT token

        # When: Call list_tasks with expired token
        result = await list_tasks(
            jwt_token=expired_jwt_token,
            filter="all",
            session=test_session
        )

        # Then: Returns authentication error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "EXPIRED_TOKEN"

    @pytest.mark.asyncio
    async def test_list_tasks_defaults_to_all_filter(
        self,
        test_session: Session,
        test_jwt_token: str,
        multiple_test_tasks: list[Task]
    ):
        """Test that list_tasks defaults to 'all' filter when not specified"""
        # Given: User has tasks

        # When: Call list_tasks without specifying filter
        result = await list_tasks(
            jwt_token=test_jwt_token,
            session=test_session
        )

        # Then: Returns all tasks
        assert result["success"] is True
        assert len(result["tasks"]) == 3

    @pytest.mark.asyncio
    async def test_list_tasks_rejects_invalid_filter(
        self,
        test_session: Session,
        test_jwt_token: str
    ):
        """Test that list_tasks rejects invalid filter value"""
        # Given: Invalid filter value

        # When: Call list_tasks with invalid filter
        result = await list_tasks(
            jwt_token=test_jwt_token,
            filter="invalid_filter",
            session=test_session
        )

        # Then: Returns validation error
        assert result["success"] is False
        assert "error" in result
        assert result["error"]["code"] == "INVALID_INPUT"

    @pytest.mark.asyncio
    async def test_list_tasks_includes_task_details(
        self,
        test_session: Session,
        test_jwt_token: str,
        test_task: Task
    ):
        """Test that list_tasks includes all task details"""
        # Given: User has a task

        # When: Call list_tasks
        result = await list_tasks(
            jwt_token=test_jwt_token,
            filter="all",
            session=test_session
        )

        # Then: Task includes all fields
        assert result["success"] is True
        task = result["tasks"][0]

        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "user_id" in task
        assert "created_at" in task
        assert "updated_at" in task

        assert task["title"] == test_task.title
        assert task["id"] == test_task.id
