# Research: Todo Full-Stack Web Application

**Date**: 2025-12-26
**Feature**: Todo Full-Stack Web Application
**Branch**: 001-todo-fullstack-app

## Purpose

This document consolidates research findings and technology decisions for the todo application implementation. All decisions resolve uncertainties from the Technical Context and provide rationale for architectural choices.

---

## 1. Monorepo Architecture

### Decision: Single Repository with `/backend` and `/frontend` Directories

**Rationale**:
- Simplified version control: Single commit can update both frontend and backend for a feature
- Easier dependency management: Shared tooling (linting, formatting, CI/CD)
- Atomic changes: API contract changes and frontend updates stay in sync
- Reduced repository overhead compared to multi-repo approach

**Alternatives Considered**:
- **Multi-repo (Polyrepo)**: Separate repositories for backend and frontend
  - ❌ Rejected: Increases coordination overhead for features spanning both layers
  - ❌ Rejected: Requires separate CI/CD pipelines and versioning strategies
  - ❌ Rejected: Makes atomic changes difficult (need two PRs)

- **Monolith (Single app with embedded frontend)**: FastAPI serves Next.js static build
  - ❌ Rejected: Complicates development workflow (requires build step for frontend changes)
  - ❌ Rejected: Reduces deployment flexibility
  - ❌ Rejected: Violates Constitution Principle III (frontend-backend separation)

**Implementation Pattern**:
```
project-root/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── .gitignore        # Shared ignore rules
├── README.md         # Monorepo documentation
└── .env              # Shared environment variables (backend URL for frontend)
```

---

## 2. Better Auth Library Selection

### Decision: Use PyJWT Directly (Not "Better Auth" Library)

**Rationale**:
- **Clarification**: "Better Auth" does not exist as a standalone Python library for FastAPI
- **Actual Choice**: PyJWT (Python JWT library) for token generation and validation
- PyJWT is industry-standard, well-maintained, and widely used with FastAPI
- Provides secure JWT encoding/decoding with algorithm selection (HS256, RS256)
- Simple integration with FastAPI dependencies for authentication

**Alternatives Considered**:
- **FastAPI-Users**: Full-featured authentication system for FastAPI
  - ❌ Rejected: Too heavyweight for simple email/password auth
  - ❌ Rejected: Adds unnecessary complexity (password reset, email verification out of scope)
  - ❌ Rejected: Requires additional database tables and configuration

- **Authlib**: Comprehensive authentication library
  - ❌ Rejected: Overkill for JWT-only authentication
  - ❌ Rejected: Designed for OAuth2/OIDC, not simple JWT

- **Custom JWT Implementation from Scratch**:
  - ❌ Rejected: Security risk (crypto mistakes)
  - ❌ Rejected: Reinventing the wheel

**Implementation Pattern**:
```python
# backend/src/core/security.py
import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload["sub"])
```

---

## 3. SQLModel for Database Operations

### Decision: SQLModel (Pydantic + SQLAlchemy ORM)

**Rationale**:
- **Type Safety**: SQLModel combines Pydantic validation with SQLAlchemy ORM
- **Single Model Definition**: Define database models once, use for validation and DB operations
- **FastAPI Integration**: Native support for Pydantic models in request/response
- **Migrations**: Works with Alembic for database migrations
- **PostgreSQL Support**: Full compatibility with Neon PostgreSQL

**Alternatives Considered**:
- **Pure SQLAlchemy**: Traditional ORM without Pydantic integration
  - ❌ Rejected: Requires separate Pydantic models for API validation (duplication)
  - ❌ Rejected: Loses type safety benefits of Pydantic

- **Raw SQL with psycopg2**: Direct database queries
  - ❌ Rejected: No ORM benefits (relationships, query builder)
  - ❌ Rejected: SQL injection risk without proper parameterization
  - ❌ Rejected: More boilerplate code

- **Tortoise ORM**: Async ORM for Python
  - ❌ Rejected: Less mature than SQLAlchemy
  - ❌ Rejected: Smaller community and ecosystem
  - ❌ Rejected: Migration tooling not as robust as Alembic

**Implementation Pattern**:
```python
# backend/src/models/task.py
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="tasks")
```

---

## 4. JWT Authentication Flow (Next.js ↔ FastAPI)

### Decision: HTTP-Only Cookies + Authorization Header Pattern

**Rationale**:
- **Security**: HTTP-only cookies prevent XSS attacks on token storage
- **Flexibility**: Also support Authorization header for API clients
- **Stateless**: JWT stored client-side, no server-side session
- **Refresh Mechanism**: Use separate refresh token endpoint before expiration

**Alternatives Considered**:
- **LocalStorage Only**: Store JWT in browser localStorage
  - ❌ Rejected: Vulnerable to XSS attacks
  - ❌ Rejected: Not recommended for sensitive tokens

- **Session-Based Auth**: Server-side sessions in Redis
  - ❌ Rejected: Violates Constitution Principle IV (stateless JWT requirement)
  - ❌ Rejected: Adds infrastructure complexity (Redis required)

- **OAuth2 with Third-Party Provider**: Google/GitHub login
  - ❌ Rejected: Out of scope for Phase 2
  - ❌ Rejected: Adds external dependency

**Implementation Flow**:
```
1. User submits login credentials (POST /auth/login)
2. Backend validates credentials, generates JWT
3. Backend returns JWT in response body + sets HTTP-only cookie
4. Frontend stores JWT in memory/context for Authorization header
5. Frontend sends JWT in Authorization: Bearer <token> header for API requests
6. Backend middleware validates JWT on protected routes
7. Backend extracts user_id from JWT claims
8. Services use user_id for data isolation queries
```

**Token Structure**:
```json
{
  "sub": "123",           // User ID (subject)
  "exp": 1735257600,      // Expiration timestamp
  "iat": 1735171200       // Issued at timestamp
}
```

---

## 5. API Request Lifecycle (Frontend → Backend)

### Decision: Axios Client with Interceptors

**Rationale**:
- **Interceptors**: Automatically attach JWT to all requests
- **Error Handling**: Centralized error handling for 401/403 responses
- **Type Safety**: TypeScript interfaces for request/response types
- **Retry Logic**: Can add retry for failed requests

**Alternatives Considered**:
- **Native Fetch API**: Browser-native HTTP client
  - ❌ Rejected: Requires manual error handling on every request
  - ❌ Rejected: No built-in request/response interceptors
  - ❌ Rejected: More boilerplate code

- **Next.js Server Actions**: Server-side API calls
  - ❌ Rejected: Not suitable for client-side state management
  - ❌ Rejected: Requires server components (complicates architecture)

**Implementation Pattern**:
```typescript
// frontend/src/lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor: Attach JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor: Handle 401 (redirect to login)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

**Request Lifecycle Steps**:
```
1. User action triggers API call (e.g., "Create Task" button click)
2. Frontend component calls API function: api.post('/tasks', taskData)
3. Axios request interceptor attaches JWT from localStorage
4. Request sent to FastAPI backend: POST http://localhost:8000/tasks
5. Backend CORS middleware validates origin
6. Backend JWT middleware validates token and extracts user_id
7. Backend route handler calls service layer
8. Service layer filters query by user_id (data isolation)
9. Database operation executed via SQLModel
10. Response returned through layers: DB → Service → Route → FastAPI
11. Frontend Axios response interceptor checks for errors
12. Frontend component updates UI with response data
```

---

## 6. Database Access Pattern (User-Level Isolation)

### Decision: Service Layer Filtering + Database Foreign Keys

**Rationale**:
- **Defense in Depth**: Enforce isolation at multiple layers
- **Service Layer**: Every query filters by `user_id` from JWT claims
- **Database Constraints**: Foreign keys enforce referential integrity
- **Query Pattern**: Always use `WHERE user_id = current_user.id`

**Alternatives Considered**:
- **Row-Level Security (RLS) in PostgreSQL**: Database-level policy enforcement
  - ❌ Rejected: Adds complexity for Neon PostgreSQL setup
  - ❌ Rejected: Requires PostgreSQL roles and session variables
  - ❌ Rejected: Over-engineering for application size

- **Application-Level Only (No DB Constraints)**: Trust service layer
  - ❌ Rejected: Single point of failure (missed filter = data leak)
  - ❌ Rejected: Doesn't enforce integrity at database level

**Implementation Pattern**:
```python
# backend/src/services/task_service.py
from sqlmodel import Session, select
from models.task import Task

class TaskService:
    @staticmethod
    def get_user_tasks(db: Session, user_id: int) -> list[Task]:
        """Get all tasks for a specific user (data isolation)"""
        statement = select(Task).where(Task.user_id == user_id)
        return db.exec(statement).all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task | None:
        """Get task by ID, ensuring user owns it (data isolation)"""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # CRITICAL: Always filter by user_id
        )
        return db.exec(statement).first()

    @staticmethod
    def create_task(db: Session, task_data: dict, user_id: int) -> Task:
        """Create task with automatic user association"""
        task = Task(**task_data, user_id=user_id)  # Auto-assign owner
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
```

**Database Schema Enforcement**:
```sql
-- Foreign key constraint ensures tasks belong to valid users
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    completed BOOLEAN DEFAULT FALSE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast user-specific queries
CREATE INDEX idx_task_user_id ON task(user_id);
```

---

## 7. Environment Variables and Secrets Handling

### Decision: `.env` Files + python-dotenv (Backend) / Next.js env (Frontend)

**Rationale**:
- **Security**: Secrets never committed to git (`.env` in `.gitignore`)
- **Flexibility**: Different configs for dev/staging/production
- **Standard Practice**: Industry-standard approach
- **Easy Rotation**: Change secrets without code changes

**Alternatives Considered**:
- **Hardcoded Secrets**: Embed in source code
  - ❌ Rejected: Security violation (Constitution requirement)
  - ❌ Rejected: Secrets exposed in git history

- **Secret Management Service**: AWS Secrets Manager, HashiCorp Vault
  - ❌ Rejected: Over-engineering for Phase 2
  - ❌ Rejected: Adds infrastructure complexity
  - ✅ Recommendation: Consider for production deployment

**Implementation Pattern**:

**Backend (.env)**:
```bash
# Database
DATABASE_URL=postgresql://user:password@neon-host/dbname

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-min-32-characters-long
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Application
DEBUG=True
```

**Backend (config.py)**:
```python
# backend/src/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_hours: int = 24
    cors_origins: str
    debug: bool = False

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

**Frontend (.env.local)**:
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Note: NEXT_PUBLIC_ prefix exposes to browser (use for non-sensitive config only)
```

**Frontend (usage)**:
```typescript
// frontend/src/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

**Security Checklist**:
- [x] `.env` added to `.gitignore`
- [x] `.env.example` committed with placeholder values
- [x] JWT secret key minimum 32 characters (HS256 requirement)
- [x] Database credentials never in source code
- [x] Environment-specific configurations (dev, staging, prod)
- [x] Secrets rotation documented in quickstart.md

---

## 8. CORS Configuration (Cross-Origin Resource Sharing)

### Decision: FastAPI CORS Middleware with Environment-Based Origins

**Rationale**:
- **Development**: Allow `http://localhost:3000` (Next.js dev server)
- **Production**: Whitelist specific frontend domain only
- **Security**: Prevent unauthorized origins from accessing API
- **Credentials**: Allow credentials for cookie-based auth

**Implementation Pattern**:
```python
# backend/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings

app = FastAPI()
settings = get_settings()

# CORS configuration
origins = settings.cors_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ["http://localhost:3000"] in dev
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],     # Authorization, Content-Type, etc.
)
```

---

## 9. Password Hashing Strategy

### Decision: Passlib with bcrypt Algorithm

**Rationale**:
- **Security**: bcrypt is designed for password hashing (slow, resistant to brute force)
- **Industry Standard**: Widely used and audited
- **Salt Automatic**: bcrypt handles salting internally
- **FastAPI Compatible**: Works seamlessly with FastAPI

**Alternatives Considered**:
- **Argon2**: Modern password hashing algorithm
  - ✅ Acceptable: Slightly more secure than bcrypt
  - ❌ Rejected for simplicity: bcrypt is more widely supported

- **SHA-256**: Cryptographic hash function
  - ❌ Rejected: Too fast (vulnerable to brute force)
  - ❌ Rejected: Not designed for password hashing

**Implementation Pattern**:
```python
# backend/src/core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

---

## 10. Database Migrations Strategy

### Decision: Alembic for Schema Migrations

**Rationale**:
- **SQLAlchemy Integration**: Works natively with SQLModel (built on SQLAlchemy)
- **Version Control**: Migration scripts tracked in git
- **Rollback Support**: Can revert schema changes
- **Team Collaboration**: Shared migration history

**Implementation Pattern**:
```bash
# Initialize Alembic
alembic init alembic

# Generate migration from model changes
alembic revision --autogenerate -m "Create user and task tables"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

**Migration File Example**:
```python
# alembic/versions/001_create_user_task_tables.py
def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(2000)),
        sa.Column('completed', sa.Boolean(), default=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_index('idx_task_user_id', 'task', ['user_id'])

def downgrade():
    op.drop_table('task')
    op.drop_table('user')
```

---

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Architecture** | Monorepo (/backend, /frontend) | Atomic changes, simplified coordination |
| **Auth Library** | PyJWT (not "Better Auth") | Industry standard, simple integration |
| **Database ORM** | SQLModel | Type safety, Pydantic + SQLAlchemy combined |
| **JWT Flow** | HTTP-only cookies + Auth header | Security (XSS protection) + flexibility |
| **API Client** | Axios with interceptors | Centralized auth/error handling |
| **Data Isolation** | Service layer filtering + FK constraints | Defense in depth, Constitution compliance |
| **Secrets** | .env files + dotenv/Next.js env | Security, never commit secrets |
| **CORS** | FastAPI middleware, env-based origins | Security, allow dev + prod origins |
| **Password Hashing** | Passlib with bcrypt | Industry standard, automatic salting |
| **Migrations** | Alembic | Version control, rollback support |

---

## Next Steps

1. **Phase 1: Design** - Generate data-model.md and API contracts
2. **Implementation** - Follow /sp.tasks for task breakdown
3. **Testing** - Verify user-level isolation in integration tests
4. **Deployment** - Configure production environment variables
