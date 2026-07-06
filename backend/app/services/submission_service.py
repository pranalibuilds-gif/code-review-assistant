from uuid import UUID
from sqlalchemy.orm import Session
from app.models.submission import Submission
from app.models.enums import SubmissionType, ReviewStatus
from app.repositories.submission_repository import SubmissionRepository

class SubmissionService:
    def __init__(self, db: Session):
        self.repo = SubmissionRepository(db)

    def create_submission(
        self,
        project_id: UUID,
        submission_type: SubmissionType,
        github_url: str = None,
        uploaded_filename: str = None
    ) -> Submission:
        submission = Submission(
            project_id=project_id,
            submission_type=submission_type,
            status=ReviewStatus.QUEUED,
            github_url=github_url,
            uploaded_filename=uploaded_filename
        )
        return self.repo.create(submission)

    def update_status(self, submission_id: UUID, status: ReviewStatus) -> Submission:
        submission = self.repo.get_by_id(submission_id)
        if submission:
            submission.status = status
            if status == ReviewStatus.COMPLETED or status == ReviewStatus.FAILED:
                import datetime
                submission.completed_at = datetime.datetime.utcnow()
            return self.repo.update(submission)
        return None
