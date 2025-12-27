# Implementation Plan: Todo Full-Stack Web Application

**Branch**: `001-todo-fullstack-app` | **Date**: 2025-12-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-fullstack-app/spec.md`

## Summary

Build a multi-user todo web application with JWT-based authentication and full CRUD operations on tasks. The system uses a monorepo architecture with FastAPI backend and Next.js frontend, communicating via RESTful APIs. User data is strictly isolated at the database level, with all task queries filtered by authenticated user ID. The application persists data in Neon PostgreSQL using SQLModel ORM for type-safe database operations.

**Technical Approach**: Monorepo structure with separate `/backend` and `/frontend` directories. Backend implements clean architecture (routes → services → models) with Better Auth for JWT management. Frontend uses Next.js with client-side state management and API integration. SQLModel provides Pydantic-based models with SQLAlchemy ORM capabilities for database operations.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript (frontend with Next.js 14+)
**Primary Dependencies**:
- Backend: FastAPI 0.109+, Better Auth (PyJWT), SQLModel 0.0.14+, Alembic (migrations), python-dotenv
- Frontend: Next.js 14+, React 18+, Axios/Fetch API, TailwindCSS (styling)

**Storage**: Neon PostgreSQL (cloud-hosted, serverless PostgreSQL)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (modern browsers: Chrome, Firefox, Safari, Edge latest versions)
**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**:
- API response time: <1s for task operations under normal load
- Registration/login flow: <2 minutes total user time
- Task creation: <5 seconds from submit to display
- Concurrent users: Support 100+ without degradation

**Constraints**:
- User-level data isolation: MUST filter all queries by user ID (NON-NEGOTIABLE)
- JWT validation required on every protected endpoint
- No server-side session storage (stateless authentication)
- Password hashing before storage (never plaintext)
- CORS configuration required for frontend-backend communication

**Scale/Scope**:
- MVP for ~100 concurrent users
- Database: 2 tables (users, tasks) with foreign key relationships
- API: ~10 endpoints (3 auth, 7 task operations)
- Frontend: 5-6 main pages/components (login, register, dashboard, task list, task form)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development (NON-NEGOTIABLE)
- [x] Specification created via `/sp.specify` ✅
- [x] Planning follows spec via `/sp.plan` ✅
- [x] Tasks will be generated via `/sp.tasks` (not yet executed)
- [x] Implementation will follow via `/sp.implement` (not yet executed)
- [x] No manual coding outside Claude Code workflow ✅

**Status**: PASS - Following spec-driven workflow correctly

### ✅ II. Read Specs Before Implementation (NON-NEGOTIABLE)
- [x] spec.md read and analyzed ✅
- [x] All functional requirements (FR-001 to FR-040) understood ✅
- [x] User stories (P1-P4) and acceptance criteria reviewed ✅
- [x] Success criteria and constraints documented ✅

**Status**: PASS - Plan based on complete spec analysis

### ✅ III. Frontend-Backend Separation
- [x] Backend handles business logic, validation, persistence (services layer) ✅
- [x] Frontend handles presentation and user interaction only ✅
- [x] No business rules duplicated in frontend ✅
- [x] Communication via REST API exclusively ✅
- [x] Backend functional independently (API-first design) ✅

**Status**: PASS - Monorepo with clear /backend and /frontend separation

### ✅ IV. JWT-Based Authentication
- [x] Stateless authentication via JWT ✅
- [x] Tokens contain user ID in claims ✅
- [x] Backend validates JWT on protected endpoints (middleware) ✅
- [x] No server-side session storage ✅
- [x] Token refresh mechanism planned ✅

**Status**: PASS - Better Auth + PyJWT for JWT management

### ✅ V. User-Level Data Isolation (NON-NEGOTIABLE)
- [x] All task queries filter by user_id (enforced in services layer) ✅
- [x] Authorization checks on ALL operations (CRUD) ✅
- [x] 404 response for unauthorized access (prevent info leakage) ✅
- [x] Foreign key constraints in database schema ✅
- [x] Test coverage for cross-user access prevention (planned) ✅

**Status**: PASS - User ID filtering enforced at service and database layers

### ✅ VI. Clean Architecture
- [x] Layered structure: API routes → Services → Models ✅
- [x] Business logic in services layer (not in routes) ✅
- [x] Models represent data structures only (SQLModel) ✅
- [x] Dependency flow: routes → services → models ✅
- [x] No circular dependencies ✅

**Status**: PASS - Clean architecture with clear layer responsibilities

### ✅ VII. RESTful API Principles
- [x] Resource-based URLs (/users, /tasks, /tasks/{id}) ✅
- [x] Standard HTTP methods (GET, POST, PUT, PATCH, DELETE) ✅
- [x] Proper status codes (200, 201, 400, 401, 403, 404, 500) ✅
- [x] JSON request/response bodies ✅
- [x] Consistent error response format ✅
- [x] Idempotent operations (GET, PUT, DELETE) ✅

**Status**: PASS - RESTful design following industry standards

### **Constitution Check Result: ✅ ALL GATES PASSED**

No violations detected. All 7 constitutional principles satisfied by the planned architecture.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-fullstack-app/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (/sp.specify output)
├── research.md          # Phase 0 output (technology decisions, patterns)
├── data-model.md        # Phase 1 output (database schema, entities)
├── quickstart.md        # Phase 1 output (getting started guide)
├── contracts/           # Phase 1 output (API and DB contracts)
│   ├── auth-api.md      # Authentication endpoints specification
│   ├── tasks-api.md     # Task CRUD endpoints specification
│   ├── database-schema.md  # User and Task table schemas
│   ├── ui-components.md    # Frontend component specifications
│   └── ui-flows.md         # User flow diagrams
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root - Monorepo Structure)

```text
# Monorepo with frontend + backend
backend/
├── src/
│   ├── api/
│   │   ├── routes/          # API route handlers
│   │   │   ├── auth.py      # Registration, login, logout endpoints
│   │   │   └── tasks.py     # Task CRUD endpoints
│   │   ├── middleware/      # JWT validation, CORS, error handling
│   │   └── dependencies.py  # Dependency injection (DB session, user auth)
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py  # User registration, authentication logic
│   │   └── task_service.py  # Task CRUD operations with user isolation
│   ├── models/              # SQLModel data models
│   │   ├── user.py          # User model (email, password_hash, timestamps)
│   │   └── task.py          # Task model (title, description, completed, user_id)
│   ├── core/
│   │   ├── config.py        # Settings (env vars, DB URL, JWT secret)
│   │   ├── security.py      # Password hashing, JWT encode/decode
│   │   └── database.py      # SQLModel engine, session management
│   └── main.py              # FastAPI app initialization, CORS, routes
├── alembic/                 # Database migrations
│   └── versions/            # Migration scripts
├── tests/
│   ├── integration/         # API integration tests
│   ├── unit/                # Service and model unit tests
│   └── conftest.py          # Pytest fixtures
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── pyproject.toml           # Python project configuration

frontend/
├── src/
│   ├── app/                 # Next.js app directory (App Router)
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Landing/home page
│   │   ├── login/
│   │   │   └── page.tsx     # Login page
│   │   ├── register/
│   │   │   └── page.tsx     # Registration page
│   │   └── dashboard/
│   │       └── page.tsx     # Task dashboard (protected route)
│   ├── components/          # React components
│   │   ├── TaskList.tsx     # Display list of tasks
│   │   ├── TaskForm.tsx     # Create/edit task form
│   │   ├── TaskItem.tsx     # Individual task display
│   │   └── AuthGuard.tsx    # Protected route wrapper
│   ├── lib/
│   │   ├── api.ts           # API client (Axios/Fetch wrapper)
│   │   ├── auth.ts          # Auth utilities (JWT storage, logout)
│   │   └── types.ts         # TypeScript interfaces (User, Task, API responses)
│   └── hooks/
│       ├── useAuth.ts       # Authentication hook
│       └── useTasks.ts      # Task data fetching hook
├── public/                  # Static assets
├── .env.local.example       # Example environment variables
├── package.json             # Node dependencies
├── tsconfig.json            # TypeScript configuration
└── next.config.js           # Next.js configuration

# Root level (monorepo)
.env                         # Environment variables (NEVER commit)
.gitignore                   # Ignore .env, node_modules, __pycache__, etc.
README.md                    # Project setup and documentation
```

**Structure Decision**: Selected **Web application (Option 2)** structure with monorepo organization. This decision aligns with the requirement for "Next.js frontend + FastAPI backend" and enables:
- Independent development and deployment of frontend/backend
- Clear separation of concerns (Constitution Principle III)
- Shared repository for simplified version control and CI/CD
- Backend can be tested independently via API endpoints
- Frontend can be developed against backend API contracts

## Complexity Tracking

> No constitution violations requiring justification.

All complexity is justified by functional requirements:
- Monorepo structure: Required for frontend + backend coordination
- SQLModel ORM: Required for type-safe database operations and migrations
- JWT authentication: Required by Constitution Principle IV
- Service layer: Required by Constitution Principle VI (clean architecture)
- User-level filtering: Required by Constitution Principle V (NON-NEGOTIABLE)

No unnecessary abstractions or premature optimization detected.
