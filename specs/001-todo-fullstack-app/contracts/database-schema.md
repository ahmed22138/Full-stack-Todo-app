# Database Schema: Todo Full-Stack Web Application

**Date**: 2025-12-26
**Database**: Neon PostgreSQL (Serverless PostgreSQL)
**ORM**: SQLModel (Pydantic + SQLAlchemy)
**Migration Tool**: Alembic

## Schema Overview

The database consists of 2 tables with a one-to-many relationship:
- `user`: Stores user accounts
- `task`: Stores todo tasks owned by users

---

## Table: user

### Purpose
Stores registered user accounts with authentication credentials.

### SQL DDL

```sql
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE UNIQUE INDEX ix_user_email ON "user"(email);
```

### Columns

| Column          | Type          | Constraints                     | Description                  |
|-----------------|---------------|---------------------------------|------------------------------|
| id              | SERIAL        | PRIMARY KEY                     | Auto-incrementing user ID    |
| email           | VARCHAR(255)  | UNIQUE, NOT NULL                | User's email (login)         |
| password_hash   | VARCHAR(255)  | NOT NULL                        | Bcrypt hashed password       |
| created_at      | TIMESTAMP     | NOT NULL, DEFAULT NOW()         | Account creation time        |

---

## Table: task

### Purpose
Stores todo tasks owned by specific users.

### SQL DDL

```sql
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX ix_task_user_id ON task(user_id);
CREATE INDEX ix_task_user_completed ON task(user_id, completed);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_task_updated_at
BEFORE UPDATE ON task
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

### Columns

| Column       | Type          | Constraints                         | Description                  |
|--------------|---------------|-------------------------------------|------------------------------|
| id           | SERIAL        | PRIMARY KEY                         | Auto-incrementing task ID    |
| title        | VARCHAR(200)  | NOT NULL                            | Task title                   |
| description  | VARCHAR(2000) | NULL                                | Optional description         |
| completed    | BOOLEAN       | NOT NULL, DEFAULT FALSE             | Completion status            |
| user_id      | INTEGER       | NOT NULL, FK → user(id) ON DELETE CASCADE | Owner reference      |
| created_at   | TIMESTAMP     | NOT NULL, DEFAULT NOW()             | Task creation time           |
| updated_at   | TIMESTAMP     | NOT NULL, DEFAULT NOW()             | Last update time             |

---

## Relationships

### user → task (One-to-Many)

```sql
ALTER TABLE task
ADD CONSTRAINT fk_task_user
FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE;
```

**Cascade Behavior**: Deleting a user automatically deletes all their tasks.

**SQLModel Representation**:
```python
# models/user.py
class User(SQLModel, table=True):
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)

# models/task.py
class Task(SQLModel, table=True):
    user: User = Relationship(back_populates="tasks")
```

---

## Indexes

### Performance Optimization

| Index Name              | Table  | Columns            | Purpose                              |
|-------------------------|--------|--------------------|--------------------------------------|
| ix_user_email           | user   | email              | Fast login lookup (unique)           |
| ix_task_user_id         | task   | user_id            | Fast user-specific queries           |
| ix_task_user_completed  | task   | user_id, completed | Filter by status for specific user   |

**Query Examples**:
```sql
-- Fast with ix_task_user_id
SELECT * FROM task WHERE user_id = 1;

-- Fast with ix_task_user_completed
SELECT * FROM task WHERE user_id = 1 AND completed = FALSE;
```

---

## Sample Data

```sql
-- Users
INSERT INTO "user" (email, password_hash, created_at) VALUES
('alice@example.com', '$2b$12$hashedpassword1...', '2025-12-26 10:00:00'),
('bob@example.com', '$2b$12$hashedpassword2...', '2025-12-26 11:00:00');

-- Tasks for Alice (user_id = 1)
INSERT INTO task (title, description, completed, user_id, created_at, updated_at) VALUES
('Buy groceries', 'Milk, eggs, bread', FALSE, 1, '2025-12-26 10:30:00', '2025-12-26 10:30:00'),
('Finish report', NULL, TRUE, 1, '2025-12-25 14:00:00', '2025-12-26 09:00:00');

-- Tasks for Bob (user_id = 2)
INSERT INTO task (title, description, completed, user_id, created_at, updated_at) VALUES
('Fix bug', 'Auth service timeout', FALSE, 2, '2025-12-26 12:00:00', '2025-12-26 12:00:00');
```

---

## Connection String Format (Neon PostgreSQL)

```
postgresql://[user]:[password]@[neon-host]/[database]?sslmode=require
```

**Example**:
```
postgresql://user123:pass456@ep-cool-grass-123456.us-east-2.aws.neon.tech/todo_db?sslmode=require
```

**Environment Variable (.env)**:
```bash
DATABASE_URL=postgresql://user:pass@neon-host/dbname?sslmode=require
```

---

## Migration Management (Alembic)

### Initial Migration

```python
# alembic/versions/001_initial_schema.py
"""Initial schema with user and task tables"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_user_email', 'user', ['email'], unique=True)

    # Create task table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(2000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_user_completed', 'task', ['user_id', 'completed'])

def downgrade():
    op.drop_table('task')
    op.drop_table('user')
```

### Migration Commands

```bash
# Generate migration from SQLModel changes
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Check current version
alembic current
```

---

## Security Considerations

1. **Password Storage**: Always hash with bcrypt before INSERT
2. **SQL Injection**: Use parameterized queries (SQLModel handles this)
3. **Data Isolation**: Always filter by user_id in WHERE clause
4. **Connection Security**: Use SSL/TLS (sslmode=require for Neon)
5. **Secrets**: Store DATABASE_URL in .env, never commit to git

---

## Backup & Recovery

### Neon PostgreSQL Backups

Neon provides automatic backups:
- Point-in-time recovery (PITR)
- 7-day retention by default
- No manual backup scripts needed

### Manual Backup (pg_dump)

```bash
# Export database
pg_dump -h neon-host -U user -d dbname > backup.sql

# Restore database
psql -h neon-host -U user -d dbname < backup.sql
```

---

## Query Examples

### User Operations

```sql
-- Register new user
INSERT INTO "user" (email, password_hash)
VALUES ('user@example.com', '$2b$12$hashed...');

-- Login (fetch user by email)
SELECT id, email, password_hash, created_at
FROM "user"
WHERE email = 'user@example.com';

-- Check email uniqueness
SELECT COUNT(*) FROM "user" WHERE email = 'user@example.com';
```

### Task Operations (with User Isolation)

```sql
-- Get all tasks for user
SELECT * FROM task
WHERE user_id = 1
ORDER BY created_at DESC;

-- Get incomplete tasks for user
SELECT * FROM task
WHERE user_id = 1 AND completed = FALSE
ORDER BY created_at DESC;

-- Get single task (with authorization check)
SELECT * FROM task
WHERE id = 42 AND user_id = 1;

-- Create task
INSERT INTO task (title, description, user_id)
VALUES ('Buy milk', 'Whole milk', 1);

-- Update task
UPDATE task
SET title = 'Buy milk and eggs', updated_at = CURRENT_TIMESTAMP
WHERE id = 42 AND user_id = 1;

-- Toggle completion
UPDATE task
SET completed = NOT completed, updated_at = CURRENT_TIMESTAMP
WHERE id = 42 AND user_id = 1;

-- Delete task
DELETE FROM task
WHERE id = 42 AND user_id = 1;
```

---

## Data Integrity Rules

1. **Email Uniqueness**: Enforced by UNIQUE constraint
2. **User Ownership**: Every task MUST have valid user_id (FK constraint)
3. **Cascade Delete**: Deleting user deletes all tasks (ON DELETE CASCADE)
4. **Timestamps**: Auto-set on insert, auto-update on modify
5. **Completion Status**: Boolean only (no NULL)
6. **Title Required**: NOT NULL constraint

---

## Database Size Estimates

| Users | Tasks/User | Total Tasks | Est. Size |
|-------|------------|-------------|-----------|
| 100   | 50         | 5,000       | ~1 MB     |
| 1,000 | 100        | 100,000     | ~20 MB    |
| 10,000| 100        | 1,000,000   | ~200 MB   |

**Note**: Neon PostgreSQL free tier supports up to 3GB storage.
