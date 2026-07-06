import json
import time
import httpx
import logging
from typing import Optional
from app.ai.base import AIProvider
from app.ai.schemas import AIReviewResult
from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaProvider(AIProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = 60.0  # Seconds

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False

    async def review(self, prompt: str) -> AIReviewResult:
        start_time = time.time()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                }

                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                response.raise_for_status()

                data = response.json()
                content = data.get("response", "")

                result_dict = json.loads(content)

                execution_time = int((time.time() - start_time) * 1000)

                return AIReviewResult(
                    summary=result_dict.get("summary", "No summary provided."),
                    overall_assessment=result_dict.get("overall_assessment", "N/A"),
                    findings=result_dict.get("findings", []),
                    recommendations=result_dict.get("recommendations", []),
                    success=True,
                    execution_time_ms=execution_time,
                    model_name=self.model
                )

        except Exception as e:
            logger.error(f"Ollama review failed: {str(e)}")
            return AIReviewResult(
                summary="AI review failed.",
                overall_assessment="Error during inference.",
                success=False,
                error=str(e),
                execution_time_ms=int((time.time() - start_time) * 1000),
                model_name=self.model
            )
