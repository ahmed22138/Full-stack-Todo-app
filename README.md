# Todo Full-Stack Web Application

A multi-user todo application built with FastAPI (backend) and Next.js (frontend), featuring JWT authentication and user-level data isolation.

## 🏗️ Architecture

**Monorepo Structure**:
- `backend/` - FastAPI REST API with PostgreSQL
- `frontend/` - Next.js React application

**Tech Stack**:
- **Backend**: Python 3.11+, FastAPI, SQLModel, Alembic, PyJWT, Passlib
- **Frontend**: Next.js 14+, React 18+, TypeScript, Axios, TailwindCSS
- **Database**: Neon PostgreSQL (serverless PostgreSQL)
- **Authentication**: JWT tokens (stateless, 24-hour expiration)

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher (with npm)
- Neon PostgreSQL account ([neon.tech](https://neon.tech))
- Git

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd todo_full_stack_web_application
git checkout 001-todo-fullstack-app
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your Neon PostgreSQL connection string and JWT secret
```

**Generate JWT Secret** (secure random string):
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local if needed (default: http://localhost:8000)
```

### 4. Database Setup

```bash
cd backend

# Initialize Alembic
alembic init alembic

# Generate initial migration
alembic revision --autogenerate -m "Initial schema with user and task tables"

# Run migrations
alembic upgrade head
```

### 5. Run Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Backend ReDoc**: http://localhost:8000/redoc

## 📖 Implementation Status

**Current Phase**: Setup Complete ✅

**Phases Remaining**:
- [ ] Phase 2: Foundational (Database models, security, middleware)
- [ ] Phase 3: User Story 1 - Authentication (Register, Login, Logout)
- [ ] Phase 4: User Story 2 - Create/View Tasks (MVP)
- [ ] Phase 5: User Story 3 - Update/Delete Tasks
- [ ] Phase 6: User Story 4 - Mark Complete/Incomplete
- [ ] Phase 7: Security & Validation
- [ ] Phase 8: API Client Integration & Polish
- [ ] Phase 9: Documentation & Deployment

**Next Steps**: Follow `specs/001-todo-fullstack-app/tasks.md` for detailed implementation tasks.

## 📝 Development Workflow

### Backend Development

```bash
# Run tests
pytest

# Format code
black src/

# Lint code
flake8 src/

# Create new migration
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Frontend Development

```bash
# Run in development mode
npm run dev

# Build for production
npm run build
npm start

# Lint
npm run lint

# Format
npm run format
```

## 🔐 Security Features

- **JWT Authentication**: Stateless authentication with 24-hour token expiration
- **Password Hashing**: Bcrypt algorithm with automatic salting
- **User-Level Data Isolation**: All queries filtered by authenticated user ID
- **CORS Protection**: Configured to allow only trusted origins
- **Input Validation**: Pydantic models validate all API inputs
- **404 for Unauthorized**: Returns 404 (not 403) to prevent information leakage

## 📚 Documentation

- **Specification**: `specs/001-todo-fullstack-app/spec.md`
- **Implementation Plan**: `specs/001-todo-fullstack-app/plan.md`
- **Task Breakdown**: `specs/001-todo-fullstack-app/tasks.md`
- **Data Model**: `specs/001-todo-fullstack-app/data-model.md`
- **API Contracts**: `specs/001-todo-fullstack-app/contracts/`
- **Quickstart Guide**: `specs/001-todo-fullstack-app/quickstart.md`

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest --cov=src --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🚢 Deployment

### Backend Deployment (Railway/Render)

1. Set environment variables in hosting platform
2. Run database migrations: `alembic upgrade head`
3. Deploy FastAPI application
4. Verify CORS_ORIGINS includes production frontend URL

### Frontend Deployment (Vercel/Netlify)

1. Set `NEXT_PUBLIC_API_URL` to production backend URL
2. Build and deploy Next.js application
3. Verify API connectivity

## 🤝 Contributing

1. Follow the spec-driven development workflow
2. Read specifications before implementation
3. Maintain frontend-backend separation
4. Ensure user-level data isolation in all queries
5. Follow clean architecture principles
6. Use RESTful API conventions

## 📄 License

[Your License]

## 🆘 Support

For issues or questions, refer to:
- API Documentation: http://localhost:8000/docs
- Specification: `specs/001-todo-fullstack-app/spec.md`
- Task List: `specs/001-todo-fullstack-app/tasks.md`
