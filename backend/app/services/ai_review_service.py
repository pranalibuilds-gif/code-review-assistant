import logging
import os
from typing import List, Dict
from pathlib import Path
from app.ai.ollama_provider import OllamaProvider
from app.ai.prompt_builder import PromptBuilder
from app.ai.schemas import AIReviewResult
from app.analyzers.schemas import NormalizedFinding, NormalizedMetric

logger = logging.getLogger(__name__)

class AIReviewService:
    def __init__(self):
        self.provider = OllamaProvider()
        self.builder = PromptBuilder()

    async def run_review(
        self,
        src_path: str,
        static_findings: List[NormalizedFinding],
        metrics: List[NormalizedMetric]
    ) -> AIReviewResult:

        # 1. Check availability
        if not await self.provider.is_available():
            logger.warning("Ollama is not available. Skipping AI review.")
            return AIReviewResult(
                summary="AI Insights Unavailable: AI Service Offline",
                overall_assessment="Unknown (AI Offline)",
                success=False,
                error="Provider unreachable"
            )

        # 2. Gather source code
        files_content = self._load_source_files(src_path)

        # 3. Build prompt
        prompt = self.builder.build_review_prompt(
            language="Python",
            files_content=files_content,
            static_findings=static_findings,
            metrics=metrics
        )

        # 4. Perform review
        logger.info("Sending prompt to AI provider...")
        result = await self.provider.review(prompt)

        return result

    def _load_source_files(self, src_path: str) -> Dict[str, str]:
        contents = {}
        path = Path(src_path)
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    full_path = Path(root) / file
                    rel_path = os.path.relpath(full_path, path)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            contents[rel_path] = f.read()
                    except Exception:
                        continue
        return contents
