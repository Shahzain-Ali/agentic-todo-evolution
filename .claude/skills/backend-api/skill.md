# Backend API Skill

**Version**: 1.0.0
**Created**: 2026-01-14
**Feature**: 002-todo-web-app
**Owner**: backend-subagent

## Purpose

This skill enables building FastAPI 0.100+ backend applications with JWT authentication, SQLModel database integration, and RESTful API design. It provides patterns, best practices, and code generation capabilities for secure, scalable backend services.

## Scope

### In Scope
- FastAPI 0.100+ application structure with routers
- JWT authentication with OAuth2PasswordBearer
- SQLModel database integration with dependency injection
- RESTful API endpoint design (CRUD operations)
- Request/response validation with Pydantic v2
- Error handling and HTTP exceptions
- CORS configuration for frontend integration
- Password hashing with bcrypt
- Middleware and security utilities

### Out of Scope
- Frontend implementation (see `frontend-builder` skill)
- Database schema design (see `database-schema` skill)
- DevOps and deployment configuration
- Testing implementation (handled during implementation phase)

## Technical Context

### Technology Stack
- **Framework**: FastAPI 0.100+
- **ORM**: SQLModel 0.14+ (built on SQLAlchemy)
- **Validation**: Pydantic v2
- **Authentication**: JWT with python-jose
- **Password Hashing**: passlib with bcrypt
- **Database**: PostgreSQL 15+ (Neon Serverless)
- **ASGI Server**: Uvicorn

### Project Structure

```
apps/backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app initialization
│   ├── config.py                   # Configuration settings
│   ├── database.py                 # Database engine and session
│   ├── dependencies.py             # Shared dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User SQLModel
│   │   └── task.py                 # Task SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                 # User Pydantic schemas
│   │   ├── task.py                 # Task Pydantic schemas
│   │   └── token.py                # Auth token schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication endpoints
│   │   └── tasks.py                # Task CRUD endpoints
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── security.py             # Password hashing, JWT utilities
│   │   └── dependencies.py         # Auth dependencies (get_current_user)
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py           # Custom exception handlers
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
├── alembic.ini
├── requirements.txt
└── .env
```

## Key Patterns

### 1. Application Initialization

**Main Application** (`app/main.py`):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tasks
from app.database import create_db_and_tables

app = FastAPI(
    title="Todo API",
    description="Full-stack todo application API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### 2. Database Session Management

**Database Configuration** (`app/database.py`):
```python
from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "postgresql://user:password@host:5432/dbname"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Type annotation for dependency injection
SessionDep = Annotated[Session, Depends(get_session)]
```

**Usage in Endpoints**:
```python
@router.post("/tasks/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    session: SessionDep,
    current_user: CurrentUserDep
):
    db_task = Task.model_validate(task, update={"user_id": current_user.id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### 3. JWT Authentication Pattern

**Security Utilities** (`app/auth/security.py`):
```python
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-here"  # Use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
```

**Authentication Dependencies** (`app/auth/dependencies.py`):
```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session, select
from app.models.user import User
from app.database import get_session
from app.auth.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user

# Type annotation for dependency injection
CurrentUserDep = Annotated[User, Depends(get_current_user)]
```

### 4. Router Pattern with Authentication

**Authentication Router** (`app/routers/auth.py`):
```python
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from app.database import SessionDep
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.auth.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, session: SessionDep):
    # Check if user exists
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password_hash=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    # Authenticate user
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
```

**Protected Resource Router** (`app/routers/tasks.py`):
```python
from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.database import SessionDep
from app.auth.dependencies import CurrentUserDep
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

@router.get("/", response_model=List[TaskResponse])
def get_tasks(session: SessionDep, current_user: CurrentUserDep):
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: SessionDep,
    current_user: CurrentUserDep
):
    db_task = Task.model_validate(task, update={"user_id": current_user.id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    session: SessionDep,
    current_user: CurrentUserDep
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update only provided fields
    task_data = task_update.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    session: SessionDep,
    current_user: CurrentUserDep
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(db_task)
    session.commit()
    return None
```

### 5. Pydantic Schema Separation

**Request/Response Schemas** (`app/schemas/task.py`):
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[str] = Field(default=None, pattern="^(pending|in_progress|completed)$")

class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### 6. Error Handling

**Custom Exception Handlers** (`app/utils/exceptions.py`):
```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body}
    )

async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Database integrity constraint violated"}
    )
```

**Register in main.py**:
```python
from app.utils.exceptions import validation_exception_handler, integrity_exception_handler

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
```

## Best Practices

### Security
1. **Never commit secrets** - Use environment variables for SECRET_KEY, DATABASE_URL
2. **Use strong secrets** - Generate with `openssl rand -hex 32`
3. **Hash passwords** - Always use bcrypt with appropriate rounds (12+)
4. **Validate tokens** - Check expiration and signature on every request
5. **User isolation** - Always filter by current_user.id for user-specific resources
6. **HTTPS only** - Use secure cookies and HTTPS in production

### Database
1. **Single session per request** - Use dependency injection pattern
2. **Separate models and schemas** - SQLModel for DB, Pydantic for API
3. **Use response_model** - Control what data is exposed in responses
4. **Handle transactions** - Commit after successful operations, rollback on errors
5. **Connection pooling** - Configure pool_size and max_overflow appropriately

### API Design
1. **RESTful conventions** - Use proper HTTP methods and status codes
2. **Consistent responses** - Use Pydantic models for all responses
3. **Pagination** - Add offset/limit for list endpoints
4. **Filtering** - Support query parameters for filtering
5. **Versioning** - Use /api/v1/ prefix for future compatibility

### Performance
1. **Async where beneficial** - Use async for I/O-bound operations
2. **Eager loading** - Use joinedload for relationships to avoid N+1 queries
3. **Caching** - Cache frequently accessed data
4. **Connection pooling** - Reuse database connections

## Common Tasks

### Task 1: Add New Protected Endpoint
1. Create router function with CurrentUserDep
2. Add database query filtered by current_user.id
3. Define request/response Pydantic schemas
4. Handle errors with HTTPException
5. Include router in main.py

### Task 2: Implement New Authentication Method
1. Add new endpoint in auth router
2. Validate credentials/tokens
3. Create JWT token with user identifier
4. Return Token response model

### Task 3: Add Database Model
1. Create SQLModel in app/models/
2. Create Pydantic schemas in app/schemas/
3. Generate Alembic migration
4. Apply migration to database

### Task 4: Add Custom Validation
1. Create Pydantic validator in schema
2. Raise ValueError with descriptive message
3. FastAPI automatically returns 422 with details

## Environment Variables

Required in `.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

## Dependencies

Core dependencies in `requirements.txt`:
```
fastapi==0.100.0
uvicorn[standard]==0.23.0
sqlmodel==0.14.0
pydantic==2.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
psycopg2-binary==2.9.7
alembic==1.11.0
```

## Testing Strategy

- **Unit Tests**: Test individual functions (password hashing, token creation)
- **Integration Tests**: Test API endpoints with test database
- **Authentication Tests**: Test login, registration, protected routes
- **Authorization Tests**: Test user isolation and permissions

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [python-jose Documentation](https://python-jose.readthedocs.io/)
- [passlib Documentation](https://passlib.readthedocs.io/)

---

**Last Updated**: 2026-01-14
**Status**: Active
**Maintainer**: Development Team
