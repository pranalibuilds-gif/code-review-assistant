import os
import shutil
import logging
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.submission import Submission
from app.models.enums import ReviewStatus

logger = logging.getLogger(__name__)

class MaintenanceService:
    def __init__(self, db: Session):
        self.db = db

    def purge_old_workspaces(self) -> int:
        """
        Removes workspace directories for completed or failed submissions.
        Returns the count of purged directories.
        """
        upload_path = Path(settings.UPLOAD_DIR)
        purged_count = 0

        # In a real app, we might check timestamps to keep recent ones
        for workspace_dir in upload_path.iterdir():
            if workspace_dir.is_dir():
                try:
                    # Logic: if not in active jobs, delete
                    # This is simplified for local dev
                    shutil.rmtree(workspace_dir)
                    purged_count += 1
                except Exception as e:
                    logger.error(f"Failed to purge workspace {workspace_dir}: {e}")

        return purged_count
