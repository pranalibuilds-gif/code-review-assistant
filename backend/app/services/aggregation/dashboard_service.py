from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc
from uuid import UUID
from app.models.review import Review
from app.models.submission import Submission
from app.models.project import Project

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_summary(self, user_id: UUID) -> Dict[str, Any]:
        # Get all reviews for user's projects
        stmt = (
            select(Review)
            .join(Submission)
            .join(Project)
            .where(Project.owner_id == user_id)
            .where(Review.status.in_(["COMPLETED", "PARTIAL_SUCCESS"]))
            .order_by(desc(Review.finished_at))
        )

        reviews = self.db.execute(stmt).scalars().all()

        if not reviews:
            return {
                "total_reviews": 0,
                "average_score": 0,
                "recent_reviews": []
            }

        valid_reviews = [r for r in reviews if r.overall_score is not None]
        avg_score = round(sum(r.overall_score for r in valid_reviews) / len(valid_reviews), 1) if valid_reviews else 0

        # Calculate Severity Distribution from cached reports
        severity_totals = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for r in reviews:
            if r.cached_report:
                stats = r.cached_report.get("statistics", {})
                severity_totals["CRITICAL"] += stats.get("critical_count", 0)
                severity_totals["HIGH"] += stats.get("high_count", 0)
                severity_totals["MEDIUM"] += stats.get("medium_count", 0)
                severity_totals["LOW"] += stats.get("low_count", 0)

        return {
            "total_reviews": len(reviews),
            "average_score": avg_score,
            "recent_reviews": [r.cached_report for r in reviews[:5] if r.cached_report],
            "severity_distribution": severity_totals
        }
