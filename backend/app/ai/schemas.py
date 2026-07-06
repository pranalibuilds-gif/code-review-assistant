from typing import List, Optional
from pydantic import BaseModel
from app.analyzers.schemas import NormalizedFinding

class AIRecommendation(BaseModel):
    title: str
    description: str
    impact: str

class AIReviewResult(BaseModel):
    summary: str
    overall_assessment: str
    findings: List[NormalizedFinding] = []
    recommendations: List[AIRecommendation] = []
    success: bool = True
    error: Optional[str] = None
    execution_time_ms: int = 0
    model_name: str = ""
