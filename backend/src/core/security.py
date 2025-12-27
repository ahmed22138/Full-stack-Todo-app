"""Security utilities for password hashing and JWT token management."""
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from .config import get_settings

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Create a JWT access token for a user.

    Args:
        user_id: User ID to encode in token

    Returns:
        Encoded JWT token string
    """
    expire = datetime.utcnow() + timedelta(hours=settings.jwt_access_token_expire_hours)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int:
    """Decode a JWT token and extract user ID.

    Args:
        token: JWT token string

    Returns:
        User ID from token

    Raises:
        jwt.InvalidTokenError: If token is invalid or expired
    """
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    user_id = int(payload["sub"])
    return user_id
