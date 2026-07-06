import os
from pathlib import Path
from typing import List, Dict

class FileDiscoveryService:
    IGNORE_DIRS = {
        ".git", ".github", "__pycache__", "node_modules", "dist", "build",
        ".venv", "venv", "env", ".idea", ".vscode", "coverage", "htmlcov",
        ".pytest_cache", ".mypy_cache", ".ruff_cache"
    }

    IGNORE_EXTENSIONS = {
        ".pyc", ".pyo", ".so", ".dll", ".exe", ".jpg", ".png", ".pdf",
        ".zip", ".tar", ".db", ".DS_Store"
    }

    @classmethod
    def discover_python_files(cls, root_path: str) -> List[str]:
        python_files = []
        for root, dirs, files in os.walk(root_path):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in cls.IGNORE_DIRS]

            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    python_files.append(os.path.relpath(full_path, root_path))

        return python_files

    @classmethod
    def get_stats(cls, root_path: str) -> Dict:
        python_files = cls.discover_python_files(root_path)
        total_size = sum(os.path.getsize(os.path.join(root_path, f)) for f in python_files)

        return {
            "total_files": len(python_files),
            "total_size_bytes": total_size,
            "python_files": python_files
        }
