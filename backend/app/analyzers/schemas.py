from typing import List, Optional
from pydantic import BaseModel
from app.models.enums import Severity, FindingSource

class NormalizedFinding(BaseModel):
    source: FindingSource
    severity: Severity
    category: Optional[str] = None
    title: str
    description: Optional[str] = None
    recommendation: Optional[str] = None
    file_path: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    rule_id: Optional[str] = None

class NormalizedMetric(BaseModel):
    source: FindingSource
    metric_name: str
    metric_value: float
    unit: Optional[str] = None

class AnalysisResult(BaseModel):
    tool_name: str
    success: bool
    findings: List[NormalizedFinding] = []
    metrics: List[NormalizedMetric] = []
    errors: List[str] = []
    execution_time_ms: int = 0
    version: Optional[str] = None
