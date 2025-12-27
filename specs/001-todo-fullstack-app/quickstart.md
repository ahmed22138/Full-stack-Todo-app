# Quickstart Guide: Todo Full-Stack Web Application

**Date**: 2025-12-26
**Feature**: Todo Full-Stack Web Application
**Branch**: 001-todo-fullstack-app

## Overview

This guide walks you through setting up and running the Todo application locally for development.

**Architecture**: Monorepo with FastAPI backend and Next.js frontend
**Database**: Neon PostgreSQL (cloud-hosted)
**Authentication**: JWT tokens with PyJWT

---

## Prerequisites

- **Python 3.11+** - Backend runtime
- **Node.js 18+** and **npm/yarn** - Frontend runtime
- **Git** - Version control
- **Neon PostgreSQL Account** - Free tier available at [neon.tech](https://neon.tech)

---

## Initial Setup

### 1. Clone Repository and Checkout Branch

```bash
git clone <repository-url>
cd todo_full_stack_web_application
git checkout 001-todo-fullstack-app
```

### 2. Create Neon PostgreSQL Database

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Create a database named `todo_db`
4. Copy the connection string (format: `postgresql://user:pass@host/dbname`)

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlmodel` - ORM (Pydantic + SQLAlchemy)
- `alembic` - Database migrations
- `pyjwt` - JWT token management
- `passlib[bcrypt]` - Password hashing
- `python-dotenv` - Environment variables
- `psycopg2-binary` - PostgreSQL driver

### 4. Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# backend/.env

# Database
DATABASE_URL=postgresql://user:password@neon-host/todo_db?sslmode=require

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-min-32-characters-long-change-this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24

# CORS (Frontend URL)
CORS_ORIGINS=http://localhost:3000

# Application
DEBUG=True
```

**Important**:
- Replace `DATABASE_URL` with your actual Neon connection string
- Generate a secure `JWT_SECRET_KEY` (minimum 32 random characters)
- Never commit `.env` to git (already in `.gitignore`)

**Generate Secure JWT Secret**:
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

### 5. Initialize Database with Alembic

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Generate initial migration
alembic revision --autogenerate -m "Initial schema with user and task tables"

# Apply migrations
alembic upgrade head
```

**Verify Migration**:
```bash
alembic current
# Should show: (head)
```

### 6. Run Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

**Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend**:
- Open browser: `http://localhost:8000/docs`
- You should see FastAPI Swagger UI with API documentation

---

## Frontend Setup

### 1. Navigate to Frontend Directory (New Terminal)

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

**Key Dependencies**:
- `next` - React framework
- `react` & `react-dom` - UI library
- `axios` - HTTP client
- `tailwindcss` - CSS framework (optional)
- `typescript` - Type safety

### 3. Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```bash
# frontend/.env.local

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note**: `NEXT_PUBLIC_` prefix exposes variable to browser (safe for non-sensitive config).

### 4. Run Frontend Server

```bash
npm run dev
# or
yarn dev
```

**Output**:
```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
- Network:      http://192.168.1.x:3000

✓ Ready in 2.3s
```

**Verify Frontend**:
- Open browser: `http://localhost:3000`
- You should see the Todo app homepage

---

## Verify Full Stack Integration

### 1. Test Authentication Flow

1. **Register**: Navigate to `http://localhost:3000/register`
   - Enter email: `test@example.com`
   - Enter password: `password123`
   - Click "Register"
   - Should redirect to login

2. **Login**: Navigate to `http://localhost:3000/login`
   - Enter credentials
   - Click "Login"
   - Should redirect to dashboard

3. **Dashboard**: You should see empty task list with "Add Task" button

### 2. Test Task Operations

1. **Create Task**:
   - Click "Add Task"
   - Enter title: "Test Todo"
   - Enter description: "This is a test"
   - Click "Save"
   - Task should appear in list

2. **Mark Complete**:
   - Click checkbox on task
   - Task should show as completed (strikethrough)

3. **Edit Task**:
   - Click "Edit" button
   - Modify title/description
   - Click "Save"
   - Changes should persist

4. **Delete Task**:
   - Click "Delete" button
   - Confirm deletion
   - Task should disappear

### 3. Test Data Isolation

1. **Create Second User**:
   - Logout
   - Register new user: `test2@example.com`
   - Login as new user
   - Dashboard should be empty (no tasks from first user)

2. **Verify Isolation**:
   - Create tasks as second user
   - Logout and login as first user
   - Should only see first user's tasks

---

## Development Workflow

### Backend Development

**Start Backend (with Auto-Reload)**:
```bash
cd backend
uvicorn src.main:app --reload
```

**Run Tests**:
```bash
pytest
```

**Create New Migration**:
```bash
# After modifying SQLModel models
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

**View API Documentation**:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Development

**Start Frontend (with Hot Reload)**:
```bash
cd frontend
npm run dev
```

**Build for Production**:
```bash
npm run build
npm start
```

**Type Check**:
```bash
npx tsc --noEmit
```

---

## Common Issues & Solutions

### Issue: "Database connection failed"

**Cause**: Invalid DATABASE_URL or Neon database not accessible

**Solution**:
1. Verify Neon database is running
2. Check DATABASE_URL format in `.env`
3. Ensure `sslmode=require` is included
4. Test connection: `psql <DATABASE_URL>`

### Issue: "401 Unauthorized" on protected endpoints

**Cause**: Missing or invalid JWT token

**Solution**:
1. Check JWT_SECRET_KEY matches between token generation and validation
2. Verify Authorization header format: `Bearer <token>`
3. Check token expiration (24 hours default)
4. Re-login to get fresh token

### Issue: "CORS policy blocked"

**Cause**: Frontend origin not in CORS_ORIGINS

**Solution**:
1. Add `http://localhost:3000` to CORS_ORIGINS in backend `.env`
2. Restart backend server
3. Clear browser cache

### Issue: "Password validation failed" during registration

**Cause**: Password < 8 characters

**Solution**:
- Use password with minimum 8 characters
- Check frontend validation matches backend rules

### Issue: Tasks not appearing after creation

**Cause**: User ID mismatch or database query issue

**Solution**:
1. Check browser console for API errors
2. Verify JWT contains correct user ID: Decode at [jwt.io](https://jwt.io)
3. Check backend logs for SQL errors
4. Verify task was created: `SELECT * FROM task;` in database

---

## Environment Configuration Summary

### Backend (.env)

| Variable                         | Required | Example                                    |
|----------------------------------|----------|--------------------------------------------|
| DATABASE_URL                     | Yes      | postgresql://user:pass@host/db?sslmode=... |
| JWT_SECRET_KEY                   | Yes      | Random 32+ character string                |
| JWT_ALGORITHM                    | No       | HS256 (default)                            |
| JWT_ACCESS_TOKEN_EXPIRE_HOURS    | No       | 24 (default)                               |
| CORS_ORIGINS                     | Yes      | http://localhost:3000                      |
| DEBUG                            | No       | True (development only)                    |

### Frontend (.env.local)

| Variable               | Required | Example                  |
|------------------------|----------|--------------------------|
| NEXT_PUBLIC_API_URL    | Yes      | http://localhost:8000    |

---

## Deployment Checklist

Before deploying to production:

- [ ] Set DEBUG=False in backend .env
- [ ] Use strong JWT_SECRET_KEY (32+ random characters)
- [ ] Update CORS_ORIGINS to production frontend URL
- [ ] Use HTTPS for both frontend and backend
- [ ] Enable Neon PostgreSQL connection pooling
- [ ] Set up environment variables in hosting platform
- [ ] Never commit .env files to git
- [ ] Run database migrations on production: `alembic upgrade head`
- [ ] Test authentication flow end-to-end
- [ ] Verify data isolation with multiple users
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting for API endpoints

---

## Useful Commands Reference

### Backend

```bash
# Start development server
uvicorn src.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Create migration
alembic revision --autogenerate -m "message"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Format code
black src/

# Lint code
flake8 src/
```

### Frontend

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Type check
npx tsc --noEmit

# Lint
npm run lint

# Format
npm run format
```

---

## Next Steps

1. **Implement Features**: Follow `/sp.tasks` to generate task breakdown
2. **Write Tests**: Add integration tests for data isolation
3. **Add UI Enhancements**: Improve styling with TailwindCSS
4. **Deploy**: Choose hosting platforms (Vercel for frontend, Railway/Render for backend)
5. **Monitor**: Set up logging and error tracking (Sentry)

---

## Support & Resources

- **API Documentation**: `http://localhost:8000/docs`
- **Spec**: `specs/001-todo-fullstack-app/spec.md`
- **Plan**: `specs/001-todo-fullstack-app/plan.md`
- **Data Model**: `specs/001-todo-fullstack-app/data-model.md`
- **API Contracts**: `specs/001-todo-fullstack-app/contracts/`

---

## Security Reminders

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Use strong JWT secrets** - Minimum 32 random characters
3. **Always filter by user_id** - Constitution Principle V (NON-NEGOTIABLE)
4. **Hash passwords** - Use bcrypt, never store plaintext
5. **Use HTTPS in production** - Protect tokens in transit
6. **Validate all inputs** - SQLModel + Pydantic handle this
7. **Return 404 (not 403)** - Prevent task existence discovery (FR-026)
