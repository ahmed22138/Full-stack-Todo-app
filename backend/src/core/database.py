"""Database configuration and session management."""
from sqlmodel import create_engine, Session, SQLModel
from .config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,  # Verify connections before using
)


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session (dependency injection)."""
    with Session(engine) as session:
        yield session
