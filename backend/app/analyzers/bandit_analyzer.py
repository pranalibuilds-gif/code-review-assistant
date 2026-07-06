import json
import asyncio
from pathlib import Path
from app.analyzers.base import BaseAnalyzer
from app.analyzers.schemas import AnalysisResult, NormalizedFinding
from app.models.enums import Severity, FindingSource

class BanditAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(tool_name="Bandit")

    def _map_severity(self, bandit_severity: str) -> Severity:
        mapping = {
            "LOW": Severity.LOW,
            "MEDIUM": Severity.MEDIUM,
            "HIGH": Severity.HIGH,
        }
        return mapping.get(bandit_severity, Severity.LOW)

    async def analyze(self, workspace_path: Path) -> AnalysisResult:
        src_path = workspace_path / "src"

        process = await asyncio.create_subprocess_exec(
            "bandit",
            "-f", "json",
            "-r", str(src_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        # Bandit returns non-zero if issues are found, so we check stdout
        if not stdout:
            return AnalysisResult(
                tool_name=self.tool_name,
                success=False,
                errors=[stderr.decode().strip()]
            )

        try:
            data = json.loads(stdout.decode())
            raw_results = data.get("results", [])
        except json.JSONDecodeError:
            return AnalysisResult(tool_name=self.tool_name, success=False, errors=["Failed to parse Bandit output"])

        findings = []
        for item in raw_results:
            findings.append(NormalizedFinding(
                source=FindingSource.BANDIT,
                severity=self._map_severity(item.get("issue_severity")),
                category="Security",
                title=item.get("issue_text"),
                description=f"Confidence: {item.get('issue_confidence')}. {item.get('issue_text')}",
                recommendation=f"See: {item.get('more_info')}",
                file_path=item.get("filename"),
                line=item.get("line_number"),
                rule_id=item.get("test_id")
            ))

        return AnalysisResult(
            tool_name=self.tool_name,
            success=True,
            findings=findings
        )
