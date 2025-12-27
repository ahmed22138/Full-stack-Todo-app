# API Contract: Authentication Endpoints

**Date**: 2025-12-26
**Feature**: Todo Full-Stack Web Application
**Base URL**: `http://localhost:8000` (development) | `https://api.yourdomain.com` (production)
**API Version**: v1

## Overview

This document specifies the authentication API endpoints for user registration, login, logout, and token management. All endpoints use JWT (JSON Web Tokens) for stateless authentication.

---

## Endpoints Summary

| Method | Endpoint          | Description                  | Auth Required |
|--------|-------------------|------------------------------|---------------|
| POST   | `/auth/register`  | Create new user account      | No            |
| POST   | `/auth/login`     | Authenticate user, get JWT   | No            |
| POST   | `/auth/logout`    | Invalidate current session   | Yes           |
| POST   | `/auth/refresh`   | Refresh JWT before expiry    | Yes           |
| GET    | `/auth/me`        | Get current user info        | Yes           |

---

## 1. POST /auth/register

### Description
Register a new user account with email and password.

### Request

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Schema:**
| Field      | Type   | Required | Constraints                        |
|------------|--------|----------|------------------------------------|
| `email`    | string | Yes      | Valid email format, max 255 chars  |
| `password` | string | Yes      | Min 8 chars, max 128 chars         |

### Response

**Success (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-12-26T10:30:00Z",
  "message": "User registered successfully"
}
```

**Error (400 Bad Request) - Invalid Input:**
```json
{
  "detail": {
    "error": "validation_error",
    "message": "Email format is invalid",
    "field": "email"
  }
}
```

**Error (409 Conflict) - Email Already Exists:**
```json
{
  "detail": {
    "error": "email_already_exists",
    "message": "An account with this email already exists"
  }
}
```

### Business Logic

1. Validate email format (Pydantic `EmailStr`)
2. Validate password strength (min 8 characters)
3. Check email uniqueness in database
4. Hash password using bcrypt
5. Create user record
6. Return user data (excluding password hash)

### Functional Requirements Covered
- FR-001: Allow user registration
- FR-002: Validate email format
- FR-003: Enforce password strength
- FR-004: Hash passwords before storage
- FR-009: Prevent duplicate email registration

---

## 2. POST /auth/login

### Description
Authenticate user and issue JWT access token.

### Request

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Schema:**
| Field      | Type   | Required | Constraints |
|------------|--------|----------|-------------|
| `email`    | string | Yes      | Valid email |
| `password` | string | Yes      | Any         |

### Response

**Success (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2025-12-26T10:30:00Z"
  }
}
```

**Response Schema:**
| Field           | Type   | Description                                 |
|-----------------|--------|---------------------------------------------|
| `access_token`  | string | JWT token for authentication                |
| `token_type`    | string | Always "bearer"                             |
| `expires_in`    | number | Token expiration time in seconds (86400=24h)|
| `user`          | object | User information                            |

**Error (401 Unauthorized) - Invalid Credentials:**
```json
{
  "detail": {
    "error": "invalid_credentials",
    "message": "Email or password is incorrect"
  }
}
```

**Error (400 Bad Request) - Missing Fields:**
```json
{
  "detail": {
    "error": "validation_error",
    "message": "Email and password are required"
  }
}
```

### JWT Token Structure

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "sub": "1",                    // User ID (subject)
  "exp": 1735257600,             // Expiration timestamp
  "iat": 1735171200              // Issued at timestamp
}
```

**Signature:**
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  JWT_SECRET_KEY
)
```

### Business Logic

1. Lookup user by email
2. Verify password hash using bcrypt
3. Generate JWT with user ID in `sub` claim
4. Set expiration to 24 hours from now
5. Return token and user data

### Functional Requirements Covered
- FR-005: Authenticate via JWT
- FR-006: Include user ID in JWT claims
- FR-008: Provide token expiration

---

## 3. POST /auth/logout

### Description
Logout current user (client-side token invalidation).

### Request

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Body:** (empty or optional)
```json
{}
```

### Response

**Success (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

**Error (401 Unauthorized) - No Token:**
```json
{
  "detail": {
    "error": "unauthorized",
    "message": "Authentication required"
  }
}
```

### Business Logic

1. Validate JWT (middleware)
2. Return success message
3. **Client responsibility**: Delete token from localStorage/cookies
4. **Note**: JWT remains valid until expiration (stateless auth limitation)

**Alternative (Token Blacklist):** For production, consider implementing token blacklist in Redis to invalidate tokens before expiration.

### Functional Requirements Covered
- FR-010: Allow user logout

---

## 4. POST /auth/refresh

### Description
Refresh JWT access token before expiration.

### Request

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Body:** (empty)
```json
{}
```

### Response

**Success (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Error (401 Unauthorized) - Expired Token:**
```json
{
  "detail": {
    "error": "token_expired",
    "message": "Token has expired, please log in again"
  }
}
```

### Business Logic

1. Validate existing JWT
2. Check token is not expired (or within refresh window)
3. Generate new JWT with extended expiration
4. Return new token

### Functional Requirements Covered
- FR-008: Provide token refresh mechanism

---

## 5. GET /auth/me

### Description
Get current authenticated user's information.

### Request

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Response

**Success (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-12-26T10:30:00Z"
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

1. Validate JWT (middleware)
2. Extract user ID from JWT claims
3. Fetch user from database
4. Return user data (excluding password hash)

---

## Error Response Format

All errors follow a consistent structure:

```json
{
  "detail": {
    "error": "error_code",
    "message": "Human-readable error message",
    "field": "field_name"  // Optional: for validation errors
  }
}
```

### Error Codes

| Code                     | HTTP Status | Description                        |
|--------------------------|-------------|------------------------------------|
| `validation_error`       | 400         | Invalid input data                 |
| `email_already_exists`   | 409         | Email is already registered        |
| `invalid_credentials`    | 401         | Login failed (wrong email/password)|
| `unauthorized`           | 401         | No or invalid JWT token            |
| `token_expired`          | 401         | JWT token has expired              |
| `internal_server_error`  | 500         | Unexpected server error            |

### Functional Requirements Covered
- FR-029: Appropriate HTTP status codes
- FR-030: Consistent JSON response format
- FR-031: Standardized error messages

---

## Authentication Flow

```
┌──────────┐
│  Client  │
└────┬─────┘
     │
     │ 1. POST /auth/register
     ▼
┌─────────────────┐
│   Backend API   │  2. Create user, hash password
└────┬────────────┘
     │ 3. Return user data (201)
     ▼
┌──────────┐
│  Client  │  4. Store user email (optional)
└────┬─────┘
     │
     │ 5. POST /auth/login {email, password}
     ▼
┌─────────────────┐
│   Backend API   │  6. Validate credentials, generate JWT
└────┬────────────┘
     │ 7. Return JWT + user data (200)
     ▼
┌──────────┐
│  Client  │  8. Store JWT in localStorage/memory
└────┬─────┘
     │
     │ 9. GET /tasks (with Authorization header)
     ▼
┌─────────────────┐
│   Backend API   │  10. Validate JWT, extract user_id
└────┬────────────┘
     │ 11. Return user's tasks (200)
     ▼
┌──────────┐
│  Client  │  12. Display tasks
└────┬─────┘
     │
     │ 13. POST /auth/logout
     ▼
┌─────────────────┐
│   Backend API   │  14. Return success
└────┬────────────┘
     │ 15. Success (200)
     ▼
┌──────────┐
│  Client  │  16. Delete JWT from storage
└──────────┘
```

---

## Security Considerations

1. **Password Storage**: Always hash with bcrypt before storage (never plaintext)
2. **JWT Secret**: Use strong secret key (min 32 characters), store in `.env`
3. **HTTPS**: Always use HTTPS in production to prevent token interception
4. **Token Expiration**: Set reasonable expiration (24 hours default)
5. **Error Messages**: Don't reveal whether email exists on login failure
6. **Rate Limiting**: Add rate limiting to prevent brute-force attacks (future enhancement)
7. **CORS**: Whitelist only trusted frontend origins

### Functional Requirements Covered
- FR-024: Return 401 for unauthenticated requests
- FR-027: Validate and sanitize inputs

---

## Frontend Integration Example

```typescript
// frontend/src/lib/api.ts
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Register
export async function register(email: string, password: string) {
  const response = await axios.post(`${API_URL}/auth/register`, {
    email,
    password,
  });
  return response.data;
}

// Login
export async function login(email: string, password: string) {
  const response = await axios.post(`${API_URL}/auth/login`, {
    email,
    password,
  });
  // Store token
  localStorage.setItem('access_token', response.data.access_token);
  return response.data;
}

// Logout
export async function logout() {
  const token = localStorage.getItem('access_token');
  await axios.post(
    `${API_URL}/auth/logout`,
    {},
    { headers: { Authorization: `Bearer ${token}` } }
  );
  localStorage.removeItem('access_token');
}

// Get current user
export async function getCurrentUser() {
  const token = localStorage.getItem('access_token');
  const response = await axios.get(`${API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}
```

---

## Testing Checklist

- [ ] User can register with valid email and password
- [ ] Registration fails with duplicate email (409)
- [ ] Registration fails with invalid email format (400)
- [ ] Registration fails with password < 8 characters (400)
- [ ] User can login with correct credentials
- [ ] Login fails with incorrect password (401)
- [ ] Login fails with non-existent email (401)
- [ ] JWT token is returned on successful login
- [ ] JWT token contains user ID in `sub` claim
- [ ] Protected endpoints reject requests without token (401)
- [ ] Protected endpoints accept requests with valid token (200)
- [ ] Token refresh generates new token
- [ ] Logout succeeds with valid token
- [ ] /auth/me returns current user data

---

## OpenAPI Specification (Partial)

```yaml
openapi: 3.0.0
info:
  title: Todo App Authentication API
  version: 1.0.0
paths:
  /auth/register:
    post:
      summary: Register new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
      responses:
        201:
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        400:
          description: Validation error
        409:
          description: Email already exists

  /auth/login:
    post:
      summary: Authenticate user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        200:
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
                  expires_in:
                    type: integer
                  user:
                    $ref: '#/components/schemas/User'
        401:
          description: Invalid credentials

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
```
