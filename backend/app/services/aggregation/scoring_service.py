from typing import List, Dict
from app.models.enums import Severity, FindingSource
from .dto import FindingDTO, MetricDTO

class ScoringService:
    WEIGHTS = {
        "SECURITY": 0.40,
        "RELIABILITY": 0.25,
        "MAINTAINABILITY": 0.20,
        "AI": 0.15
    }

    PENALTIES = {
        Severity.CRITICAL: 20,
        Severity.HIGH: 10,
        Severity.MEDIUM: 5,
        Severity.LOW: 2,
        Severity.INFO: 0
    }

    @classmethod
    def calculate_overall_score(cls, findings: List[FindingDTO], metrics: List[MetricDTO]) -> float:
        # 1. Group findings by category
        security_findings = [f for f in findings if f.source == FindingSource.BANDIT]
        reliability_findings = [f for f in findings if f.source == FindingSource.PYLINT]
        ai_findings = [f for f in findings if f.source == FindingSource.AI]

        # 2. Calculate category scores
        security_score = cls._calculate_category_score(security_findings)
        reliability_score = cls._calculate_category_score(reliability_findings)
        ai_score = cls._calculate_category_score(ai_findings)

        # 3. Maintainability from Metrics (Radon)
        maintainability_score = 100.0
        mi_metric = next((m for m in metrics if m.metric_name == "Maintainability Index"), None)
        if mi_metric:
            maintainability_score = mi_metric.metric_value

        # 4. Weighted Aggregate
        overall = (
            (security_score * cls.WEIGHTS["SECURITY"]) +
            (reliability_score * cls.WEIGHTS["RELIABILITY"]) +
            (maintainability_score * cls.WEIGHTS["MAINTAINABILITY"]) +
            (ai_score * cls.WEIGHTS["AI"])
        )

        return round(max(0.0, min(100.0, overall)), 2)

    @classmethod
    def _calculate_category_score(cls, findings: List[FindingDTO]) -> float:
        score = 100.0
        for f in findings:
            score -= cls.PENALTIES.get(f.severity, 0)
        return max(0.0, score)

    @staticmethod
    def get_grade(score: float) -> str:
        if score >= 97: return "A+"
        if score >= 93: return "A"
        if score >= 90: return "A-"
        if score >= 87: return "B+"
        if score >= 83: return "B"
        if score >= 80: return "B-"
        if score >= 77: return "C+"
        if score >= 73: return "C"
        if score >= 70: return "C-"
        if score >= 60: return "D"
        return "F"
