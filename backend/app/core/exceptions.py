import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all for any unhandled exceptions.
    Returns a consistent JSON response and logs the error.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=True,
        extra={"request_id": request_id}
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please contact support.",
                "request_id": request_id
            }
        },
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handler for explicit HTTP exceptions.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_EXCEPTION",
                "message": exc.detail,
                "request_id": request_id
            }
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler for Pydantic validation errors.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    errors = exc.errors()

    msg = "Input validation failed."
    if errors:
        error = errors[0]
        field = " -> ".join([str(loc) for loc in error.get("loc", [])])
        msg = f"Validation Error: {error.get('msg')} ({field})"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": msg,
                "details": errors,
                "request_id": request_id
            }
        },
    )
