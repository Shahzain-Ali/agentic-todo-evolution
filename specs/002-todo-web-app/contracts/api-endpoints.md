# API Endpoints: Full-Stack Todo Application

**Feature**: 002-todo-web-app
**Date**: 2026-01-14
**Status**: Completed
**Base URL**: `https://api.example.com` (replace with actual backend URL)

## Overview

This document defines all REST API endpoints for the todo application. The API follows RESTful conventions and uses JSON for request/response bodies.

## Authentication

All endpoints except authentication endpoints require a valid JWT token in the Authorization header.

**Header Format**:
```
Authorization: Bearer <jwt_token>
```

**Token Expiration**: 24 hours

**Error Response** (401 Unauthorized):
```json
{
  "detail": "Could not validate credentials"
}
```

## Endpoints

### Authentication Endpoints

#### POST /api/auth/register

Register a new user account.

**Request**:
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Body Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| email | string | Yes | Valid email format | User's email address |
| password | string | Yes | Min 8 characters | User's password (will be hashed) |

**Success Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2026-01-14T12:00:00Z"
}
```

**Error Responses**:

409 Conflict - Email already registered:
```json
{
  "detail": "Email already registered"
}
```

422 Unprocessable Entity - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**Example**:
```bash
curl -X POST https://api.example.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass123"}'
```

---

#### POST /api/auth/login

Authenticate user and receive JWT token.

**Request**:
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Body Schema**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email address |
| password | string | Yes | User's password |

**Success Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjE3MDUzMjQ4MDB9.signature",
  "token_type": "bearer"
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| access_token | string | JWT token for authentication |
| token_type | string | Always "bearer" |

**Error Responses**:

401 Unauthorized - Invalid credentials:
```json
{
  "detail": "Incorrect email or password"
}
```

422 Unprocessable Entity - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Example**:
```bash
curl -X POST https://api.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass123"}'
```

---

### Task Endpoints

All task endpoints require authentication via JWT token.

#### GET /api/tasks

Retrieve all tasks for the authenticated user.

**Request**:
```http
GET /api/tasks
Authorization: Bearer <jwt_token>
```

**Query Parameters**: None

**Success Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "pending",
    "created_at": "2026-01-14T12:00:00Z",
    "updated_at": "2026-01-14T12:00:00Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Review pull requests",
    "description": null,
    "status": "completed",
    "created_at": "2026-01-14T10:00:00Z",
    "updated_at": "2026-01-14T11:30:00Z"
  }
]
```

**Response Schema** (Array of Task objects):
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique task identifier |
| user_id | string (UUID) | Owner's user ID |
| title | string | Task title (max 200 chars) |
| description | string \| null | Optional description (max 2000 chars) |
| status | string | "pending" or "completed" |
| created_at | string (ISO 8601) | Creation timestamp |
| updated_at | string (ISO 8601) | Last update timestamp |

**Empty Response** (200 OK):
```json
[]
```

**Error Responses**:

401 Unauthorized - Missing or invalid token:
```json
{
  "detail": "Could not validate credentials"
}
```

**Example**:
```bash
curl -X GET https://api.example.com/api/tasks \
  -H "Authorization: Bearer <jwt_token>"
```

---

#### POST /api/tasks

Create a new task for the authenticated user.

**Request**:
```http
POST /api/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Request Body Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| title | string | Yes | Min 1, max 200 chars | Task title |
| description | string | No | Max 2000 chars | Task description |

**Success Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "New task title",
  "description": "Optional task description",
  "status": "pending",
  "created_at": "2026-01-14T13:00:00Z",
  "updated_at": "2026-01-14T13:00:00Z"
}
```

**Error Responses**:

401 Unauthorized - Missing or invalid token:
```json
{
  "detail": "Could not validate credentials"
}
```

422 Unprocessable Entity - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**Example**:
```bash
curl -X POST https://api.example.com/api/tasks \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"New task","description":"Task details"}'
```

---

#### PUT /api/tasks/{id}

Update an existing task. Only the task owner can update.

**Request**:
```http
PUT /api/tasks/550e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated description",
  "status": "completed"
}
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| id | string (UUID) | Task ID to update |

**Request Body Schema** (all fields optional):
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| title | string | No | Min 1, max 200 chars | Updated task title |
| description | string \| null | No | Max 2000 chars | Updated description |
| status | string | No | "pending" or "completed" | Updated status |

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated task title",
  "description": "Updated description",
  "status": "completed",
  "created_at": "2026-01-14T12:00:00Z",
  "updated_at": "2026-01-14T14:00:00Z"
}
```

**Error Responses**:

401 Unauthorized - Missing or invalid token:
```json
{
  "detail": "Could not validate credentials"
}
```

403 Forbidden - User doesn't own this task:
```json
{
  "detail": "Not authorized to update this task"
}
```

404 Not Found - Task doesn't exist:
```json
{
  "detail": "Task not found"
}
```

422 Unprocessable Entity - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "status"],
      "msg": "value is not a valid enumeration member; permitted: 'pending', 'completed'",
      "type": "type_error.enum"
    }
  ]
}
```

**Example**:
```bash
curl -X PUT https://api.example.com/api/tasks/550e8400-e29b-41d4-a716-446655440001 \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'
```

---

#### DELETE /api/tasks/{id}

Delete a task. Only the task owner can delete.

**Request**:
```http
DELETE /api/tasks/550e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <jwt_token>
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| id | string (UUID) | Task ID to delete |

**Success Response** (200 OK):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:

401 Unauthorized - Missing or invalid token:
```json
{
  "detail": "Could not validate credentials"
}
```

403 Forbidden - User doesn't own this task:
```json
{
  "detail": "Not authorized to delete this task"
}
```

404 Not Found - Task doesn't exist:
```json
{
  "detail": "Task not found"
}
```

**Example**:
```bash
curl -X DELETE https://api.example.com/api/tasks/550e8400-e29b-41d4-a716-446655440001 \
  -H "Authorization: Bearer <jwt_token>"
```

---

## Health Check Endpoint

#### GET /health

Check if the API is running and database is connected.

**Request**:
```http
GET /health
```

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Error Response** (503 Service Unavailable):
```json
{
  "status": "unhealthy",
  "database": "disconnected"
}
```

**Example**:
```bash
curl -X GET https://api.example.com/health
```

---

## Error Response Format

All error responses follow a consistent format:

**Standard Error** (4xx, 5xx):
```json
{
  "detail": "Error message describing what went wrong"
}
```

**Validation Error** (422):
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST (resource created) |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists (duplicate email) |
| 422 | Unprocessable Entity | Validation error in request body |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Service temporarily unavailable |

## Rate Limiting

**Current**: No rate limiting implemented

**Future**: Consider implementing rate limiting for production:
- 100 requests per minute per IP
- 1000 requests per hour per user

## CORS Configuration

**Allowed Origins**: Frontend domain (Vercel deployment URL)
**Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
**Allowed Headers**: Content-Type, Authorization
**Allow Credentials**: Yes (for cookies)

## OpenAPI/Swagger Documentation

Interactive API documentation available at:
- **Swagger UI**: `https://api.example.com/docs`
- **ReDoc**: `https://api.example.com/redoc`
- **OpenAPI JSON**: `https://api.example.com/openapi.json`

## Testing

### Postman Collection

Import the API into Postman:
1. Create new collection "Todo API"
2. Add environment variables:
   - `base_url`: https://api.example.com
   - `jwt_token`: (set after login)
3. Add requests for each endpoint
4. Use `{{base_url}}` and `{{jwt_token}}` variables

### cURL Examples

**Complete Flow**:
```bash
# 1. Register
curl -X POST https://api.example.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# 2. Login (save token)
TOKEN=$(curl -X POST https://api.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}' \
  | jq -r '.access_token')

# 3. Create task
curl -X POST https://api.example.com/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My first task","description":"Task details"}'

# 4. Get all tasks
curl -X GET https://api.example.com/api/tasks \
  -H "Authorization: Bearer $TOKEN"

# 5. Update task (replace TASK_ID)
curl -X PUT https://api.example.com/api/tasks/TASK_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# 6. Delete task (replace TASK_ID)
curl -X DELETE https://api.example.com/api/tasks/TASK_ID \
  -H "Authorization: Bearer $TOKEN"
```

## Summary

The API provides:
- **2 authentication endpoints** (register, login)
- **4 task endpoints** (list, create, update, delete)
- **1 health check endpoint**
- **RESTful design** with standard HTTP methods
- **JWT authentication** for security
- **Comprehensive error handling** with clear messages
- **Automatic documentation** via OpenAPI/Swagger

**Next Steps**: Create data models documentation for request/response schemas.
