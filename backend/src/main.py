"""FastAPI application initialization and configuration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .core.database import create_db_and_tables
from .api.middleware.error_handler import register_error_handlers

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="Multi-user Todo application with JWT authentication",
    version="0.1.0",
    debug=settings.debug
)

# Configure CORS
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register error handlers
register_error_handlers(app)

# Register API routers
from .api.routes import auth, tasks
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    create_db_and_tables()


@app.get("/")
def root():
    """Root endpoint - API health check."""
    return {
        "message": "Todo API is running",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
