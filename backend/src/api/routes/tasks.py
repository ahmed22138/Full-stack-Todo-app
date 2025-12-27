"""Task API routes - CRUD operations for todo tasks."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ...models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from ...services.task_service import (
    create_task,
    get_user_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task_completion
)
from ...api.dependencies import get_session, get_current_user

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create a new task for the authenticated user.

    Args:
        task_data: Task creation data (title, description)
        user_id: Current user ID from JWT (injected)
        db: Database session (injected)

    Returns:
        Created task data

    Raises:
        401: Unauthorized (invalid/missing token)
        422: Validation error
    """
    task = create_task(db, task_data, user_id)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.get("", response_model=list[TaskResponse])
def get_tasks(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all tasks for the authenticated user.

    Args:
        user_id: Current user ID from JWT (injected)
        db: Database session (injected)

    Returns:
        List of user's tasks (sorted by created_at DESC)

    Raises:
        401: Unauthorized (invalid/missing token)
    """
    tasks = get_user_tasks(db, user_id)
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get a specific task by ID.

    Args:
        task_id: ID of the task to retrieve
        user_id: Current user ID from JWT (injected)
        db: Database session (injected)

    Returns:
        Task data

    Raises:
        401: Unauthorized (invalid/missing token)
        404: Task not found or doesn't belong to user
    """
    task = get_task_by_id(db, task_id, user_id)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update an existing task.

    Args:
        task_id: ID of the task to update
        task_data: Updated task data (title, description, completed)
        user_id: Current user ID from JWT (injected)
        db: Database session (injected)

    Returns:
        Updated task data

    Raises:
        401: Unauthorized (invalid/missing token)
        404: Task not found or doesn't belong to user
        422: Validation error
    """
    task = update_task(db, task_id, task_data, user_id)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete a task.

    Args:
        task_id: ID of the task to delete
        user_id: Current user ID from JWT (injected)
        db: Database session (injected)

    Returns:
        No content (204)

    Raises:
        401: Unauthorized (invalid/missing token)
        404: Task not found or doesn't belong to user
    """
    delete_task(db, task_id, user_id)


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task(
    task_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Toggle the completion status of a task.

    Args:
        task_id: ID of the task to toggle
        user_id: Current user ID from JWT (injected)
        db: Database session (injected)

    Returns:
        Updated task data with toggled completion status

    Raises:
        401: Unauthorized (invalid/missing token)
        404: Task not found or doesn't belong to user
    """
    task = toggle_task_completion(db, task_id, user_id)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
