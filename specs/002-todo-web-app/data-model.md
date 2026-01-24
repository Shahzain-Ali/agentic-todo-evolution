# Data Model: Full-Stack Todo Application

**Feature**: 002-todo-web-app
**Date**: 2026-01-14
**Status**: Completed

## Overview

This document defines the database schema, entity relationships, and data validation rules for the todo application. The schema supports user authentication, task management, and user isolation.

## Entity Relationship Diagram

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ password_hash   │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐
│     Tasks       │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ title           │
│ description     │
│ status          │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

## Entities

### User Entity

**Purpose**: Represents a registered user account with authentication credentials.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier, auto-generated |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (login identifier) |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt-hashed password (never plain text) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for login lookups)

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Email must be unique across all users
- Password must be minimum 8 characters before hashing
- Password hash must use bcrypt with 12 salt rounds

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (not stored in database)
    tasks: list["Task"] = Relationship(back_populates="user")
```

**Security Considerations**:
- Password never stored in plain text
- Password hash never returned in API responses
- Email used as unique identifier (no username)
- Created_at for audit trail

### Task Entity

**Purpose**: Represents a todo item belonging to a specific user.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier, auto-generated |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Owner of the task |
| title | VARCHAR(200) | NOT NULL | Task title (required) |
| description | TEXT | NULL | Optional detailed description |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending', CHECK | Task status (pending or completed) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Task creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last modification timestamp |

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` (for user-specific queries)
- Index on `status` (for filtering by status)
- Composite index on `(user_id, status)` (for filtered user queries)

**Constraints**:
- Foreign key: `user_id` REFERENCES `users(id)` ON DELETE CASCADE
- Check constraint: `status IN ('pending', 'completed')`

**Validation Rules**:
- Title must not be empty (min 1 character)
- Title maximum 200 characters
- Description maximum 2000 characters
- Status must be either 'pending' or 'completed'
- User_id must reference existing user

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (not stored in database)
    user: Optional[User] = Relationship(back_populates="tasks")
```

**Business Rules**:
- Tasks are owned by exactly one user
- Users can have zero or many tasks
- Deleting a user cascades to delete all their tasks
- Tasks cannot be transferred between users
- Status can only be 'pending' or 'completed'

## Relationships

### User → Tasks (One-to-Many)

**Type**: One-to-Many

**Description**: Each user can have multiple tasks, but each task belongs to exactly one user.

**Implementation**:
- Foreign key constraint on `tasks.user_id` references `users.id`
- Cascade delete: When user is deleted, all their tasks are deleted
- Index on `user_id` for efficient queries

**Query Patterns**:
```python
# Get all tasks for a user
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# Get user with their tasks
user = session.exec(
    select(User).where(User.id == user_id)
).first()
tasks = user.tasks  # Via relationship
```

## Database Schema (SQL)

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### Tasks Table

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'completed')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

### Triggers (Optional - for updated_at)

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## Migration Strategy

### Initial Migration (001_initial_schema)

**Up Migration**:
```python
# alembic/versions/001_initial_schema.py
def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_status', 'tasks', ['status'])
    op.create_index('idx_tasks_user_status', 'tasks', ['user_id', 'status'])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

## Data Access Patterns

### Common Queries

**1. User Registration**:
```python
# Check if email exists
existing = session.exec(
    select(User).where(User.email == email)
).first()

# Create new user
user = User(email=email, password_hash=hashed_password)
session.add(user)
session.commit()
```

**2. User Login**:
```python
# Find user by email
user = session.exec(
    select(User).where(User.email == email)
).first()

# Verify password (in auth service)
if user and verify_password(password, user.password_hash):
    # Generate JWT token
```

**3. Get User's Tasks**:
```python
# All tasks for user
tasks = session.exec(
    select(Task)
    .where(Task.user_id == user_id)
    .order_by(Task.created_at.desc())
).all()

# Filter by status
pending_tasks = session.exec(
    select(Task)
    .where(Task.user_id == user_id, Task.status == TaskStatus.PENDING)
).all()
```

**4. Create Task**:
```python
task = Task(
    user_id=user_id,
    title=title,
    description=description
)
session.add(task)
session.commit()
session.refresh(task)
```

**5. Update Task**:
```python
# Verify ownership
task = session.exec(
    select(Task).where(Task.id == task_id, Task.user_id == user_id)
).first()

if task:
    task.title = new_title
    task.description = new_description
    task.status = new_status
    task.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(task)
```

**6. Delete Task**:
```python
# Verify ownership
task = session.exec(
    select(Task).where(Task.id == task_id, Task.user_id == user_id)
).first()

if task:
    session.delete(task)
    session.commit()
```

## Performance Considerations

### Indexes

**Primary Indexes** (automatic):
- `users.id` - Primary key lookup
- `tasks.id` - Primary key lookup

**Secondary Indexes** (explicit):
- `users.email` - Login queries (UNIQUE)
- `tasks.user_id` - User's tasks queries
- `tasks.status` - Status filtering
- `tasks(user_id, status)` - Combined filtering

**Query Optimization**:
- All user-specific queries use `user_id` index
- Status filtering uses composite index
- Email lookup uses unique index

### Connection Pooling

**Configuration**:
```python
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

**Best Practices**:
- Use async sessions for non-blocking I/O
- Close sessions after use
- Use context managers for automatic cleanup
- Monitor connection pool usage

## Data Validation

### Application-Level Validation (Pydantic)

**User Registration**:
```python
class UserCreate(BaseModel):
    email: EmailStr  # Validates email format
    password: str = Field(min_length=8, max_length=100)
```

**Task Creation**:
```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
```

**Task Update**:
```python
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = None
```

### Database-Level Validation

- NOT NULL constraints on required fields
- UNIQUE constraint on email
- CHECK constraint on status enum
- Foreign key constraint on user_id
- Length constraints on VARCHAR fields

## Security Considerations

### User Isolation

**Enforcement**:
- All task queries filtered by `user_id` from JWT token
- User_id never accepted from request body
- 403 Forbidden if user attempts to access another user's task

**Implementation**:
```python
# Extract user_id from JWT token
current_user = Depends(get_current_user)

# Query with user_id filter
task = session.exec(
    select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id  # Enforce ownership
    )
).first()
```

### Password Security

- Passwords hashed with bcrypt (12 rounds)
- Password hash never returned in API responses
- Password validation before hashing
- No password recovery (out of scope)

### Data Integrity

- Foreign key constraints prevent orphaned tasks
- Cascade delete ensures cleanup
- Transactions for multi-step operations
- Unique constraints prevent duplicates

## Testing Data

### Test Fixtures

**Test Users**:
```python
@pytest.fixture
def test_user(session):
    user = User(
        email="test@example.com",
        password_hash=hash_password("testpassword123")
    )
    session.add(user)
    session.commit()
    return user
```

**Test Tasks**:
```python
@pytest.fixture
def test_tasks(session, test_user):
    tasks = [
        Task(user_id=test_user.id, title="Task 1", status=TaskStatus.PENDING),
        Task(user_id=test_user.id, title="Task 2", status=TaskStatus.COMPLETED),
    ]
    for task in tasks:
        session.add(task)
    session.commit()
    return tasks
```

## Summary

The data model provides:
- **Simplicity**: Only 2 tables with clear relationship
- **Security**: User isolation, password hashing, foreign key constraints
- **Performance**: Appropriate indexes for common queries
- **Scalability**: UUID primary keys, connection pooling
- **Maintainability**: Type-safe models, validation, migrations

**Next Steps**: Create API contracts documentation.
