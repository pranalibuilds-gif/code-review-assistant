import json
import asyncio
from pathlib import Path
from app.analyzers.base import BaseAnalyzer
from app.analyzers.schemas import AnalysisResult, NormalizedFinding
from app.models.enums import Severity, FindingSource

class PylintAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(tool_name="Pylint")

    def _map_severity(self, pylint_type: str) -> Severity:
        mapping = {
            "convention": Severity.INFO,
            "refactor": Severity.LOW,
            "warning": Severity.MEDIUM,
            "error": Severity.HIGH,
            "fatal": Severity.CRITICAL,
        }
        return mapping.get(pylint_type, Severity.INFO)

    async def analyze(self, workspace_path: Path) -> AnalysisResult:
        src_path = workspace_path / "src"

        # Run pylint as a subprocess
        process = await asyncio.create_subprocess_exec(
            "pylint",
            "--output-format=json",
            "--recursive=y",
            str(src_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0 and not stdout:
            return AnalysisResult(
                tool_name=self.tool_name,
                success=False,
                errors=[stderr.decode().strip()]
            )

        try:
            raw_findings = json.loads(stdout.decode())
        except json.JSONDecodeError:
            # Pylint might output nothing if no issues found or return a non-JSON error
            return AnalysisResult(tool_name=self.tool_name, success=True)

        findings = []
        for item in raw_findings:
            findings.append(NormalizedFinding(
                source=FindingSource.PYLINT,
                severity=self._map_severity(item.get("type")),
                category=item.get("message-id"),
                title=item.get("symbol"),
                description=item.get("message"),
                file_path=item.get("path"),
                line=item.get("line"),
                column=item.get("column"),
                rule_id=item.get("message-id")
            ))

        return AnalysisResult(
            tool_name=self.tool_name,
            success=True,
            findings=findings
        )
