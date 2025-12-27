---
id: 002
title: Create System Plan
stage: plan
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-fullstack-app
branch: 001-todo-fullstack-app
user: Ahmed-malik
command: /sp.plan
labels: ["plan", "architecture", "monorepo", "jwt-auth", "sqlmodel", "fastapi", "nextjs"]
links:
  spec: specs/001-todo-fullstack-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-todo-fullstack-app/plan.md
 - specs/001-todo-fullstack-app/research.md
 - specs/001-todo-fullstack-app/data-model.md
 - specs/001-todo-fullstack-app/contracts/auth-api.md
 - specs/001-todo-fullstack-app/contracts/tasks-api.md
 - specs/001-todo-fullstack-app/contracts/database-schema.md
 - specs/001-todo-fullstack-app/quickstart.md
tests:
 - none
---

## Prompt

```text
Create a system plan for Phase II.

Include:
- Monorepo architecture
- Frontend/Backend responsibilities
- JWT auth flow between Next.js and FastAPI
- API request lifecycle
- Database access pattern using SQLModel
- Environment variables and secrets handling
```

## Response snapshot

Created comprehensive implementation plan with research, data model, API contracts, and quickstart guide.

**Plan Structure (plan.md):**

**Technical Context:**
- Python 3.11+ backend (FastAPI, SQLModel, PyJWT, Alembic)
- Next.js 14+ frontend (TypeScript, Axios, TailwindCSS)
- Neon PostgreSQL (cloud-hosted, serverless)
- Monorepo architecture (/backend, /frontend)

**Constitution Check: ✅ ALL 7 PRINCIPLES PASSED**
1. Spec-Driven Development ✅
2. Read Specs Before Implementation ✅
3. Frontend-Backend Separation ✅
4. JWT-Based Authentication ✅
5. User-Level Data Isolation ✅
6. Clean Architecture ✅
7. RESTful API Principles ✅

**Research Decisions (research.md):**
1. Monorepo with /backend and /frontend directories (vs multi-repo)
2. PyJWT library (clarified "Better Auth" doesn't exist for FastAPI)
3. SQLModel for type-safe ORM (Pydantic + SQLAlchemy)
4. HTTP-only cookies + Authorization header for JWT
5. Axios client with interceptors for API requests
6. Service layer filtering + database FK constraints for data isolation
7. .env files + python-dotenv/Next.js env for secrets
8. FastAPI CORS middleware with env-based origins
9. Passlib with bcrypt for password hashing
10. Alembic for database migrations

**Data Model (data-model.md):**
- **User table**: id, email (unique), password_hash, created_at
- **Task table**: id, title, description, completed, user_id (FK), created_at, updated_at
- Relationship: One User → Many Tasks (CASCADE DELETE)
- Indexes: user.email (unique), task.user_id, task(user_id, completed)
- Critical pattern: ALL queries MUST filter by user_id for data isolation

**API Contracts:**

**Auth API (auth-api.md):**
- POST /auth/register - Create account (email + password)
- POST /auth/login - Authenticate, get JWT (24hr expiration)
- POST /auth/logout - Client-side token invalidation
- POST /auth/refresh - Refresh JWT before expiry
- GET /auth/me - Get current user info

**Tasks API (tasks-api.md):**
- GET /tasks - List all user's tasks (with pagination, filtering)
- GET /tasks/{id} - Get specific task (404 if unauthorized for info leakage prevention)
- POST /tasks - Create task (auto-assign user_id)
- PUT /tasks/{id} - Full update
- PATCH /tasks/{id} - Partial update
- DELETE /tasks/{id} - Delete task
- PATCH /tasks/{id}/toggle - Toggle completion status

**Database Schema (database-schema.md):**
- PostgreSQL DDL with migrations
- Foreign key constraints (ON DELETE CASCADE)
- Indexes for performance
- Alembic migration scripts
- Connection string format for Neon

**Quickstart Guide (quickstart.md):**
- Prerequisites (Python 3.11+, Node 18+, Neon account)
- Backend setup (venv, pip install, .env config, alembic migrations, uvicorn)
- Frontend setup (npm install, .env.local config, npm run dev)
- Verification steps (register, login, CRUD tasks, test data isolation)
- Common issues & solutions
- Deployment checklist

**Architecture Highlights:**
- **Monorepo**: Single repository, atomic changes, simplified coordination
- **JWT Flow**: Login → JWT generated → Stored in localStorage → Sent in Authorization header → Validated by middleware → User ID extracted → Queries filtered by user_id
- **Request Lifecycle**: Frontend (Axios) → CORS middleware → JWT middleware → Route handler → Service layer (user_id filtering) → SQLModel → Database
- **Clean Layers**: Routes → Services → Models (no business logic in routes)
- **Data Isolation**: Enforced at service layer (WHERE user_id = ...) + database constraints (FK)

## Outcome

- ✅ Impact: Complete implementation plan with architecture decisions, data model, API contracts, and quickstart guide ready for /sp.tasks
- 🧪 Tests: No tests at planning stage (test strategy defined in contracts)
- 📁 Files: Created plan.md, research.md, data-model.md, 3 API contract files, database-schema.md, quickstart.md
- 🔁 Next prompts: /sp.tasks to generate actionable task breakdown organized by user story
- 🧠 Reflection: Plan successfully addresses all user requirements (monorepo, JWT flow, SQLModel patterns, secrets handling). Constitution compliance verified at all layers. Critical clarification: "Better Auth" library doesn't exist for Python/FastAPI - using PyJWT directly per industry standard. Data isolation pattern emphasized throughout with service layer filtering and database constraints for defense in depth.

## Evaluation notes (flywheel)

- Failure modes observed: None (plan created successfully with all required artifacts)
- Graders run and results (PASS/FAIL): Constitution Check - ALL 7 PRINCIPLES PASSED
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): During /sp.tasks, validate that task organization enables independent testing of user stories per Constitution Principle and spec prioritization (P1 auth → P2 MVP → P3 full CRUD → P4 enhancements)
