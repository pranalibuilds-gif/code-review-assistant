import json
import asyncio
from pathlib import Path
from typing import List
from app.analyzers.base import BaseAnalyzer
from app.analyzers.schemas import AnalysisResult, NormalizedMetric
from app.models.enums import FindingSource

class RadonAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(tool_name="Radon")

    async def analyze(self, workspace_path: Path) -> AnalysisResult:
        src_path = workspace_path / "src"

        # We run Radon Complexity (cc) and Maintainability Index (mi)
        cc_process = await asyncio.create_subprocess_exec(
            "radon", "cc", "-j", str(src_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        mi_process = await asyncio.create_subprocess_exec(
            "radon", "mi", "-j", str(src_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        cc_out, cc_err = await cc_process.communicate()
        mi_out, mi_err = await mi_process.communicate()

        metrics = []

        # Parse CC
        try:
            cc_data = json.loads(cc_out.decode())
            total_complexity = 0
            count = 0
            for file, items in cc_data.items():
                for item in items:
                    total_complexity += item.get("complexity", 0)
                    count += 1

            if count > 0:
                metrics.append(NormalizedMetric(
                    source=FindingSource.RADON,
                    metric_name="Average Cyclomatic Complexity",
                    metric_value=round(total_complexity / count, 2)
                ))
        except:
            pass

        # Parse MI
        try:
            mi_data = json.loads(mi_out.decode())
            total_mi = 0
            count = 0
            for file, mi_val in mi_data.items():
                total_mi += mi_val.get("mi", 0)
                count += 1

            if count > 0:
                metrics.append(NormalizedMetric(
                    source=FindingSource.RADON,
                    metric_name="Maintainability Index",
                    metric_value=round(total_mi / count, 2)
                ))
        except:
            pass

        return AnalysisResult(
            tool_name=self.tool_name,
            success=True,
            metrics=metrics
        )
