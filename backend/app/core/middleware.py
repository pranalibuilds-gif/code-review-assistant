import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject a unique Request ID into every request context.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Store request_id in state so it can be accessed by handlers or loggers
        request.state.request_id = request_id

        start_time = time.time()

        # Perform the actual request
        response = await call_next(request)

        process_time = time.time() - start_time

        # Add Request ID to response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log incoming requests and their completion status.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = getattr(request.state, "request_id", "unknown")

        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={"request_id": request_id}
        )

        response = await call_next(request)

        logger.info(
            f"Request completed: {response.status_code}",
            extra={"request_id": request_id}
        )

        return response
