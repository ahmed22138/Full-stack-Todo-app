"""Authentication service - business logic for user registration and login."""
from sqlmodel import Session, select
from fastapi import HTTPException, status
from ..models.user import User, UserCreate, UserLogin
from ..core.security import hash_password, verify_password, create_access_token


def get_user_by_email(db: Session, email: str) -> User | None:
    """Retrieve user by email address.

    Args:
        db: Database session
        email: User's email address

    Returns:
        User object if found, None otherwise
    """
    statement = select(User).where(User.email == email)
    result = db.exec(statement)
    return result.first()


def register_user(db: Session, user_data: UserCreate) -> User:
    """Register a new user account.

    Args:
        db: Database session
        user_data: User registration data (email, password)

    Returns:
        Created User object

    Raises:
        HTTPException: If email already exists (409 Conflict)
    """
    # Check if email already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "email_already_exists"}
        )

    # Hash password and create user
    password_hash = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, credentials: UserLogin) -> tuple[User, str]:
    """Authenticate user with email and password.

    Args:
        db: Database session
        credentials: Login credentials (email, password)

    Returns:
        Tuple of (User object, JWT access token)

    Raises:
        HTTPException: If credentials are invalid (401 Unauthorized)
    """
    # Get user by email
    user = get_user_by_email(db, credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "invalid_credentials"}
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "invalid_credentials"}
        )

    # Generate JWT token
    access_token = create_access_token(user.id)

    return user, access_token


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Retrieve user by ID.

    Args:
        db: Database session
        user_id: User's ID

    Returns:
        User object if found, None otherwise
    """
    return db.get(User, user_id)
