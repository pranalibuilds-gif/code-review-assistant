from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.submission import Submission

class SubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, submission_id: UUID) -> Optional[Submission]:
        return self.db.get(Submission, submission_id)

    def list_by_project(self, project_id: UUID, skip: int = 0, limit: int = 100) -> List[Submission]:
        return list(self.db.execute(
            select(Submission).where(Submission.project_id == project_id).offset(skip).limit(limit)
        ).scalars().all())

    def create(self, submission: Submission) -> Submission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def update(self, submission: Submission) -> Submission:
        self.db.commit()
        self.db.refresh(submission)
        return submission
