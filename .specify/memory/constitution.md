# Todo Full Stack Web Application Constitution

<!--
Sync Impact Report:
Version: 1.0.0 (Initial ratification)
Modified Principles: All principles newly defined
Added Sections:
  - Core Principles (7 principles)
  - Architecture Standards
  - Development Workflow
  - Governance
Removed Sections: None
Templates Requiring Updates:
  ✅ plan-template.md - Updated (Constitution Check section aligns with principles)
  ✅ spec-template.md - Updated (Requirements align with functional/data isolation principles)
  ✅ tasks-template.md - Updated (Task organization supports independent testing and clean architecture)
Follow-up TODOs: None
-->

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**All development must follow the spec-driven workflow strictly:**
- Features begin with specification (`/sp.specify`)
- Specifications are planned before implementation (`/sp.plan`)
- Tasks are generated from plans (`/sp.tasks`)
- Implementation follows tasks (`/sp.implement`)
- No manual coding outside of Claude Code workflow

**Rationale**: Ensures consistency, traceability, and prevents scope creep. Specifications serve as single source of truth for requirements, design decisions, and acceptance criteria.

### II. Read Specs Before Implementation (NON-NEGOTIABLE)

**Before implementing any task or feature:**
- MUST read the corresponding spec.md file
- MUST read the plan.md for architectural context
- MUST understand acceptance criteria and constraints
- MUST verify task aligns with specification

**Rationale**: Prevents implementation drift, ensures work matches requirements, and maintains alignment between specification and delivered code.

### III. Frontend-Backend Separation

**Clear separation between presentation and business logic:**
- Backend handles all business logic, data validation, and persistence
- Frontend focuses solely on presentation and user interaction
- No business rules duplicated in frontend
- Communication via well-defined REST APIs only
- Backend must be functional independently of frontend

**Rationale**: Enables independent development, testing, and deployment. Facilitates future client applications (mobile, desktop) without backend changes. Simplifies testing and maintenance.

### IV. JWT-Based Authentication

**All API authentication uses JSON Web Tokens:**
- Stateless authentication via JWT
- Tokens contain user identity and claims
- Backend validates JWT on every protected endpoint
- No server-side session storage
- Token expiration and refresh mechanism required

**Rationale**: Stateless architecture scales horizontally, reduces server memory overhead, and simplifies distributed deployments. Standard approach for modern web APIs.

### V. User-Level Data Isolation (NON-NEGOTIABLE)

**Every user's data must be strictly isolated:**
- Database queries MUST filter by authenticated user ID
- Users cannot access other users' data under any circumstance
- Authorization checks required on ALL data operations (create, read, update, delete)
- Test coverage MUST include cross-user access prevention

**Rationale**: Security and privacy requirement. Prevents unauthorized data access, maintains user trust, and ensures compliance with data protection principles.

### VI. Clean Architecture

**Code must follow clean architecture principles:**
- Separation of concerns: models, services, controllers/routes, views
- Business logic in service layer, not in routes or controllers
- Models represent data structures and relationships only
- Dependency flow: routes → services → models
- No circular dependencies

**Rationale**: Maintainable, testable code that adapts to changing requirements. Business logic reuse across multiple interfaces. Clear responsibility boundaries.

### VII. RESTful API Principles

**APIs must follow REST conventions:**
- Resource-based URLs (nouns, not verbs)
- Standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- JSON request/response bodies
- Consistent error response format
- Idempotent operations where appropriate (GET, PUT, DELETE)

**Rationale**: Industry-standard conventions ensure predictability, ease of integration, and developer familiarity. Clear semantics for operations.

## Architecture Standards

### Technology Stack Requirements

- **Backend Framework**: Must support REST API development with clear MVC/service patterns
- **Authentication**: JWT library with secure token generation and validation
- **Database**: Relational database with migration support
- **API Documentation**: OpenAPI/Swagger or equivalent for contract documentation
- **Environment Configuration**: `.env` files for secrets and configuration (NEVER commit secrets)

### Security Requirements

- **Authentication**: All protected endpoints require valid JWT
- **Authorization**: User-level access control on all data operations
- **Input Validation**: Validate and sanitize all user inputs
- **Error Handling**: Never expose internal details in error messages
- **Secrets Management**: Use environment variables, never hardcode credentials
- **HTTPS**: Production deployments must use HTTPS

### Data Management

- **Migrations**: All schema changes via migration scripts
- **Referential Integrity**: Enforce foreign key constraints
- **User Association**: All user-specific tables include user_id foreign key
- **Soft Deletes**: Consider soft deletes for user data (optional, based on requirements)

## Development Workflow

### Specification Phase
1. User provides feature description
2. Run `/sp.specify` to create spec.md with user stories and requirements
3. Run `/sp.clarify` if requirements need refinement
4. User reviews and approves specification

### Planning Phase
1. Run `/sp.plan` to create implementation plan
2. Research existing codebase patterns
3. Define data models, API contracts, and architecture
4. User reviews and approves plan

### Task Generation Phase
1. Run `/sp.tasks` to generate actionable task list
2. Tasks organized by user story for independent testing
3. Include foundational tasks that block user stories
4. User reviews task breakdown

### Implementation Phase
1. Run `/sp.implement` to execute tasks
2. Follow TDD when tests are specified
3. Commit after each task or logical group
4. Validate at story checkpoints

### Code Review Requirements
- All changes must reference spec and task IDs
- Security review for authentication/authorization changes
- Data isolation verification for database operations
- API contract verification against plan

### Quality Gates
- **Before Implementation**: Specification approved, plan reviewed
- **During Implementation**: Tests pass (if included), no hardcoded secrets
- **Before Commit**: Code follows architecture principles, user data isolated
- **Before Deploy**: Integration tests pass, API documentation updated

## Governance

### Amendment Process
1. Constitution changes require explicit user approval
2. Version bump follows semantic versioning (MAJOR.MINOR.PATCH)
3. All dependent templates and documentation updated
4. Changes documented in Sync Impact Report

### Compliance Verification
- All PRs must verify compliance with constitution principles
- Violations require explicit justification in plan.md Complexity Tracking section
- Security and data isolation principles are NON-NEGOTIABLE

### Version Control
- Constitution changes tracked in git with clear commit messages
- ADRs created for significant architectural decisions
- PHRs created for all user interactions and implementation work

### Enforcement
- Automated checks where possible (linting, security scans)
- Manual review for architecture and data isolation compliance
- User data isolation violations result in immediate fix requirement

**Version**: 1.0.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2025-12-26
