from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.enums import ReviewStatus, Severity, FindingSource

class FindingDTO(BaseModel):
    source: FindingSource
    severity: Severity
    category: Optional[str] = None
    title: str
    description: Optional[str] = None
    recommendation: Optional[str] = None
    file_path: Optional[str] = None
    line: Optional[int] = None
    rule_id: Optional[str] = None

class MetricDTO(BaseModel):
    metric_name: str
    metric_value: float
    unit: Optional[str] = None

class TrendDTO(BaseModel):
    score_delta: float = 0.0
    findings_delta: int = 0
    complexity_delta: float = 0.0
    maintainability_delta: float = 0.0

class StatisticsDTO(BaseModel):
    total_findings: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    security_count: int = 0
    quality_count: int = 0
    complexity_count: int = 0
    files_analyzed: int = 0
    duration_ms: int = 0

class CanonicalReviewReport(BaseModel):
    review_id: UUID
    submission_id: UUID
    project_id: UUID
    score: float
    grade: str
    status: ReviewStatus
    summary: Optional[str] = None
    ai_summary: Optional[str] = None
    recommendations: List[Dict[str, str]] = []
    findings: List[FindingDTO] = []
    metrics: List[MetricDTO] = []
    statistics: StatisticsDTO
    trend: TrendDTO
    created_at: datetime
    finished_at: Optional[datetime] = None
