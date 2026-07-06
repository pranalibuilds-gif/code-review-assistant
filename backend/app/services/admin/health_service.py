import psutil
import time
import httpx
import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.ai.ollama_provider import OllamaProvider

logger = logging.getLogger(__name__)

class SystemHealthService:
    def __init__(self, db: Session):
        self.db = db
        self.ollama = OllamaProvider()

    async def get_full_health(self) -> Dict[str, Any]:
        """
        Aggregates health status from all critical components.
        """
        db_health = self._check_database()
        ai_health = await self._check_ai()
        storage_health = self._check_storage()

        # Determine overall status
        statuses = [db_health["status"], ai_health["status"], storage_health["status"]]

        if "unhealthy" in statuses:
            overall = "unhealthy"
        elif "degraded" in statuses:
            overall = "degraded"
        else:
            overall = "healthy"

        return {
            "status": overall,
            "timestamp": time.time(),
            "services": {
                "database": db_health,
                "ai": ai_health,
                "storage": storage_health,
                "api": {
                    "status": "healthy",
                    "version": settings.VERSION,
                    "environment": settings.ENVIRONMENT
                }
            }
        }

    def _check_database(self) -> Dict[str, Any]:
        try:
            start_time = time.time()
            self.db.execute(text("SELECT 1"))
            latency = int((time.time() - start_time) * 1000)
            return {
                "status": "healthy",
                "latency_ms": latency
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    async def _check_ai(self) -> Dict[str, Any]:
        is_up = await self.ollama.is_available()
        return {
            "status": "healthy" if is_up else "degraded",
            "provider": "ollama",
            "model": settings.OLLAMA_MODEL,
            "base_url": settings.OLLAMA_BASE_URL
        }

    def _check_storage(self) -> Dict[str, Any]:
        try:
            usage = psutil.disk_usage(settings.UPLOAD_DIR)
            status = "healthy"
            if usage.percent > 90:
                status = "unhealthy"
            elif usage.percent > 75:
                status = "degraded"

            return {
                "status": status,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percent_used": usage.percent
            }
        except Exception as e:
            return {"status": "unknown", "error": str(e)}
