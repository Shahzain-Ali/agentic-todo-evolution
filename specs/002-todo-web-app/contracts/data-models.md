# Data Models: Request/Response Schemas

**Feature**: 002-todo-web-app
**Date**: 2026-01-14
**Status**: Completed

## Overview

This document defines the Pydantic schemas used for API request validation and response serialization. These schemas ensure type safety, automatic validation, and clear API contracts.

## Authentication Schemas

### UserCreate (Request)

Used for user registration.

**Schema**:
```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
```

**JSON Example**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Validation Rules**:
- `email`: Must be valid email format (RFC 5322)
- `password`: Minimum 8 characters, maximum 100 characters

---

### UserLogin (Request)

Used for user authentication.

**Schema**:
```python
from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

**JSON Example**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Validation Rules**:
- `email`: Must be valid email format
- `password`: Required (no length validation on login)

---

### UserResponse (Response)

Returned after successful registration.

**Schema**:
```python
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allows creation from SQLModel
```

**JSON Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2026-01-14T12:00:00Z"
}
```

**Notes**:
- Password hash is NEVER included in response
- `from_attributes = True` allows direct conversion from SQLModel User

---

### TokenResponse (Response)

Returned after successful login.

**Schema**:
```python
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

**JSON Example**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Notes**:
- `access_token`: JWT token string
- `token_type`: Always "bearer" for JWT authentication

---

## Task Schemas

### TaskCreate (Request)

Used for creating new tasks.

**Schema**:
```python
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
```

**JSON Example**:
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation"
}
```

**Minimal Example** (description optional):
```json
{
  "title": "Quick task"
}
```

**Validation Rules**:
- `title`: Required, minimum 1 character, maximum 200 characters
- `description`: Optional, maximum 2000 characters

---

### TaskUpdate (Request)

Used for updating existing tasks.

**Schema**:
```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = None
```

**JSON Examples**:

Update title only:
```json
{
  "title": "Updated task title"
}
```

Update status only:
```json
{
  "status": "completed"
}
```

Update all fields:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed"
}
```

**Validation Rules**:
- All fields are optional (partial update)
- `title`: If provided, minimum 1 character, maximum 200 characters
- `description`: If provided, maximum 2000 characters
- `status`: If provided, must be "pending" or "completed"

---

### TaskResponse (Response)

Returned for all task operations (create, read, update).

**Schema**:
```python
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows creation from SQLModel
```

**JSON Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "status": "pending",
  "created_at": "2026-01-14T12:00:00Z",
  "updated_at": "2026-01-14T12:00:00Z"
}
```

**Notes**:
- `from_attributes = True` allows direct conversion from SQLModel Task
- All fields are always present in response
- `description` can be null if not provided

---

### TaskListResponse (Response)

Returned when fetching all tasks (array of TaskResponse).

**Schema**:
```python
from typing import List

TaskListResponse = List[TaskResponse]
```

**JSON Example**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Task 1",
    "description": "Description 1",
    "status": "pending",
    "created_at": "2026-01-14T12:00:00Z",
    "updated_at": "2026-01-14T12:00:00Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Task 2",
    "description": null,
    "status": "completed",
    "created_at": "2026-01-14T10:00:00Z",
    "updated_at": "2026-01-14T11:30:00Z"
  }
]
```

**Empty Response**:
```json
[]
```

---

## Error Schemas

### HTTPError (Response)

Standard error response for 4xx and 5xx errors.

**Schema**:
```python
from pydantic import BaseModel

class HTTPError(BaseModel):
    detail: str
```

**JSON Examples**:

401 Unauthorized:
```json
{
  "detail": "Could not validate credentials"
}
```

403 Forbidden:
```json
{
  "detail": "Not authorized to update this task"
}
```

404 Not Found:
```json
{
  "detail": "Task not found"
}
```

409 Conflict:
```json
{
  "detail": "Email already registered"
}
```

---

### ValidationError (Response)

Returned for 422 Unprocessable Entity (validation errors).

**Schema**:
```python
from pydantic import BaseModel
from typing import List, Any

class ValidationErrorDetail(BaseModel):
    loc: List[str]  # Location of error (e.g., ["body", "email"])
    msg: str        # Error message
    type: str       # Error type

class ValidationError(BaseModel):
    detail: List[ValidationErrorDetail]
```

**JSON Example**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    },
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

## Success Message Schemas

### DeleteResponse (Response)

Returned after successful deletion.

**Schema**:
```python
from pydantic import BaseModel

class DeleteResponse(BaseModel):
    message: str
```

**JSON Example**:
```json
{
  "message": "Task deleted successfully"
}
```

---

### HealthResponse (Response)

Returned by health check endpoint.

**Schema**:
```python
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    database: str
```

**JSON Examples**:

Healthy:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

Unhealthy:
```json
{
  "status": "unhealthy",
  "database": "disconnected"
}
```

---

## Internal Schemas (Not Exposed in API)

### JWT Token Payload

Internal structure of JWT token (not directly exposed).

**Schema**:
```python
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TokenPayload(BaseModel):
    sub: UUID  # Subject (user_id)
    exp: datetime  # Expiration time
    iat: datetime  # Issued at time
```

**Example Payload** (decoded JWT):
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "exp": 1705324800,
  "iat": 1705238400
}
```

---

## Schema Relationships

### Request → Database → Response Flow

**User Registration**:
```
UserCreate (request)
  ↓
User (SQLModel - database)
  ↓
UserResponse (response)
```

**Task Creation**:
```
TaskCreate (request)
  ↓
Task (SQLModel - database)
  ↓
TaskResponse (response)
```

**Task Update**:
```
TaskUpdate (request - partial)
  ↓
Task (SQLModel - database - merged)
  ↓
TaskResponse (response)
```

---

## Validation Examples

### Email Validation

**Valid**:
- `user@example.com`
- `john.doe@company.co.uk`
- `test+tag@domain.com`

**Invalid**:
- `invalid-email` (no @ symbol)
- `@example.com` (no local part)
- `user@` (no domain)

### Password Validation

**Valid**:
- `password123` (8+ characters)
- `MySecureP@ssw0rd!` (complex password)

**Invalid**:
- `pass` (less than 8 characters)
- `` (empty string)

### Title Validation

**Valid**:
- `A` (1 character minimum)
- `Complete project documentation` (normal length)
- `X` * 200 (200 characters maximum)

**Invalid**:
- `` (empty string)
- `X` * 201 (exceeds 200 characters)

### Status Validation

**Valid**:
- `pending`
- `completed`

**Invalid**:
- `in-progress` (not in enum)
- `done` (not in enum)
- `PENDING` (case-sensitive, must be lowercase)

---

## TypeScript Types (Frontend)

For frontend TypeScript integration:

```typescript
// Authentication
export interface UserCreate {
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserResponse {
  id: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// Tasks
export type TaskStatus = 'pending' | 'completed';

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
  status?: TaskStatus;
}

export interface TaskResponse {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

// Errors
export interface HTTPError {
  detail: string;
}

export interface ValidationErrorDetail {
  loc: string[];
  msg: string;
  type: string;
}

export interface ValidationError {
  detail: ValidationErrorDetail[];
}
```

---

## Summary

The data models provide:
- **Type Safety**: Pydantic validation ensures correct data types
- **Automatic Validation**: Invalid data rejected before reaching business logic
- **Clear Contracts**: Well-defined request/response structures
- **Documentation**: Automatic OpenAPI schema generation
- **Frontend Integration**: Easy to generate TypeScript types

**Total Schemas**:
- **4 Request schemas** (UserCreate, UserLogin, TaskCreate, TaskUpdate)
- **5 Response schemas** (UserResponse, TokenResponse, TaskResponse, DeleteResponse, HealthResponse)
- **2 Error schemas** (HTTPError, ValidationError)

**Next Steps**: Create quickstart guide for local development setup.
