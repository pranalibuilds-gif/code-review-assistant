import time
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import RequestIDMiddleware, LoggingMiddleware
from app.core.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from app.api.v1 import auth, submissions, reviews, dashboard, admin

# Initialize logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Custom Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# Register Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# API v1 Router
api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    """
    Health check endpoint to verify system status.
    """
    return {
        "success": True,
        "data": {
            "status": "online",
            "service": "codesage-api",
            "version": settings.VERSION,
            "timestamp": time.time(),
            "environment": settings.ENVIRONMENT
        }
    }

@api_router.get("/system/info")
async def system_info():
    """
    Detailed system information (intended for development).
    """
    return {
        "success": True,
        "data": {
            "project_name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "api_prefix": settings.API_V1_STR,
            "debug_mode": settings.DEBUG,
            "ollama_config": {
                "base_url": settings.OLLAMA_BASE_URL,
                "model": settings.OLLAMA_MODEL
            }
        }
    }

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
