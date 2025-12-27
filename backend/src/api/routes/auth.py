"""Authentication API routes - register, login, logout, current user."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ...models.user import User, UserCreate, UserLogin, UserResponse
from ...services.auth_service import register_user, authenticate_user, get_user_by_id
from ...api.dependencies import get_session, get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_session)
):
    """Register a new user account.

    Args:
        user_data: User registration data (email, password)
        db: Database session (injected)

    Returns:
        Created user data (without password)

    Raises:
        409: Email already exists
        422: Validation error
    """
    user = register_user(db, user_data)
    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


@router.post("/login")
def login(
    credentials: UserLogin,
    db: Session = Depends(get_session)
):
    """Authenticate user and return JWT access token.

    Args:
        credentials: Login credentials (email, password)
        db: Database session (injected)

    Returns:
        Access token and user data

    Raises:
        401: Invalid credentials
        422: Validation error
    """
    user, access_token = authenticate_user(db, credentials)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
    }


@router.post("/logout")
def logout():
    """Logout endpoint (client-side token deletion).

    Returns:
        Success message

    Note:
        JWT tokens are stateless. Actual logout is handled client-side
        by removing the token from storage. This endpoint exists for
        consistency and future extension (e.g., token blacklisting).
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get current authenticated user's information.

    Args:
        user_id: Current user ID from JWT (injected)
        db: Database session (injected)

    Returns:
        Current user data (without password)

    Raises:
        401: Unauthorized (invalid/missing token)
        404: User not found
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "user_not_found"}
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )
