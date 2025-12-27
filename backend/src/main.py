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

# Configure CORS with wildcard support
import re

def get_cors_origins():
    """Get CORS origins with wildcard pattern support."""
    origins_list = settings.cors_origins.split(",")
    processed_origins = []

    for origin in origins_list:
        origin = origin.strip()
        # Convert wildcard patterns to regex
        if "*" in origin:
            # Convert *.vercel.app to regex pattern
            pattern = origin.replace(".", r"\.").replace("*", r".*")
            processed_origins.append(pattern)
        else:
            processed_origins.append(origin)

    return processed_origins

def check_origin(origin: str) -> bool:
    """Check if origin is allowed based on patterns."""
    allowed_origins = get_cors_origins()

    for allowed in allowed_origins:
        # If it's a regex pattern (contains .*)
        if ".*" in allowed:
            if re.match(f"^{allowed}$", origin):
                return True
        # Exact match
        elif origin == allowed:
            return True

    return False

# Use allow_origin_regex for wildcard support
origins_patterns = get_cors_origins()
# Check if we have wildcard patterns
has_wildcard = any(".*" in pattern for pattern in origins_patterns)

if has_wildcard:
    # Combine all patterns into one regex
    combined_pattern = "|".join(f"({pattern})" for pattern in origins_patterns)
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=combined_pattern,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Use regular allow_origins for exact matches
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins_patterns,
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
