import uuid
import logging
from datetime import datetime, timezone
from fastapi import BackgroundTasks, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path

from app.models.submission import Submission
from app.models.enums import SubmissionType, ReviewStatus
from app.repositories.submission_repository import SubmissionRepository
from app.services.workspace_service import WorkspaceService
from app.services.file_discovery_service import FileDiscoveryService
from app.services.archive_service import ArchiveService
from app.services.github_service import GitHubService

logger = logging.getLogger(__name__)

class SubmissionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SubmissionRepository(db)

    def process_paste(self, project_id: uuid.UUID, code: str, filename: str, background_tasks: BackgroundTasks):
        submission = self._create_initial_submission(project_id, SubmissionType.PASTE)

        workspace_path = WorkspaceService.create_workspace(submission.id)
        src_path = WorkspaceService.get_src_path(workspace_path)

        with open(Path(src_path) / filename, "w") as f:
            f.write(code)

        background_tasks.add_task(self._run_analysis_pipeline, submission.id, workspace_path)
        return submission

    def process_upload(self, project_id: uuid.UUID, file: UploadFile, background_tasks: BackgroundTasks):
        submission = self._create_initial_submission(project_id, SubmissionType.UPLOAD)

        workspace_path = WorkspaceService.create_workspace(submission.id)
        temp_zip = Path(workspace_path) / file.filename

        with open(temp_zip, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        src_path = WorkspaceService.get_src_path(workspace_path)

        try:
            ArchiveService.extract_zip(str(temp_zip), src_path)
            ArchiveService.cleanup(str(temp_zip))
        except Exception as e:
            WorkspaceService.cleanup_workspace(workspace_path)
            self._update_status(submission.id, ReviewStatus.FAILED)
            raise e

        background_tasks.add_task(self._run_analysis_pipeline, submission.id, workspace_path)
        return submission

    def process_github(self, project_id: uuid.UUID, github_url: str, background_tasks: BackgroundTasks):
        GitHubService.validate_url(github_url)
        submission = self._create_initial_submission(project_id, SubmissionType.GITHUB)

        workspace_path = WorkspaceService.create_workspace(submission.id)
        src_path = WorkspaceService.get_src_path(workspace_path)

        try:
            GitHubService.clone_repository(github_url, src_path)
        except Exception as e:
            WorkspaceService.cleanup_workspace(workspace_path)
            self._update_status(submission.id, ReviewStatus.FAILED)
            raise e

        background_tasks.add_task(self._run_analysis_pipeline, submission.id, workspace_path)
        return submission

    def _create_initial_submission(self, project_id: uuid.UUID, sub_type: SubmissionType):
        submission = Submission(
            project_id=project_id,
            submission_type=sub_type,
            status=ReviewStatus.QUEUED
        )
        return self.repo.create(submission)

    def _update_status(self, submission_id: uuid.UUID, status: ReviewStatus):
        submission = self.repo.get_by_id(submission_id)
        if submission:
            submission.status = status
            if status in [ReviewStatus.COMPLETED, ReviewStatus.FAILED]:
                submission.completed_at = datetime.now(timezone.utc)
            self.db.commit()

    async def _run_analysis_pipeline(self, submission_id: uuid.UUID, workspace_path: str):
        try:
            # 1. Validation & Discovery
            self._update_status(submission_id, ReviewStatus.DISCOVERING_FILES)
            src_path = WorkspaceService.get_src_path(workspace_path)
            stats = FileDiscoveryService.get_stats(src_path)

            if stats["total_files"] == 0:
                logger.error(f"No Python files found in submission {submission_id}")
                self._update_status(submission_id, ReviewStatus.FAILED)
                # Should we cleanup here? Maybe keep for debugging if failed.
                return

            # 2. Manifest Generation
            self._update_status(submission_id, ReviewStatus.PREPARING_WORKSPACE)
            submission = self.repo.get_by_id(submission_id)
            manifest = {
                "submission_id": str(submission_id),
                "project_id": str(submission.project_id),
                "type": submission.submission_type.value,
                "stats": stats,
                "created_at": str(submission.created_at)
            }
            WorkspaceService.write_manifest(workspace_path, manifest)

            # 3. Ready for Analysis (Future phases take over here)
            self._update_status(submission_id, ReviewStatus.READY_FOR_ANALYSIS)
            logger.info(f"Submission {submission_id} is ready for analysis.")

        except Exception as e:
            logger.error(f"Pipeline failed for submission {submission_id}: {str(e)}")
            self._update_status(submission_id, ReviewStatus.FAILED)
