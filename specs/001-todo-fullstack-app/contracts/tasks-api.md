# API Contract: Task CRUD Endpoints

**Date**: 2025-12-26
**Feature**: Todo Full-Stack Web Application
**Base URL**: `http://localhost:8000` (development) | `https://api.yourdomain.com` (production)
**API Version**: v1

## Overview

This document specifies the task management API endpoints for creating, reading, updating, and deleting todo tasks. All endpoints require JWT authentication and enforce user-level data isolation.

---

## Endpoints Summary

| Method | Endpoint             | Description                  | Auth Required |
|--------|----------------------|------------------------------|---------------|
| GET    | `/tasks`             | Get all user's tasks         | Yes           |
| GET    | `/tasks/{id}`        | Get specific task by ID      | Yes           |
| POST   | `/tasks`             | Create new task              | Yes           |
| PUT    | `/tasks/{id}`        | Update task (full replace)   | Yes           |
| PATCH  | `/tasks/{id}`        | Partial update task          | Yes           |
| DELETE | `/tasks/{id}`        | Delete task                  | Yes           |
| PATCH  | `/tasks/{id}/toggle` | Toggle completion status     | Yes           |

---

## Authentication

All task endpoints require JWT authentication via Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**User Isolation**: All endpoints automatically filter by authenticated user's ID. Users can only access their own tasks.

---

## 1. GET /tasks

### Description
Retrieve all tasks belonging to the authenticated user.

### Request

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters (Optional):**
| Parameter   | Type    | Description                               | Default |
|-------------|---------|-------------------------------------------|---------|
| `completed` | boolean | Filter by completion status               | None    |
| `limit`     | integer | Max number of tasks to return             | 100     |
| `offset`    | integer | Number of tasks to skip (pagination)      | 0       |

**Example:**
```
GET /tasks?completed=false&limit=20&offset=0
```

### Response

**Success (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "user_id": 1,
      "created_at": "2025-12-26T10:00:00Z",
      "updated_at": "2025-12-26T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Finish project report",
      "description": null,
      "completed": true,
      "user_id": 1,
      "created_at": "2025-12-25T14:30:00Z",
      "updated_at": "2025-12-26T09:15:00Z"
    }
  ],
  "total": 2,
  "limit": 20,
  "offset": 0
}
```

**Error (401 Unauthorized):**
```json
{
  "detail": {
    "error": "unauthorized",
    "message": "Authentication required"
  }
}
```

### Business Logic

1. Validate JWT (extract user_id from claims)
2. Query tasks WHERE user_id = authenticated_user_id
3. Apply optional filters (completed status)
4. Apply pagination (limit/offset)
5. Sort by created_at DESC (newest first)
6. Return task list

### Functional Requirements Covered
- FR-016: Allow users to retrieve all their own tasks
- FR-022: Filter all queries by user ID
- FR-024: Return 401 for unauthenticated requests

---

## 2. GET /tasks/{id}

### Description
Retrieve a specific task by ID (only if user owns it).

### Request

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
| Parameter | Type    | Description      |
|-----------|---------|------------------|
| `id`      | integer | Task ID          |

**Example:**
```
GET /tasks/42
```

### Response

**Success (200 OK):**
```json
{
  "id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": 1,
  "created_at": "2025-12-26T10:00:00Z",
  "updated_at": "2025-12-26T10:00:00Z"
}
```

**Error (404 Not Found) - Task Not Found or Unauthorized:**
```json
{
  "detail": {
    "error": "not_found",
    "message": "Task not found"
  }
}
```

**Note**: Returns 404 (not 403) even if task exists but belongs to another user. This prevents information leakage (Constitution: FR-026).

### Business Logic

1. Validate JWT (extract user_id)
2. Query task WHERE id = {id} AND user_id = authenticated_user_id
3. If not found: Return 404
4. If found: Return task data

### Functional Requirements Covered
- FR-017: Allow users to retrieve specific task by ID (if they own it)
- FR-023: Reject attempts to access tasks owned by other users
- FR-026: Return 404 (not 403) to prevent information leakage

---

## 3. POST /tasks

### Description
Create a new task for the authenticated user.

### Request

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Schema:**
| Field         | Type   | Required | Constraints                    |
|---------------|--------|----------|--------------------------------|
| `title`       | string | Yes      | Min 1 char, max 200 chars      |
| `description` | string | No       | Max 2000 chars                 |

### Response

**Success (201 Created):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": 1,
  "created_at": "2025-12-26T10:00:00Z",
  "updated_at": "2025-12-26T10:00:00Z"
}
```

**Error (400 Bad Request) - Validation Error:**
```json
{
  "detail": {
    "error": "validation_error",
    "message": "Title cannot be empty",
    "field": "title"
  }
}
```

**Error (400 Bad Request) - Title Too Long:**
```json
{
  "detail": {
    "error": "validation_error",
    "message": "Title must be 200 characters or fewer",
    "field": "title"
  }
}
```

### Business Logic

1. Validate JWT (extract user_id)
2. Validate request body (title required, max lengths)
3. Create task with user_id = authenticated_user_id (auto-assign)
4. Set completed = false by default
5. Set created_at and updated_at to current timestamp
6. Save to database
7. Return created task

### Functional Requirements Covered
- FR-011: Allow authenticated users to create tasks
- FR-012: Validate title is not empty
- FR-013: Limit title to 200 characters
- FR-014: Limit description to 2000 characters
- FR-015: Automatically associate tasks with user ID

---

## 4. PUT /tasks/{id}

### Description
Update task (full replacement - all fields required).

### Request

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters:**
| Parameter | Type    | Description      |
|-----------|---------|------------------|
| `id`      | integer | Task ID          |

**Body:**
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "completed": true
}
```

**Schema:**
| Field         | Type    | Required | Constraints           |
|---------------|---------|----------|-----------------------|
| `title`       | string  | Yes      | Min 1, max 200 chars  |
| `description` | string  | No       | Max 2000 chars        |
| `completed`   | boolean | Yes      | true or false         |

### Response

**Success (200 OK):**
```json
{
  "id": 1,
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "completed": true,
  "user_id": 1,
  "created_at": "2025-12-26T10:00:00Z",
  "updated_at": "2025-12-26T11:30:00Z"
}
```

**Error (404 Not Found):**
```json
{
  "detail": {
    "error": "not_found",
    "message": "Task not found"
  }
}
```

**Error (403 Forbidden) - Not Owner:**

*Note: We return 404 instead to prevent information leakage (FR-026)*

### Business Logic

1. Validate JWT (extract user_id)
2. Query task WHERE id = {id} AND user_id = authenticated_user_id
3. If not found: Return 404
4. Validate request body
5. Update all fields
6. Update updated_at timestamp
7. Save to database
8. Return updated task

### Functional Requirements Covered
- FR-018: Allow users to update task (if they own it)
- FR-023: Reject attempts to modify tasks owned by other users
- FR-040: Automatically timestamp updates

---

## 5. PATCH /tasks/{id}

### Description
Partial update task (only specified fields are updated).

### Request

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters:**
| Parameter | Type    | Description      |
|-----------|---------|------------------|
| `id`      | integer | Task ID          |

**Body (all fields optional):**
```json
{
  "title": "Buy groceries and cook dinner"
}
```

**Schema:**
| Field         | Type    | Required | Constraints           |
|---------------|---------|----------|-----------------------|
| `title`       | string  | No       | Min 1, max 200 chars  |
| `description` | string  | No       | Max 2000 chars        |
| `completed`   | boolean | No       | true or false         |

### Response

**Success (200 OK):**
```json
{
  "id": 1,
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": 1,
  "created_at": "2025-12-26T10:00:00Z",
  "updated_at": "2025-12-26T11:45:00Z"
}
```

### Business Logic

1. Validate JWT (extract user_id)
2. Query task WHERE id = {id} AND user_id = authenticated_user_id
3. If not found: Return 404
4. Update only provided fields
5. Update updated_at timestamp
6. Save to database
7. Return updated task

### Functional Requirements Covered
- FR-018: Allow users to update task
- FR-020: Allow users to mark tasks as complete/incomplete
- FR-021: Persist completion status

---

## 6. DELETE /tasks/{id}

### Description
Delete a task (only if user owns it).

### Request

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
| Parameter | Type    | Description      |
|-----------|---------|------------------|
| `id`      | integer | Task ID          |

**Example:**
```
DELETE /tasks/42
```

### Response

**Success (204 No Content):**
```
(empty body)
```

**Error (404 Not Found):**
```json
{
  "detail": {
    "error": "not_found",
    "message": "Task not found"
  }
}
```

### Business Logic

1. Validate JWT (extract user_id)
2. Query task WHERE id = {id} AND user_id = authenticated_user_id
3. If not found: Return 404
4. Delete task from database
5. Return 204 No Content

### Functional Requirements Covered
- FR-019: Allow users to delete tasks (if they own it)
- FR-023: Reject attempts to delete tasks owned by other users

---

## 7. PATCH /tasks/{id}/toggle

### Description
Toggle task completion status (convenience endpoint).

### Request

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
| Parameter | Type    | Description      |
|-----------|---------|------------------|
| `id`      | integer | Task ID          |

**Example:**
```
PATCH /tasks/42/toggle
```

### Response

**Success (200 OK):**
```json
{
  "id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "user_id": 1,
  "created_at": "2025-12-26T10:00:00Z",
  "updated_at": "2025-12-26T12:00:00Z"
}
```

### Business Logic

1. Validate JWT (extract user_id)
2. Query task WHERE id = {id} AND user_id = authenticated_user_id
3. If not found: Return 404
4. Toggle completed: false → true or true → false
5. Update updated_at timestamp
6. Save to database
7. Return updated task

### Functional Requirements Covered
- FR-020: Allow users to mark tasks as complete/incomplete
- FR-021: Persist completion status

---

## Error Response Format

All errors follow a consistent structure:

```json
{
  "detail": {
    "error": "error_code",
    "message": "Human-readable error message",
    "field": "field_name"  // Optional
  }
}
```

### Error Codes

| Code                  | HTTP Status | Description                           |
|-----------------------|-------------|---------------------------------------|
| `validation_error`    | 400         | Invalid input data                    |
| `unauthorized`        | 401         | Missing or invalid JWT token          |
| `forbidden`           | 403         | User lacks permission (rarely used)   |
| `not_found`           | 404         | Task not found or unauthorized access |
| `internal_server_error` | 500       | Unexpected server error               |

---

## Data Isolation Enforcement

**Critical Security Rule**: Every task query MUST include user_id filter.

**Correct Pattern:**
```python
# Get task with authorization check
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == current_user_id  # ALWAYS include this
).first()
```

**❌ WRONG Pattern (Data Leak):**
```python
# Missing user_id filter - allows cross-user access!
task = db.query(Task).filter(Task.id == task_id).first()
```

### Authorization Flow

```
1. User sends request with JWT: GET /tasks/42
2. Backend middleware validates JWT
3. Extract user_id from JWT claims: user_id = 1
4. Query: SELECT * FROM task WHERE id = 42 AND user_id = 1
5. If found: Return task (200)
6. If not found: Return 404 (prevents info leakage)
```

---

## Frontend Integration Example

```typescript
// frontend/src/lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Automatically attach JWT to all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Task API functions
export async function getTasks(completed?: boolean) {
  const response = await api.get('/tasks', {
    params: { completed },
  });
  return response.data;
}

export async function getTask(id: number) {
  const response = await api.get(`/tasks/${id}`);
  return response.data;
}

export async function createTask(title: string, description?: string) {
  const response = await api.post('/tasks', { title, description });
  return response.data;
}

export async function updateTask(id: number, data: {
  title?: string;
  description?: string;
  completed?: boolean;
}) {
  const response = await api.patch(`/tasks/${id}`, data);
  return response.data;
}

export async function deleteTask(id: number) {
  await api.delete(`/tasks/${id}`);
}

export async function toggleTask(id: number) {
  const response = await api.patch(`/tasks/${id}/toggle`);
  return response.data;
}
```

---

## Testing Checklist

### Data Isolation Tests (Critical)
- [ ] User A cannot read User B's tasks
- [ ] User A cannot update User B's tasks
- [ ] User A cannot delete User B's tasks
- [ ] Direct task ID guessing returns 404 (not 403)

### CRUD Operations
- [ ] User can create task with title only
- [ ] User can create task with title and description
- [ ] User can retrieve all their tasks
- [ ] User can retrieve single task by ID
- [ ] User can update task title
- [ ] User can update task description
- [ ] User can mark task as complete
- [ ] User can mark task as incomplete
- [ ] User can toggle task completion
- [ ] User can delete task
- [ ] Deleted task no longer appears in list

### Validation
- [ ] Cannot create task with empty title (400)
- [ ] Cannot create task with title > 200 chars (400)
- [ ] Cannot create task with description > 2000 chars (400)
- [ ] Cannot update task with invalid data (400)

### Authentication
- [ ] All endpoints reject requests without JWT (401)
- [ ] All endpoints reject requests with expired JWT (401)
- [ ] All endpoints accept requests with valid JWT (200/201/204)

---

## OpenAPI Specification (Partial)

```yaml
openapi: 3.0.0
info:
  title: Todo App Task API
  version: 1.0.0
paths:
  /tasks:
    get:
      summary: Get all user's tasks
      security:
        - BearerAuth: []
      parameters:
        - name: completed
          in: query
          schema:
            type: boolean
        - name: limit
          in: query
          schema:
            type: integer
            default: 100
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        200:
          description: List of tasks
          content:
            application/json:
              schema:
                type: object
                properties:
                  tasks:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  total:
                    type: integer
                  limit:
                    type: integer
                  offset:
                    type: integer
        401:
          description: Unauthorized

    post:
      summary: Create new task
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [title]
              properties:
                title:
                  type: string
                  minLength: 1
                  maxLength: 200
                description:
                  type: string
                  maxLength: 2000
      responses:
        201:
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        400:
          description: Validation error
        401:
          description: Unauthorized

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Task:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        description:
          type: string
          nullable: true
        completed:
          type: boolean
        user_id:
          type: integer
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
```
