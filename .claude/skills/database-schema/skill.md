# Database Schema Skill

**Version**: 1.0.0
**Created**: 2026-01-14
**Feature**: 002-todo-web-app
**Owner**: database-subagent

## Purpose

This skill enables designing and managing database schemas using SQLModel 0.14+ with PostgreSQL 15+, Alembic migrations, and proper relationship modeling. It provides patterns, best practices, and code generation capabilities for robust data persistence layers.

## Scope

### In Scope
- SQLModel 0.14+ table model definitions
- Database relationships (one-to-many, many-to-many)
- Field types, constraints, and indexes
- Alembic migration management
- Query patterns and optimization
- Database session management
- Data validation and integrity

### Out of Scope
- Frontend implementation (see `frontend-builder` skill)
- API endpoint implementation (see `backend-api` skill)
- Database deployment and infrastructure
- Testing implementation (handled during implementation phase)

## Technical Context

### Technology Stack
- **ORM**: SQLModel 0.14+ (built on SQLAlchemy 2.0+)
- **Database**: PostgreSQL 15+ (Neon Serverless)
- **Migrations**: Alembic 1.11+
- **Validation**: Pydantic v2 (integrated in SQLModel)
- **Connection**: psycopg2-binary

### Project Structure

```
apps/backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User table model
│   │   └── task.py                 # Task table model
│   └── database.py                 # Engine and session config
├── alembic/
│   ├── versions/
│   │   └── xxxx_initial_schema.py  # Migration files
│   ├── env.py                      # Alembic environment
│   └── script.py.mako              # Migration template
├── alembic.ini                     # Alembic configuration
└── .env                            # Database credentials
```

## Key Patterns

### 1. Table Model Definition

**Basic Table Model** (`app/models/user.py`):
```python
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"

    # Primary key with UUID
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Unique indexed field
    email: str = Field(max_length=255, unique=True, index=True)

    # Non-nullable field
    password_hash: str = Field(max_length=255)

    # Timestamp with default
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (one-to-many)
    tasks: List["Task"] = Relationship(back_populates="user")
```

**Field Types and Constraints**:
```python
from decimal import Decimal
from sqlmodel import Field

class Example(SQLModel, table=True):
    # String with length constraint
    name: str = Field(min_length=1, max_length=100)

    # Optional field (nullable)
    description: Optional[str] = Field(default=None, max_length=500)

    # Integer with range
    age: int = Field(ge=0, le=150)

    # Decimal for financial data
    price: Decimal = Field(max_digits=10, decimal_places=2)

    # Boolean with default
    is_active: bool = Field(default=True)

    # Enum-like field
    status: str = Field(pattern="^(pending|active|completed)$")

    # Indexed field for faster queries
    user_id: UUID = Field(foreign_key="users.id", index=True)
```

### 2. Relationship Patterns

**One-to-Many Relationship**:
```python
# Parent model
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)

    # One user has many tasks
    tasks: List["Task"] = Relationship(back_populates="user")

# Child model
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200)

    # Foreign key to parent
    user_id: UUID = Field(foreign_key="users.id", index=True)

    # Relationship back to parent
    user: Optional[User] = Relationship(back_populates="tasks")
```

**Cascade Delete Configuration**:
```python
class Task(SQLModel, table=True):
    # Database-level cascade delete
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        ondelete="CASCADE"  # Delete tasks when user is deleted
    )

    # Python-level cascade (optional)
    user: Optional[User] = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

**Many-to-Many Relationship** (if needed in future):
```python
# Link table
class UserTeamLink(SQLModel, table=True):
    __tablename__ = "user_team_links"
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    team_id: UUID = Field(foreign_key="teams.id", primary_key=True)

    # Optional: additional fields
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    role: str = Field(default="member")

# User model
class User(SQLModel, table=True):
    teams: List["Team"] = Relationship(
        back_populates="users",
        link_model=UserTeamLink
    )

# Team model
class Team(SQLModel, table=True):
    users: List[User] = Relationship(
        back_populates="teams",
        link_model=UserTeamLink
    )
```

### 3. Database Engine and Session

**Engine Configuration** (`app/database.py`):
```python
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

# PostgreSQL connection string
DATABASE_URL = "postgresql://user:password@host:5432/dbname"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Additional connections when pool is full
    pool_recycle=3600  # Recycle connections after 1 hour
)

def create_db_and_tables():
    """Create all tables (use only for development/testing)"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for FastAPI to get database session"""
    with Session(engine) as session:
        yield session
```

**Session Usage in FastAPI**:
```python
from typing import Annotated
from fastapi import Depends
from app.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/tasks/")
def create_task(task: TaskCreate, session: SessionDep):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### 4. Query Patterns

**Basic Queries**:
```python
from sqlmodel import select, Session

# Get all records
def get_all_tasks(session: Session) -> List[Task]:
    statement = select(Task)
    tasks = session.exec(statement).all()
    return tasks

# Get by primary key
def get_task_by_id(session: Session, task_id: UUID) -> Optional[Task]:
    task = session.get(Task, task_id)
    return task

# Filter with WHERE clause
def get_user_tasks(session: Session, user_id: UUID) -> List[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

# Multiple conditions (AND)
def get_completed_tasks(session: Session, user_id: UUID) -> List[Task]:
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.status == "completed"
    )
    tasks = session.exec(statement).all()
    return tasks

# OR conditions
from sqlmodel import or_

def get_active_or_pending_tasks(session: Session, user_id: UUID) -> List[Task]:
    statement = select(Task).where(
        Task.user_id == user_id,
        or_(Task.status == "pending", Task.status == "in_progress")
    )
    tasks = session.exec(statement).all()
    return tasks
```

**Pagination**:
```python
def get_tasks_paginated(
    session: Session,
    user_id: UUID,
    offset: int = 0,
    limit: int = 20
) -> List[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .offset(offset)
        .limit(limit)
    )
    tasks = session.exec(statement).all()
    return tasks
```

**Ordering**:
```python
def get_tasks_ordered(session: Session, user_id: UUID) -> List[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())  # Most recent first
    )
    tasks = session.exec(statement).all()
    return tasks
```

**Counting**:
```python
from sqlmodel import func

def count_user_tasks(session: Session, user_id: UUID) -> int:
    statement = select(func.count(Task.id)).where(Task.user_id == user_id)
    count = session.exec(statement).one()
    return count
```

**Working with Relationships**:
```python
# Access related data (automatic fetching)
def get_user_with_tasks(session: Session, user_id: UUID) -> Optional[User]:
    user = session.get(User, user_id)
    if user:
        # Access tasks through relationship
        print(f"User has {len(user.tasks)} tasks")
        for task in user.tasks:
            print(task.title)
    return user

# Eager loading to avoid N+1 queries
from sqlalchemy.orm import selectinload

def get_users_with_tasks(session: Session) -> List[User]:
    statement = select(User).options(selectinload(User.tasks))
    users = session.exec(statement).all()
    return users
```

### 5. CRUD Operations

**Create**:
```python
def create_task(session: Session, task_data: TaskCreate, user_id: UUID) -> Task:
    db_task = Task.model_validate(task_data, update={"user_id": user_id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)  # Get updated data from DB
    return db_task
```

**Read**:
```python
def get_task(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # User isolation
    )
    task = session.exec(statement).first()
    return task
```

**Update**:
```python
def update_task(
    session: Session,
    task_id: UUID,
    task_update: TaskUpdate,
    user_id: UUID
) -> Optional[Task]:
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        return None

    # Update only provided fields
    task_data = task_update.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

**Delete**:
```python
def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        return False

    session.delete(db_task)
    session.commit()
    return True
```

### 6. Alembic Migrations

**Initialize Alembic** (first time only):
```bash
cd apps/backend
alembic init alembic
```

**Configure Alembic** (`alembic/env.py`):
```python
from sqlmodel import SQLModel
from app.models.user import User
from app.models.task import Task
from app.database import DATABASE_URL

# Set target metadata
target_metadata = SQLModel.metadata

# Set database URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)
```

**Generate Migration**:
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add tasks table"

# Create empty migration (for data migrations)
alembic revision -m "Seed initial data"
```

**Apply Migrations**:
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# View migration history
alembic history

# View current revision
alembic current
```

**Migration File Example**:
```python
"""Add tasks table

Revision ID: abc123
Revises: def456
Create Date: 2026-01-14 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=2000), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])

def downgrade() -> None:
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
```

## Best Practices

### Model Design
1. **Use UUIDs for primary keys** - Better for distributed systems and security
2. **Add indexes strategically** - Index foreign keys and frequently queried fields
3. **Set appropriate field lengths** - Prevent excessive storage usage
4. **Use proper field types** - Decimal for money, DateTime for timestamps
5. **Define relationships clearly** - Use back_populates for bidirectional relationships

### Data Integrity
1. **Foreign key constraints** - Ensure referential integrity
2. **Unique constraints** - Prevent duplicate data (e.g., email)
3. **NOT NULL constraints** - Use Optional[] for nullable fields
4. **Check constraints** - Use Field validators for business rules
5. **Cascade deletes** - Define deletion behavior explicitly

### Performance
1. **Avoid N+1 queries** - Use selectinload/joinedload for relationships
2. **Use pagination** - Don't load all records at once
3. **Index frequently queried fields** - Speed up WHERE clauses
4. **Connection pooling** - Reuse database connections
5. **Batch operations** - Use session.add_all() for multiple inserts

### Migrations
1. **Always use migrations** - Never modify database schema manually
2. **Review auto-generated migrations** - Verify before applying
3. **Test migrations** - Apply to test database first
4. **Keep migrations small** - One logical change per migration
5. **Never edit applied migrations** - Create new migration to fix issues

### Security
1. **User isolation** - Always filter by user_id for user-specific data
2. **Validate input** - Use Pydantic validators in models
3. **Sanitize queries** - SQLModel prevents SQL injection by default
4. **Secure credentials** - Use environment variables for DATABASE_URL
5. **Least privilege** - Database user should have minimal required permissions

## Common Tasks

### Task 1: Add New Table Model
1. Create model file in `app/models/`
2. Define SQLModel class with `table=True`
3. Add fields with appropriate types and constraints
4. Define relationships if needed
5. Generate Alembic migration
6. Apply migration to database

### Task 2: Add Field to Existing Model
1. Add field to model class
2. Generate migration: `alembic revision --autogenerate -m "Add field"`
3. Review migration file
4. Apply migration: `alembic upgrade head`

### Task 3: Create Relationship
1. Add foreign key field to child model
2. Add Relationship field to both models
3. Use back_populates for bidirectional relationship
4. Generate and apply migration

### Task 4: Optimize Query Performance
1. Identify slow queries (use echo=True during development)
2. Add indexes to frequently queried fields
3. Use eager loading for relationships
4. Implement pagination for large result sets

## Environment Variables

Required in `.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

## Dependencies

Core dependencies in `requirements.txt`:
```
sqlmodel==0.14.0
psycopg2-binary==2.9.7
alembic==1.11.0
```

## Testing Strategy

- **Unit Tests**: Test model validation and relationships
- **Integration Tests**: Test CRUD operations with test database
- **Migration Tests**: Verify migrations apply and rollback correctly
- **Performance Tests**: Test query performance with realistic data volumes

## References

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Last Updated**: 2026-01-14
**Status**: Active
**Maintainer**: Development Team
