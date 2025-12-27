# Tasks: Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-todo-fullstack-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/, research.md

**Tests**: Tests are OPTIONAL - not explicitly requested in spec, so test tasks are excluded from this breakdown.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo**: `backend/` and `frontend/` at repository root
- Backend paths: `backend/src/`, `backend/tests/`
- Frontend paths: `frontend/src/`, `frontend/public/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create monorepo directory structure (backend/, frontend/, .gitignore, README.md)
- [X] T002 [P] Initialize backend Python project with pyproject.toml and requirements.txt
- [X] T003 [P] Initialize frontend Next.js project with package.json and tsconfig.json
- [X] T004 [P] Create backend .env.example file with DATABASE_URL, JWT_SECRET_KEY, CORS_ORIGINS placeholders
- [X] T005 [P] Create frontend .env.local.example file with NEXT_PUBLIC_API_URL placeholder
- [X] T006 [P] Add .env and .env.local to .gitignore
- [ ] T007 [P] Install backend dependencies (FastAPI, SQLModel, Alembic, PyJWT, passlib, python-dotenv, uvicorn)
- [ ] T008 [P] Install frontend dependencies (Next.js, React, Axios, TailwindCSS, TypeScript)
- [X] T009 Configure TailwindCSS for frontend in tailwind.config.js and globals.css

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [X] T010 Initialize Alembic in backend/alembic/ directory
- [X] T011 Create SQLModel base configuration in backend/src/core/database.py (engine, session maker)
- [X] T012 [P] Create User model in backend/src/models/user.py (id, email, password_hash, created_at)
- [X] T013 [P] Create Task model in backend/src/models/task.py (id, title, description, completed, user_id, created_at, updated_at)
- [X] T014 Generate Alembic migration for User and Task tables in backend/alembic/versions/
- [X] T015 Create database configuration loader in backend/src/core/config.py (Settings class with pydantic-settings)

### Security Foundation

- [X] T016 [P] Implement password hashing functions in backend/src/core/security.py (hash_password, verify_password using passlib/bcrypt)
- [X] T017 [P] Implement JWT functions in backend/src/core/security.py (create_access_token, decode_access_token using PyJWT)
- [X] T018 Create JWT authentication dependency in backend/src/api/dependencies.py (get_current_user extracts user_id from token)
- [X] T019 Create database session dependency in backend/src/api/dependencies.py (get_db provides SQLModel session)

### API Foundation

- [X] T020 Create FastAPI app initialization in backend/src/main.py (app instance, CORS middleware, startup/shutdown events)
- [X] T021 Configure CORS middleware in backend/src/main.py (allow origins from environment variable)
- [X] T022 Create error handler middleware in backend/src/api/middleware/error_handler.py (consistent error response format)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 FOUNDATION

**Goal**: Enable users to register, login, and authenticate for multi-user isolation

**Independent Test**: Register new user, login with credentials, verify JWT token received, logout and verify session terminated

### Implementation for User Story 1

- [X] T023 [P] [US1] Create UserCreate Pydantic schema in backend/src/models/user.py (email, password validation)
- [X] T024 [P] [US1] Create UserLogin Pydantic schema in backend/src/models/user.py (email, password)
- [X] T025 [P] [US1] Create UserResponse Pydantic schema in backend/src/models/user.py (id, email, created_at - no password)
- [X] T026 [US1] Implement register_user function in backend/src/services/auth_service.py (check email uniqueness, hash password, create user)
- [X] T027 [US1] Implement authenticate_user function in backend/src/services/auth_service.py (validate credentials, verify password hash)
- [X] T028 [US1] Implement get_user_by_email function in backend/src/services/auth_service.py (database query)
- [X] T029 [US1] Implement POST /auth/register endpoint in backend/src/api/routes/auth.py (call register_user service, return 201)
- [X] T030 [US1] Implement POST /auth/login endpoint in backend/src/api/routes/auth.py (call authenticate_user, generate JWT, return token + user)
- [X] T031 [US1] Implement POST /auth/logout endpoint in backend/src/api/routes/auth.py (return success message, client-side token deletion)
- [X] T032 [US1] Implement GET /auth/me endpoint in backend/src/api/routes/auth.py (require JWT, return current user)
- [X] T033 [US1] Register auth routes in backend/src/main.py (app.include_router for /auth endpoints)

### Frontend for User Story 1

- [X] T034 [P] [US1] Create TypeScript types in frontend/src/lib/types.ts (User, LoginRequest, RegisterRequest, AuthResponse)
- [X] T035 [P] [US1] Create Axios API client in frontend/src/lib/api.ts (base URL, request/response interceptors for JWT)
- [X] T036 [P] [US1] Create auth API functions in frontend/src/lib/api.ts (register, login, logout, getCurrentUser)
- [X] T037 [P] [US1] Create useAuth hook in frontend/src/hooks/useAuth.ts (auth state, login/logout/register functions)
- [X] T038 [US1] Create registration page in frontend/src/app/register/page.tsx (email/password form, call register API)
- [X] T039 [US1] Create login page in frontend/src/app/login/page.tsx (email/password form, call login API, store JWT)
- [X] T040 [US1] Create AuthGuard component in frontend/src/components/AuthGuard.tsx (protect routes, redirect if not authenticated)
- [X] T041 [US1] Create logout button component in frontend/src/components/LogoutButton.tsx (call logout API, clear token, redirect to login)
- [X] T042 [US1] Update root layout in frontend/src/app/layout.tsx (add navigation, logout button if authenticated)

**Checkpoint**: User Story 1 complete - Users can register, login, and authenticate. Multi-user foundation established.

---

## Phase 4: User Story 2 - Create and View Todo Tasks (Priority: P2) 🎯 MVP

**Goal**: Enable authenticated users to create new tasks and view their task list

**Independent Test**: Login as user, create multiple tasks with titles/descriptions, verify tasks appear in list, verify only user's own tasks visible

### Implementation for User Story 2

- [X] T043 [P] [US2] Create TaskCreate Pydantic schema in backend/src/models/task.py (title, description validation)
- [X] T044 [P] [US2] Create TaskResponse Pydantic schema in backend/src/models/task.py (all task fields)
- [X] T045 [US2] Implement create_task function in backend/src/services/task_service.py (auto-assign user_id, validate title, save task)
- [X] T046 [US2] Implement get_user_tasks function in backend/src/services/task_service.py (filter by user_id, sort by created_at DESC)
- [X] T047 [US2] Implement get_task_by_id function in backend/src/services/task_service.py (filter by task_id AND user_id for data isolation)
- [X] T048 [US2] Implement POST /tasks endpoint in backend/src/api/routes/tasks.py (require JWT, call create_task service, return 201)
- [X] T049 [US2] Implement GET /tasks endpoint in backend/src/api/routes/tasks.py (require JWT, call get_user_tasks service, return task list)
- [X] T050 [US2] Implement GET /tasks/{id} endpoint in backend/src/api/routes/tasks.py (require JWT, call get_task_by_id, return 404 if not found/unauthorized)
- [X] T051 [US2] Register task routes in backend/src/main.py (app.include_router for /tasks endpoints)

### Frontend for User Story 2

- [X] T052 [P] [US2] Create Task TypeScript type in frontend/src/lib/types.ts (id, title, description, completed, user_id, timestamps)
- [X] T053 [P] [US2] Create task API functions in frontend/src/lib/api.ts (getTasks, getTask, createTask)
- [X] T054 [P] [US2] Create useTasks hook in frontend/src/hooks/useTasks.ts (fetch tasks, create task, state management)
- [X] T055 [US2] Create TaskList component in frontend/src/components/TaskList.tsx (display tasks, handle empty state)
- [X] T056 [US2] Create TaskItem component in frontend/src/components/TaskItem.tsx (display single task with title, description, timestamps)
- [X] T057 [US2] Create TaskForm component in frontend/src/components/TaskForm.tsx (create task form with title/description fields, validation)
- [X] T058 [US2] Create dashboard page in frontend/src/app/dashboard/page.tsx (protected route, show TaskList and TaskForm)
- [X] T059 [US2] Add "Add Task" button to dashboard that shows TaskForm component
- [X] T060 [US2] Update login page redirect to /dashboard after successful authentication

**Checkpoint**: User Story 2 complete (MVP) - Users can create and view their personal todo tasks. Basic todo functionality operational.

---

## Phase 5: User Story 3 - Update and Delete Todo Tasks (Priority: P3)

**Goal**: Enable users to edit and delete their existing tasks

**Independent Test**: Create tasks, edit titles/descriptions, delete tasks, verify changes persist, verify cannot modify other users' tasks

### Implementation for User Story 3

- [X] T061 [P] [US3] Create TaskUpdate Pydantic schema in backend/src/models/task.py (optional title, description, completed fields)
- [X] T062 [US3] Implement update_task function in backend/src/services/task_service.py (filter by task_id AND user_id, update fields, update updated_at timestamp)
- [X] T063 [US3] Implement delete_task function in backend/src/services/task_service.py (filter by task_id AND user_id, delete from database)
- [X] T064 [US3] Implement PUT /tasks/{id} endpoint in backend/src/api/routes/tasks.py (require JWT, call update_task service, return updated task)
- [ ] T065 [US3] Implement PATCH /tasks/{id} endpoint in backend/src/api/routes/tasks.py (require JWT, partial update, call update_task service)
- [X] T066 [US3] Implement DELETE /tasks/{id} endpoint in backend/src/api/routes/tasks.py (require JWT, call delete_task service, return 204)

### Frontend for User Story 3

- [X] T067 [P] [US3] Add updateTask and deleteTask functions to frontend/src/lib/api.ts (PUT/PATCH and DELETE requests)
- [X] T068 [P] [US3] Add update and delete functions to frontend/src/hooks/useTasks.ts (call API, update local state)
- [X] T069 [US3] Create TaskEditForm component in frontend/src/components/TaskEditForm.tsx (pre-filled form for editing task)
- [X] T070 [US3] Add "Edit" button to TaskItem component that shows TaskEditForm
- [X] T071 [US3] Add "Delete" button to TaskItem component with confirmation dialog
- [X] T072 [US3] Implement optimistic UI updates in useTasks hook (update local state before API response)
- [X] T073 [US3] Add error handling for failed update/delete operations (revert optimistic updates, show error message)

**Checkpoint**: User Story 3 complete - Users have full CRUD control over their tasks.

---

## Phase 6: User Story 4 - Mark Tasks as Complete/Incomplete (Priority: P4)

**Goal**: Enable users to track progress by marking tasks complete or incomplete

**Independent Test**: Create tasks, toggle completion status, verify visual indicators, verify persistence, test filtering by status

### Implementation for User Story 4

- [X] T074 [US4] Implement toggle_task_completion function in backend/src/services/task_service.py (filter by task_id AND user_id, toggle completed boolean, update updated_at)
- [X] T075 [US4] Implement PATCH /tasks/{id}/toggle endpoint in backend/src/api/routes/tasks.py (require JWT, call toggle_task_completion service)
- [ ] T076 [US4] Update GET /tasks endpoint to support completed query parameter (filter by status)

### Frontend for User Story 4

- [X] T077 [P] [US4] Add toggleTask function to frontend/src/lib/api.ts (PATCH /tasks/{id}/toggle)
- [X] T078 [P] [US4] Add toggle function to frontend/src/hooks/useTasks.ts (call API, update local state)
- [X] T079 [US4] Add checkbox to TaskItem component for toggling completion status
- [X] T080 [US4] Add visual styling to TaskItem for completed tasks (strikethrough text, muted colors)
- [ ] T081 [US4] Add filter buttons to dashboard ("All", "Active", "Completed")
- [ ] T082 [US4] Implement filter logic in useTasks hook (filter tasks based on completed status)

**Checkpoint**: User Story 4 complete - Users can track progress with completion status and filtering.

---

## Phase 7: Security & Validation (Cross-Cutting Concerns)

**Purpose**: Ensure security, validation, and data integrity across all features

- [ ] T083 [P] Add input validation for email format in backend/src/models/user.py (Pydantic EmailStr)
- [ ] T084 [P] Add password strength validation in backend/src/models/user.py (min 8 characters)
- [ ] T085 [P] Add title length validation in backend/src/models/task.py (max 200 characters)
- [ ] T086 [P] Add description length validation in backend/src/models/task.py (max 2000 characters)
- [ ] T087 [P] Add empty title validation in backend/src/models/task.py (min 1 character, no whitespace-only)
- [ ] T088 [P] Add error handling for duplicate email in backend/src/api/routes/auth.py (return 409 Conflict)
- [ ] T089 [P] Add error handling for invalid credentials in backend/src/api/routes/auth.py (return 401 Unauthorized)
- [ ] T090 [P] Add 404 response for non-existent/unauthorized tasks in backend/src/api/routes/tasks.py (prevent info leakage per FR-026)
- [ ] T091 [P] Add request validation error handling in backend/src/api/middleware/error_handler.py (return 400 with field details)
- [ ] T092 [P] Add frontend form validation in registration page (email format, password length)
- [ ] T093 [P] Add frontend form validation in task form (title required, character limits)
- [ ] T094 [P] Add loading states to all frontend forms (disable submit during API calls)
- [ ] T095 [P] Add error display components in frontend/src/components/ (show API error messages to user)
- [ ] T096 Verify all task service functions include user_id filter (data isolation audit)
- [ ] T097 Test cross-user access prevention (attempt to access another user's task by ID)

---

## Phase 8: API Client Integration & Polish

**Purpose**: Complete API integration and improve user experience

- [ ] T098 [P] Add JWT token refresh logic in frontend/src/lib/api.ts (before token expiration)
- [ ] T099 [P] Add 401 error interceptor in frontend/src/lib/api.ts (redirect to login on authentication failure)
- [ ] T100 [P] Add network error handling in frontend/src/lib/api.ts (retry logic, offline detection)
- [ ] T101 [P] Add request cancellation in useTasks hook (cancel pending requests on component unmount)
- [ ] T102 [P] Add task sorting options to dashboard (by date, title, completion status)
- [ ] T103 [P] Add pagination to GET /tasks endpoint (limit, offset query parameters)
- [ ] T104 [P] Implement pagination in frontend TaskList component (load more button or infinite scroll)
- [ ] T105 [P] Add empty state messages ("No tasks yet", "All tasks completed")
- [ ] T106 [P] Add confirmation dialogs for destructive actions (delete task, logout)
- [ ] T107 [P] Improve UI styling with TailwindCSS (responsive design, dark mode support)
- [ ] T108 [P] Add loading skeletons for task list (while fetching from API)
- [ ] T109 [P] Add toast notifications for success/error messages (task created, task deleted, etc.)

---

## Phase 9: Documentation & Deployment Preparation

**Purpose**: Finalize documentation and prepare for deployment

- [ ] T110 [P] Create README.md with project overview, tech stack, and setup instructions
- [ ] T111 [P] Document environment variables in backend/.env.example and frontend/.env.local.example
- [ ] T112 [P] Create backend/requirements.txt with all dependencies and versions
- [ ] T113 [P] Create quickstart guide following specs/001-todo-fullstack-app/quickstart.md
- [ ] T114 [P] Add API documentation in backend/src/main.py (FastAPI auto-docs configuration)
- [ ] T115 [P] Verify .gitignore excludes .env files, node_modules, __pycache__, etc.
- [ ] T116 Run Alembic migrations on fresh database (verify schema creation)
- [ ] T117 Verify full authentication flow end-to-end (register → login → access protected route → logout)
- [ ] T118 Verify data isolation (create tasks as User A, login as User B, confirm no cross-user access)
- [ ] T119 Run linting on backend code (flake8 or black)
- [ ] T120 Run linting on frontend code (ESLint, Prettier)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion (can run in parallel with US1 if different developers, but US1 provides authentication needed by US2)
- **User Story 3 (Phase 5)**: Depends on User Story 2 completion (requires tasks to exist)
- **User Story 4 (Phase 6)**: Depends on User Story 2 completion (requires tasks to exist, can run in parallel with US3)
- **Security & Validation (Phase 7)**: Can start after Foundational, integrate as user stories progress
- **API Client Integration (Phase 8)**: Depends on user stories being functional
- **Documentation (Phase 9)**: Can run in parallel with implementation phases

### User Story Dependencies

**Critical Path**:
```
Setup → Foundational → US1 (Auth) → US2 (Create/View) → US3 (Update/Delete) / US4 (Complete)
                                                               ↓
                                          Security & Validation → API Polish → Documentation
```

**Independent Paths After Foundational**:
- **Path 1 (MVP)**: US1 → US2 (minimal viable product)
- **Path 2 (Full CRUD)**: US2 → US3 (complete task management)
- **Path 3 (Progress Tracking)**: US2 → US4 (completion status)

### Within Each User Story

1. **US1 (Authentication)**:
   - Backend: Schemas → Services → Routes (sequential)
   - Frontend: Types & API client → Hooks → Pages & Components (sequential)
   - Backend and Frontend can develop in parallel

2. **US2 (Create/View Tasks)**:
   - Backend: Schemas → Services → Routes (sequential)
   - Frontend: Types & API client → Hooks → Components → Dashboard (sequential)
   - Backend and Frontend can develop in parallel

3. **US3 (Update/Delete)**:
   - Backend: Schema → Service functions → Routes (sequential)
   - Frontend: API functions → Hook updates → Component updates (sequential)
   - Backend and Frontend can develop in parallel

4. **US4 (Mark Complete)**:
   - Backend: Service function → Route → Endpoint update (sequential)
   - Frontend: API function → Hook update → Component updates → Filter UI (sequential)
   - Backend and Frontend can develop in parallel

### Parallel Opportunities

**Setup Phase**: T002, T003, T004, T005, T006, T007, T008 can all run in parallel

**Foundational Phase**:
- T012, T013 (User and Task models) can run in parallel
- T016, T017 (Password hashing and JWT functions) can run in parallel
- After T019: Backend foundation tasks independent of frontend

**User Story 1**:
- T023, T024, T025 (Pydantic schemas) can run in parallel
- T034, T035, T036, T037 (Frontend types and API client) can run in parallel
- Backend tasks (T023-T033) and Frontend tasks (T034-T042) can develop in parallel

**User Story 2**:
- T043, T044 (Pydantic schemas) can run in parallel
- T052, T053, T054 (Frontend types and hooks) can run in parallel
- Backend (T043-T051) and Frontend (T052-T060) can develop in parallel

**Security & Validation Phase**: Almost all tasks (T083-T095) can run in parallel (different files)

**API Polish Phase**: Most tasks (T098-T109) can run in parallel (different concerns)

**Documentation Phase**: All tasks (T110-T115) can run in parallel

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Backend Team (or concurrent tasks)
Task T023: Create UserCreate schema
Task T024: Create UserLogin schema
Task T025: Create UserResponse schema

# After schemas complete:
Task T026: Implement register_user service
Task T027: Implement authenticate_user service
Task T028: Implement get_user_by_email service

# After services complete:
Task T029: POST /auth/register route
Task T030: POST /auth/login route
Task T031: POST /auth/logout route
Task T032: GET /auth/me route

# Frontend Team (can work in parallel with backend)
Task T034: Create TypeScript types
Task T035: Create Axios API client
Task T036: Create auth API functions
Task T037: Create useAuth hook

# After frontend foundation:
Task T038: Registration page
Task T039: Login page
Task T040: AuthGuard component
Task T041: Logout button component
Task T042: Update root layout
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 Only)

**Recommended for initial delivery**:

1. **Phase 1**: Setup (T001-T009)
2. **Phase 2**: Foundational (T010-T022)
3. **Phase 3**: User Story 1 - Authentication (T023-T042)
4. **Phase 4**: User Story 2 - Create/View Tasks (T043-T060)
5. **STOP and VALIDATE**: Test MVP end-to-end
   - Register user → Login → Create tasks → View tasks → Logout
   - Test data isolation (create second user, verify separate task lists)
6. **Deploy/Demo MVP** (if ready)

**MVP Delivers**:
- Multi-user authentication
- Personal todo list (create and view)
- Data isolation between users
- Functional web application

**Deferred to Post-MVP**:
- Edit/delete tasks (US3)
- Mark complete/incomplete (US4)
- Advanced features (polish, pagination, etc.)

### Incremental Delivery

**Full feature rollout**:

1. **Setup + Foundational** → Foundation ready
2. **Add User Story 1** → Test independently → Users can register/login
3. **Add User Story 2** → Test independently → MVP deployed (basic todo app)
4. **Add User Story 3** → Test independently → Full CRUD functionality
5. **Add User Story 4** → Test independently → Complete todo app with progress tracking
6. **Add Security & Polish** → Production-ready deployment

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. **All team members**: Complete Setup + Foundational together
2. **Once Foundational complete**:
   - **Developer A**: User Story 1 (Authentication) - PRIORITY (blocks others)
   - **Developer B**: Security & Validation setup (T083-T087) - can start early
   - **Developer C**: Documentation (T110-T115) - can prepare in parallel
3. **After US1 complete**:
   - **Developer A**: User Story 2 (Create/View)
   - **Developer B**: User Story 4 (Mark Complete) - can prep in parallel
4. **After US2 complete**:
   - **Developer A**: User Story 3 (Update/Delete)
   - **Developer B**: API Client Integration (T098-T109)
5. **Final**: All team members integrate and test

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** = maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **Data Isolation Critical**: Every task query MUST filter by user_id (validate in T096)
- **Security First**: JWT validation required on all protected endpoints
- **Error Handling**: Return 404 (not 403) for unauthorized task access (T090)
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 120 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 9 tasks
- Phase 2 (Foundational): 13 tasks
- Phase 3 (User Story 1 - Authentication): 20 tasks
- Phase 4 (User Story 2 - Create/View): 18 tasks
- Phase 5 (User Story 3 - Update/Delete): 13 tasks
- Phase 6 (User Story 4 - Mark Complete): 9 tasks
- Phase 7 (Security & Validation): 15 tasks
- Phase 8 (API Client Integration & Polish): 12 tasks
- Phase 9 (Documentation): 11 tasks

**MVP Scope** (Recommended first delivery):
- Phase 1: Setup (9 tasks)
- Phase 2: Foundational (13 tasks)
- Phase 3: User Story 1 (20 tasks)
- Phase 4: User Story 2 (18 tasks)
- **Total MVP**: 60 tasks

**Parallel Opportunities**: 70+ tasks marked with [P] can run in parallel with other tasks in same phase
