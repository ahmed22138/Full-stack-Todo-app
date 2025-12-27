"""User model and schemas."""
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from pydantic import EmailStr
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


class User(SQLModel, table=True):
    """User account model for authentication and task ownership."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(
        unique=True,
        index=True,
        max_length=255,
        sa_column_kwargs={"nullable": False}
    )
    password_hash: str = Field(
        max_length=255,
        sa_column_kwargs={"nullable": False}
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )

    # Relationship: one user has many tasks
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class UserCreate(SQLModel):
    """Schema for user registration request."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(SQLModel):
    """Schema for user login request."""
    email: EmailStr
    password: str


class UserResponse(SQLModel):
    """Schema for user data in API responses (no password)."""
    id: int
    email: str
    created_at: datetime
