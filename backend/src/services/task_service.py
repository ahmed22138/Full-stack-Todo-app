"""Task service - business logic for task CRUD operations."""
from sqlmodel import Session, select
from datetime import datetime
from fastapi import HTTPException, status
from ..models.task import Task, TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate, user_id: int) -> Task:
    """Create a new task for the authenticated user.

    Args:
        db: Database session
        task_data: Task creation data (title, description)
        user_id: ID of the authenticated user

    Returns:
        Created Task object
    """
    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id,
        completed=False
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_user_tasks(db: Session, user_id: int) -> list[Task]:
    """Get all tasks for a specific user, sorted by creation date (newest first).

    Args:
        db: Database session
        user_id: ID of the user

    Returns:
        List of Task objects belonging to the user
    """
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    result = db.exec(statement)
    return result.all()


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task:
    """Get a specific task by ID, ensuring it belongs to the authenticated user.

    Args:
        db: Database session
        task_id: ID of the task
        user_id: ID of the authenticated user

    Returns:
        Task object if found and belongs to user

    Raises:
        HTTPException: If task not found or doesn't belong to user (404)
    """
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "task_not_found"}
        )

    # Ensure task belongs to the authenticated user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "task_not_found"}
        )

    return task


def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
    user_id: int
) -> Task:
    """Update an existing task.

    Args:
        db: Database session
        task_id: ID of the task to update
        task_data: Updated task data (title, description, completed)
        user_id: ID of the authenticated user

    Returns:
        Updated Task object

    Raises:
        HTTPException: If task not found or doesn't belong to user (404)
    """
    task = get_task_by_id(db, task_id, user_id)

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    """Delete a task.

    Args:
        db: Database session
        task_id: ID of the task to delete
        user_id: ID of the authenticated user

    Raises:
        HTTPException: If task not found or doesn't belong to user (404)
    """
    task = get_task_by_id(db, task_id, user_id)

    db.delete(task)
    db.commit()


def toggle_task_completion(db: Session, task_id: int, user_id: int) -> Task:
    """Toggle the completion status of a task.

    Args:
        db: Database session
        task_id: ID of the task to toggle
        user_id: ID of the authenticated user

    Returns:
        Updated Task object with toggled completion status

    Raises:
        HTTPException: If task not found or doesn't belong to user (404)
    """
    task = get_task_by_id(db, task_id, user_id)

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
