"""Global error handling middleware for FastAPI."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors.

    Returns consistent error format for validation failures.
    """
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"][1:])  # Skip 'body'
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Validation error on {request.url.path}: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "validation_error", "details": errors}
    )


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """Handle database integrity constraint violations.

    Returns user-friendly error messages for common integrity errors.
    """
    error_msg = str(exc.orig)

    # Handle unique constraint violations
    if "unique constraint" in error_msg.lower() or "duplicate key" in error_msg.lower():
        if "email" in error_msg.lower():
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"error": "email_already_exists"}
            )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "duplicate_entry"}
        )

    # Handle foreign key constraint violations
    if "foreign key constraint" in error_msg.lower():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "invalid_reference"}
        )

    # Generic integrity error
    logger.error(f"Database integrity error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "database_constraint_violation"}
    )


async def sqlalchemy_error_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Handle general SQLAlchemy database errors."""
    logger.error(f"Database error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "database_error"}
    )


async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle all unhandled exceptions.

    Logs the error and returns a generic error response.
    """
    logger.exception(f"Unhandled exception on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "internal_server_error"}
    )


def register_error_handlers(app):
    """Register all error handlers with the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)
