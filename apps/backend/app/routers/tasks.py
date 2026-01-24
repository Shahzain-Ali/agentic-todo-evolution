from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID

from app.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.auth.dependencies import CurrentUserDep

router = APIRouter()

# Type annotation for session dependency
SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Get all tasks for the authenticated user.

    - Requires valid JWT token
    - Returns tasks ordered by created_at DESC (newest first)
    - User isolation enforced (only returns current user's tasks)
    """
    statement = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
    )
    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Create a new task for the authenticated user.

    - Requires valid JWT token
    - Title is required (1-200 characters)
    - Description is optional (max 2000 characters)
    - Status defaults to 'pending'
    """
    db_task = Task.model_validate(task, update={"user_id": current_user.id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Update an existing task.

    - Requires valid JWT token
    - Only task owner can update
    - Supports partial updates (only provided fields are updated)
    """
    db_task = session.get(Task, task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update only provided fields
    task_data = task_update.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)

    # Update timestamp
    from datetime import datetime
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Delete a task.

    - Requires valid JWT token
    - Only task owner can delete
    - Returns success message
    """
    db_task = session.get(Task, task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}
