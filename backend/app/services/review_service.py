import logging
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Dict

from app.models.review import Review
from app.models.finding import Finding
from app.models.metric import Metric
from app.models.enums import ReviewStatus
from app.repositories.review_repository import ReviewRepository
from app.repositories.finding_repository import FindingRepository
from app.repositories.metric_repository import MetricRepository
from app.analyzers.schemas import NormalizedFinding, NormalizedMetric

logger = logging.getLogger(__name__)

class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.review_repo = ReviewRepository(db)
        self.finding_repo = FindingRepository(db)
        self.metric_repo = MetricRepository(db)

    def create_or_update_review(
        self,
        submission_id: UUID,
        status: ReviewStatus,
        findings: List[NormalizedFinding] = None,
        metrics: List[NormalizedMetric] = None,
        metadata: List[Dict] = None
    ) -> Review:
        review = self.review_repo.get_by_submission(submission_id)

        if not review:
            review = Review(
                submission_id=submission_id,
                status=status,
                started_at=datetime.now(timezone.utc)
            )
            review = self.review_repo.create(review)
        else:
            review.status = status

        if status in [ReviewStatus.COMPLETED, ReviewStatus.PARTIAL_SUCCESS, ReviewStatus.FAILED]:
            review.finished_at = datetime.now(timezone.utc)
            duration = (review.finished_at - review.started_at).total_seconds() * 1000
            review.duration_ms = int(duration)

        # Save findings
        if findings:
            db_findings = [
                Finding(
                    review_id=review.id,
                    source=f.source,
                    severity=f.severity,
                    category=f.category,
                    title=f.title,
                    description=f.description,
                    recommendation=f.recommendation,
                    file_path=f.file_path,
                    line=f.line,
                    rule_id=f.rule_id
                ) for f in findings
            ]
            self.finding_repo.create_many(db_findings)

        # Save metrics
        if metrics:
            db_metrics = [
                Metric(
                    review_id=review.id,
                    metric_name=m.metric_name,
                    metric_value=m.metric_value,
                    unit=m.unit
                ) for m in metrics
            ]
            self.metric_repo.create_many(db_metrics)

        # Update review score (Naive calculation for now)
        if status == ReviewStatus.COMPLETED:
            review.overall_score = self._calculate_score(findings, metrics)

        self.review_repo.update(review)
        return review

    def _calculate_score(self, findings: List[NormalizedFinding], metrics: List[NormalizedMetric]) -> float:
        # Placeholder scoring logic
        # 100 base score, deduct based on findings severity
        score = 100.0
        if not findings:
            return score

        deductions = {
            "CRITICAL": 20,
            "HIGH": 10,
            "MEDIUM": 5,
            "LOW": 2,
            "INFO": 0
        }

        total_deduction = 0
        for f in findings:
            total_deduction += deductions.get(f.severity.value, 0)

        return max(0.0, score - total_deduction)
