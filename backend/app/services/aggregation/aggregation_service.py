import json
import logging
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.submission import Submission
from app.models.finding import Finding
from app.models.metric import Metric
from .dto import CanonicalReviewReport, FindingDTO, MetricDTO, StatisticsDTO, TrendDTO
from .scoring_service import ScoringService
from .trend_service import TrendService

logger = logging.getLogger(__name__)

class AggregationService:
    def __init__(self, db: Session):
        self.db = db

    def generate_report(self, review_id: str) -> CanonicalReviewReport:
        review = self.db.get(Review, review_id)
        if not review:
            raise ValueError("Review not found")

        submission = self.db.get(Submission, review.submission_id)

        # 1. Fetch Findings and Metrics
        db_findings = review.findings
        db_metrics = review.metrics

        findings = [FindingDTO.model_validate(f, from_attributes=True) for f in db_findings]
        metrics = [MetricDTO.model_validate(m, from_attributes=True) for m in db_metrics]

        # 2. Calculate Statistics
        stats = self._calculate_statistics(findings, metrics, review)

        # 3. Calculate Score and Grade
        score = ScoringService.calculate_overall_score(findings, metrics)
        grade = ScoringService.get_grade(score)

        # 4. Parse Recommendations
        recommendations = []
        if review.recommendations:
            try:
                recommendations = json.loads(review.recommendations)
            except:
                pass

        # 5. Build Preliminary Report
        report = CanonicalReviewReport(
            review_id=review.id,
            submission_id=submission.id,
            project_id=submission.project_id,
            score=score,
            grade=grade,
            status=review.status,
            summary=review.summary,
            ai_summary=review.ai_summary,
            recommendations=recommendations,
            findings=findings,
            metrics=metrics,
            statistics=stats,
            trend=TrendDTO(), # Default empty
            created_at=review.started_at,
            finished_at=review.finished_at
        )

        # 6. Calculate Trends
        report.trend = TrendService.calculate_trend(self.db, submission.project_id, current_report=report)

        # 7. Cache the report
        review.cached_report = report.model_dump(mode='json')
        review.overall_score = score
        self.db.commit()

        return report

    def _calculate_statistics(self, findings: List[FindingDTO], metrics: List[MetricDTO], review: Review) -> StatisticsDTO:
        stats = StatisticsDTO(
            total_findings=len(findings),
            critical_count=len([f for f in findings if f.severity == "CRITICAL"]),
            high_count=len([f for f in findings if f.severity == "HIGH"]),
            medium_count=len([f for f in findings if f.severity == "MEDIUM"]),
            low_count=len([f for f in findings if f.severity == "LOW"]),
            security_count=len([f for f in findings if f.source == "BANDIT"]),
            quality_count=len([f for f in findings if f.source == "PYLINT"]),
            complexity_count=len([f for f in findings if f.source == "RADON"]),
            duration_ms=review.duration_ms or 0
        )
        return stats
