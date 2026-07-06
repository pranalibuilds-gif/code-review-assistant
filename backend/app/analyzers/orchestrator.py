import asyncio
import logging
from pathlib import Path
from typing import List, Dict
from app.analyzers.pylint_analyzer import PylintAnalyzer
from app.analyzers.bandit_analyzer import BanditAnalyzer
from app.analyzers.radon_analyzer import RadonAnalyzer
from app.analyzers.schemas import AnalysisResult, NormalizedFinding, NormalizedMetric
from app.models.enums import ReviewStatus

logger = logging.getLogger(__name__)

class StaticAnalysisOrchestrator:
    def __init__(self):
        self.analyzers = [
            PylintAnalyzer(),
            BanditAnalyzer(),
            RadonAnalyzer()
        ]

    async def run_all(self, workspace_path: str) -> Dict:
        path = Path(workspace_path)

        logger.info(f"Starting parallel static analysis for workspace: {workspace_path}")

        # Run all analyzers concurrently
        tasks = [analyzer.run(path) for analyzer in self.analyzers]
        results: List[AnalysisResult] = await asyncio.gather(*tasks)

        aggregated_findings: List[NormalizedFinding] = []
        aggregated_metrics: List[NormalizedMetric] = []
        execution_metadata = []

        success_count = 0
        for res in results:
            if res.success:
                success_count += 1
                aggregated_findings.extend(res.findings)
                aggregated_metrics.extend(res.metrics)

            execution_metadata.append({
                "tool": res.tool_name,
                "success": res.success,
                "duration_ms": res.execution_time_ms,
                "errors": res.errors
            })

            logger.info(f"Analyzer {res.tool_name} finished in {res.execution_time_ms}ms. Success: {res.success}")

        # Determine overall status
        if success_count == len(self.analyzers):
            status = ReviewStatus.COMPLETED
        elif success_count > 0:
            status = ReviewStatus.PARTIAL_SUCCESS
        else:
            status = ReviewStatus.FAILED

        return {
            "status": status,
            "findings": aggregated_findings,
            "metrics": aggregated_metrics,
            "metadata": execution_metadata
        }
