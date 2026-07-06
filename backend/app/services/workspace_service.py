import os
import shutil
import json
import uuid
from pathlib import Path
from app.core.config import settings

class WorkspaceService:
    @staticmethod
    def create_workspace(submission_id: uuid.UUID) -> str:
        workspace_path = Path(settings.UPLOAD_DIR) / str(submission_id)

        # Create directory structure
        (workspace_path / "src").mkdir(parents=True, exist_ok=True)
        (workspace_path / "analysis").mkdir(exist_ok=True)
        (workspace_path / "artifacts").mkdir(exist_ok=True)
        (workspace_path / "logs").mkdir(exist_ok=True)

        return str(workspace_path)

    @staticmethod
    def cleanup_workspace(workspace_path: str):
        if os.path.exists(workspace_path):
            shutil.rmtree(workspace_path)

    @staticmethod
    def write_manifest(workspace_path: str, manifest_data: dict):
        manifest_path = Path(workspace_path) / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest_data, f, indent=4)

    @staticmethod
    def get_src_path(workspace_path: str) -> str:
        return str(Path(workspace_path) / "src")
