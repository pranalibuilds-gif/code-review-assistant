from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.submission import Submission
from app.models.enums import ReviewStatus

class JobService:
    def __init__(self, db: Session):
        self.db = db

    def list_active_jobs(self) -> List[Dict[str, Any]]:
        """
        List all jobs that are currently being processed.
        """
        stmt = (
            select(Submission)
            .where(Submission.status.notin_([ReviewStatus.COMPLETED, ReviewStatus.FAILED, ReviewStatus.PARTIAL_SUCCESS]))
            .order_by(desc(Submission.created_at))
        )
        submissions = self.db.execute(stmt).scalars().all()

        return [
            {
                "submission_id": s.id,
                "project_id": s.project_id,
                "type": s.submission_type,
                "status": s.status,
                "created_at": s.created_at
            } for s in submissions
        ]

    def get_job_stats(self) -> Dict[str, Any]:
        """
        Provides a summary of job processing performance.
        """
        total = self.db.query(Submission).count()
        failed = self.db.query(Submission).filter(Submission.status == ReviewStatus.FAILED).count()
        completed = self.db.query(Submission).filter(Submission.status == ReviewStatus.COMPLETED).count()

        return {
            "total_jobs": total,
            "completed": completed,
            "failed": failed,
            "success_rate": round((completed / total * 100), 1) if total > 0 else 100
        }
