"""Dependency injection for authentication and database sessions."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel import Session
from ..core.database import get_session
from ..core.security import decode_access_token
import jwt

security = HTTPBearer()


def get_db() -> Session:
    """Get database session dependency.

    Yields:
        Database session
    """
    return Depends(get_session)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
) -> int:
    """Get current authenticated user ID from JWT token.

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        User ID from token

    Raises:
        HTTPException: If token is invalid or expired (401 Unauthorized)
    """
    token = credentials.credentials

    try:
        user_id = decode_access_token(token)
        return user_id
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "unauthorized",
                "message": "Invalid or expired token"
            }
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "unauthorized",
                "message": "Authentication required"
            }
        )
