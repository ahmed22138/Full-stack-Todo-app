"""Task model and schemas."""
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional
from .user import User


class Task(SQLModel, table=True):
    """Task model representing a todo item owned by a user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(
        max_length=200,
        min_length=1,
        sa_column_kwargs={"nullable": False}
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000
    )
    completed: bool = Field(
        default=False,
        sa_column_kwargs={"nullable": False}
    )
    user_id: int = Field(
        foreign_key="user.id",
        sa_column_kwargs={"nullable": False},
        index=True
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )

    # Relationship: many tasks belong to one user
    user: User = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed}, user_id={self.user_id})>"


class TaskCreate(SQLModel):
    """Schema for task creation request."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskUpdate(SQLModel):
    """Schema for task update request (all fields optional)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = None


class TaskResponse(SQLModel):
    """Schema for task data in API responses."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
