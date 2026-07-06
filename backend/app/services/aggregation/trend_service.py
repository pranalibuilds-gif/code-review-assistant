from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.review import Review
from app.models.submission import Submission
from .dto import TrendDTO, CanonicalReviewReport

class TrendService:
    @staticmethod
    def calculate_trend(db: Session, project_id: UUID, current_report: CanonicalReviewReport) -> TrendDTO:
        # Get the previous completed review for this project
        stmt = (
            select(Review)
            .join(Submission)
            .where(Submission.project_id == project_id)
            .where(Review.status.in_(["COMPLETED", "PARTIAL_SUCCESS"]))
            .where(Review.id != current_report.review_id)
            .order_by(desc(Review.finished_at))
            .limit(1)
        )

        previous_review = db.execute(stmt).scalar_one_or_none()

        if not previous_review or not previous_review.cached_report:
            return TrendDTO()

        prev_report = previous_review.cached_report

        return TrendDTO(
            score_delta=round(current_report.score - prev_report.get("score", 0), 2),
            findings_delta=current_report.statistics.total_findings - prev_report.get("statistics", {}).get("total_findings", 0),
            # Add complexity/maintainability deltas if needed
        )
