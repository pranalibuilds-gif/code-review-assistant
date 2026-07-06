import zipfile
import os
from pathlib import Path
from fastapi import HTTPException

class ArchiveService:
    @staticmethod
    def extract_zip(zip_path: str, extract_to: str):
        if not zipfile.is_zipfile(zip_path):
            raise HTTPException(status_code=400, detail="Invalid ZIP archive")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Protection against Zip Slip (Path Traversal)
            for member in zip_ref.namelist():
                member_path = os.path.join(extract_to, member)
                if not os.path.abspath(member_path).startswith(os.path.abspath(extract_to)):
                    raise HTTPException(status_code=400, detail="Detected potential path traversal in ZIP")

            zip_ref.extractall(extract_to)

    @staticmethod
    def cleanup(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
