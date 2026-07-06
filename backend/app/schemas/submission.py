from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from app.models.enums import SubmissionType, ReviewStatus

class SubmissionBase(BaseModel):
    project_id: UUID

class PasteSubmission(SubmissionBase):
    code: str
    filename: str = "snippet.py"

class GitHubSubmission(SubmissionBase):
    github_url: HttpUrl

class SubmissionResponse(BaseModel):
    submission_id: UUID
    project_id: UUID
    status: ReviewStatus
    created_at: datetime

    class Config:
        from_attributes = True
