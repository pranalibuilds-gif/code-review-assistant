import git
import os
import shutil
from fastapi import HTTPException

class GitHubService:
    @staticmethod
    def clone_repository(repo_url: str, dest_path: str):
        try:
            # Clone with depth 1 to save time/space
            git.Repo.clone_from(repo_url, dest_path, depth=1)
        except git.GitCommandError as e:
            if "not found" in str(e).lower():
                raise HTTPException(status_code=404, detail="GitHub repository not found or private")
            raise HTTPException(status_code=400, detail=f"Failed to clone repository: {str(e)}")

    @staticmethod
    def validate_url(url: str):
        if not url.startswith("https://github.com/"):
            raise HTTPException(status_code=400, detail="Only public GitHub repositories are supported")
