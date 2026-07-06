import time
import abc
from pathlib import Path
from app.analyzers.schemas import AnalysisResult

class BaseAnalyzer(abc.ABC):
    def __init__(self, tool_name: str):
        self.tool_name = tool_name

    async def run(self, workspace_path: Path) -> AnalysisResult:
        start_time = time.time()
        try:
            result = await self.analyze(workspace_path)
            result.execution_time_ms = int((time.time() - start_time) * 1000)
            result.tool_name = self.tool_name
            return result
        except Exception as e:
            return AnalysisResult(
                tool_name=self.tool_name,
                success=False,
                errors=[str(e)],
                execution_time_ms=int((time.time() - start_time) * 1000)
            )

    @abc.abstractmethod
    async def analyze(self, workspace_path: Path) -> AnalysisResult:
        """
        Perform the actual analysis and return a normalized result.
        """
        pass
