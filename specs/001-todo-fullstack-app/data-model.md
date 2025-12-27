# Data Model: Todo Full-Stack Web Application

**Date**: 2025-12-26
**Feature**: Todo Full-Stack Web Application
**Branch**: 001-todo-fullstack-app

## Purpose

This document defines the database schema, entity relationships, validation rules, and state transitions for the todo application. All models use SQLModel for type-safe database operations and Pydantic validation.

---

## Entity-Relationship Diagram

```
┌─────────────────────────────────┐
│          User                    │
│─────────────────────────────────│
│ PK  id: int                     │
│ UQ  email: str (max 255)        │
│     password_hash: str (max 255)│
│     created_at: datetime        │
└─────────────────────────────────┘
           │ 1
           │
           │ owns
           │
           │ *
┌─────────────────────────────────┐
│          Task                    │
│─────────────────────────────────│
│ PK  id: int                     │
│     title: str (max 200)        │
│     description: str? (max 2000)│
│     completed: bool             │
│ FK  user_id: int → User.id      │
│     created_at: datetime        │
│     updated_at: datetime        │
└─────────────────────────────────┘

Relationship: One User → Many Tasks (one-to-many)
Cascade: ON DELETE CASCADE (deleting user deletes all their tasks)
```

---

## Entity: User

### Purpose
Represents a registered user account with authentication credentials.

### Fields

| Field          | Type      | Constraints                     | Description                                    |
|----------------|-----------|---------------------------------|------------------------------------------------|
| `id`           | Integer   | Primary Key, Auto-increment     | Unique user identifier                         |
| `email`        | String    | Unique, Not Null, Max 255 chars | User's email address (used for login)          |
| `password_hash`| String    | Not Null, Max 255 chars         | Bcrypt-hashed password (never store plaintext) |
| `created_at`   | DateTime  | Not Null, Default=now()         | Account creation timestamp                     |

### Validation Rules

1. **Email Format**: Must be valid email format (validated by Pydantic `EmailStr`)
2. **Email Uniqueness**: No duplicate emails allowed (enforced at database level)
3. **Password Strength** (pre-hash): Minimum 8 characters (validated before hashing)
4. **Password Storage**: Always store hashed password, never plaintext
5. **Email Case**: Store lowercase for case-insensitive lookup

### Indexes

- **Primary Key**: `id` (automatically indexed)
- **Unique Index**: `email` (for fast login lookups and uniqueness enforcement)

### SQLModel Implementation

```python
# backend/src/models/user.py
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from pydantic import EmailStr

class User(SQLModel, table=True):
    """User account model for authentication and task ownership."""

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(
        unique=True,
        index=True,
        max_length=255,
        sa_column_kwargs={"nullable": False}
    )
    password_hash: str = Field(
        max_length=255,
        sa_column_kwargs={"nullable": False}
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )

    # Relationship: one user has many tasks
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
```

### Pydantic Schemas (API Request/Response)

```python
# backend/src/models/user.py (continued)

class UserCreate(SQLModel):
    """Schema for user registration request."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserLogin(SQLModel):
    """Schema for user login request."""
    email: EmailStr
    password: str

class UserResponse(SQLModel):
    """Schema for user data in API responses (no password)."""
    id: int
    email: str
    created_at: datetime
```

### Business Rules

1. **Registration**: Email must be unique, password must be hashed before storage
2. **Login**: Verify password hash using bcrypt comparison
3. **Data Isolation**: All user-specific queries filter by `user_id`
4. **Cascade Delete**: Deleting a user deletes all their tasks (ON DELETE CASCADE)

---

## Entity: Task

### Purpose
Represents a todo item owned by a specific user.

### Fields

| Field         | Type      | Constraints                        | Description                                  |
|---------------|-----------|------------------------------------|----------------------------------------------|
| `id`          | Integer   | Primary Key, Auto-increment        | Unique task identifier                       |
| `title`       | String    | Not Null, Max 200 chars            | Task title/summary                           |
| `description` | String    | Nullable, Max 2000 chars           | Optional detailed description                |
| `completed`   | Boolean   | Not Null, Default=False            | Task completion status                       |
| `user_id`     | Integer   | Foreign Key → User.id, Not Null    | Owner of the task (for data isolation)       |
| `created_at`  | DateTime  | Not Null, Default=now()            | Task creation timestamp                      |
| `updated_at`  | DateTime  | Not Null, Default=now()            | Last update timestamp (auto-updated)         |

### Validation Rules

1. **Title Required**: Title cannot be empty or whitespace-only
2. **Title Length**: Maximum 200 characters (FR-013)
3. **Description Length**: Maximum 2000 characters (FR-014)
4. **Ownership**: Every task MUST have a valid `user_id` (foreign key constraint)
5. **Completion Status**: Boolean only (true/false)
6. **Timestamps**: Automatically set on creation, `updated_at` refreshed on modification

### Indexes

- **Primary Key**: `id` (automatically indexed)
- **Foreign Key Index**: `user_id` (for fast user-specific queries)
- **Composite Index** (optional): `(user_id, completed)` for filtering by status

### SQLModel Implementation

```python
# backend/src/models/task.py
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    """Task model representing a todo item owned by a user."""

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(
        max_length=200,
        min_length=1,
        sa_column_kwargs={"nullable": False}
    )
    description: str | None = Field(
        default=None,
        max_length=2000
    )
    completed: bool = Field(
        default=False,
        sa_column_kwargs={"nullable": False}
    )
    user_id: int = Field(
        foreign_key="user.id",
        sa_column_kwargs={"nullable": False},
        index=True
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False, "onupdate": datetime.utcnow}
    )

    # Relationship: many tasks belong to one user
    user: User = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed}, user_id={self.user_id})>"
```

### Pydantic Schemas (API Request/Response)

```python
# backend/src/models/task.py (continued)

class TaskCreate(SQLModel):
    """Schema for task creation request."""
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)

class TaskUpdate(SQLModel):
    """Schema for task update request (all fields optional)."""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool | None = None

class TaskResponse(SQLModel):
    """Schema for task data in API responses."""
    id: int
    title: str
    description: str | None
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
```

### Business Rules

1. **Creation**: Automatically assign `user_id` from authenticated user (FR-015)
2. **Data Isolation**: All queries MUST filter by `user_id` (FR-022)
3. **Authorization**: Users can only access/modify their own tasks (FR-023)
4. **Update Timestamp**: `updated_at` automatically updated on any modification
5. **Default Status**: New tasks default to `completed=False`
6. **Validation**: Title cannot be empty/whitespace-only (FR-012)

---

## State Transitions

### Task Completion Status

```
┌─────────────────┐
│   Incomplete    │ (completed = False)
│  (Default)      │
└─────────────────┘
        │
        │ User marks complete
        ▼
┌─────────────────┐
│    Completed    │ (completed = True)
└─────────────────┘
        │
        │ User marks incomplete
        ▼
┌─────────────────┐
│   Incomplete    │ (completed = False)
└─────────────────┘

Transitions:
- False → True: User clicks "Mark Complete"
- True → False: User clicks "Mark Incomplete"
- No other states exist (binary status only)
```

### User Account Status

```
┌─────────────────┐
│  Unregistered   │
└─────────────────┘
        │
        │ Registration (POST /auth/register)
        ▼
┌─────────────────┐
│   Registered    │
│ (Account exists)│
└─────────────────┘
        │
        │ Login (POST /auth/login)
        ▼
┌─────────────────┐
│  Authenticated  │
│ (JWT issued)    │
└─────────────────┘
        │
        │ Logout or token expiry
        ▼
┌─────────────────┐
│ Unauthenticated │
└─────────────────┘

Transitions:
- Unregistered → Registered: Create account
- Registered → Authenticated: Valid login
- Authenticated → Unauthenticated: Logout or token expiration
```

---

## Database Constraints

### Foreign Key Constraints

```sql
-- Task → User relationship
ALTER TABLE task
ADD CONSTRAINT fk_task_user
FOREIGN KEY (user_id) REFERENCES "user"(id)
ON DELETE CASCADE;  -- Deleting user deletes all tasks
```

### Unique Constraints

```sql
-- Unique email for users
ALTER TABLE "user"
ADD CONSTRAINT uq_user_email
UNIQUE (email);
```

### Check Constraints (Optional)

```sql
-- Ensure title is not empty (SQLModel handles this)
ALTER TABLE task
ADD CONSTRAINT chk_task_title_not_empty
CHECK (LENGTH(TRIM(title)) > 0);
```

---

## Query Patterns (User-Level Isolation)

### Get All Tasks for User

```python
# CORRECT: Filters by user_id (Constitution Principle V)
def get_user_tasks(db: Session, user_id: int) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    return db.exec(statement).all()
```

### Get Single Task (Authorization Check)

```python
# CORRECT: Ensures user owns the task
def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task | None:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL: Always include this
    )
    return db.exec(statement).first()
```

### ❌ INCORRECT Pattern (Data Leak)

```python
# WRONG: Missing user_id filter - allows cross-user access
def get_task_by_id_WRONG(db: Session, task_id: int) -> Task | None:
    statement = select(Task).where(Task.id == task_id)
    return db.exec(statement).first()
    # ❌ User could access other users' tasks!
```

---

## Migration Scripts

### Initial Migration

```python
# alembic/versions/001_initial_schema.py
"""Initial schema with user and task tables"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

def upgrade():
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
    )
    op.create_index('ix_user_email', 'user', ['email'], unique=True)

    # Create task table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(2000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
    )
    op.create_index('ix_task_user_id', 'task', ['user_id'])

def downgrade():
    op.drop_table('task')
    op.drop_table('user')
```

---

## Data Validation Summary

| Validation | Layer | Enforcement |
|------------|-------|-------------|
| Email format | Application | Pydantic `EmailStr` |
| Email uniqueness | Database | Unique constraint |
| Password strength | Application | Pydantic `min_length=8` |
| Password hashing | Application | bcrypt via passlib |
| Title not empty | Application | Pydantic `min_length=1` |
| Title max length | Application + DB | Pydantic + VARCHAR(200) |
| Description max length | Application + DB | Pydantic + VARCHAR(2000) |
| User ownership | Application | Service layer filtering |
| Foreign key integrity | Database | FK constraint |
| Timestamps | Database | Default + onupdate |

---

## Performance Considerations

### Indexes for Fast Queries

1. **User lookup by email**: `CREATE INDEX ix_user_email ON user(email)`
2. **Tasks by user**: `CREATE INDEX ix_task_user_id ON task(user_id)`
3. **Optional - Filter by status**: `CREATE INDEX ix_task_user_status ON task(user_id, completed)`

### Query Optimization

- **Always filter by user_id first**: Reduces result set for user-specific queries
- **Use pagination for large task lists**: Add `LIMIT` and `OFFSET` for >100 tasks
- **Eager load relationships** (if needed): Use SQLModel `selectinload` for user + tasks

### Estimated Data Volume

- **Users**: ~1000-10,000 (small to medium scale)
- **Tasks per user**: ~10-100 average, up to 1000 max
- **Total tasks**: ~100,000 (well within PostgreSQL capabilities)

---

## Security Considerations

1. **Password Storage**: Never store plaintext passwords (use bcrypt hash)
2. **User ID Exposure**: Safe to expose in API responses (not sensitive)
3. **Task ID Enumeration**: Use 404 (not 403) to prevent task existence discovery
4. **SQL Injection**: Prevented by SQLModel parameterized queries
5. **Data Isolation**: Enforced at service layer + database constraints

---

## Next Steps

1. Implement SQLModel models in `backend/src/models/`
2. Create Alembic migration scripts
3. Define API contracts in `contracts/` directory
4. Implement service layer with user-level filtering
5. Write integration tests for data isolation
