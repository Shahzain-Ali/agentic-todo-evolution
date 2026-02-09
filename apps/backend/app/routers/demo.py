"""
Demo API endpoints - No authentication required
For chatbot integration testing
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID

from app.database import get_session
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]

# Demo user UUID
DEMO_USER_ID = UUID("625460a4-b5f7-4c64-ba84-66da5dabfd3c")


@router.get("/tasks", response_model=List[TaskResponse])
def get_demo_tasks(session: SessionDep):
    """Get all tasks for demo user (no auth required)"""
    statement = (
        select(Task)
        .where(Task.user_id == DEMO_USER_ID)
        .order_by(Task.created_at.desc())
    )
    tasks = session.exec(statement).all()
    return tasks


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_demo_task(task: TaskCreate, session: SessionDep):
    """Create a new task for demo user (no auth required)"""
    db_task = Task.model_validate(task, update={"user_id": DEMO_USER_ID})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_demo_task(task_id: UUID, task_update: TaskUpdate, session: SessionDep):
    """Update a task for demo user (no auth required)"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == DEMO_USER_ID)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
