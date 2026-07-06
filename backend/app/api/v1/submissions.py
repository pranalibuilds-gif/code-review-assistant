from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, Form
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.security import get_current_user, get_db
from app.models.user import User
from app.schemas.submission import SubmissionResponse, PasteSubmission, GitHubSubmission
from app.services.submission_service import SubmissionService

router = APIRouter()

@router.post("/paste", response_model=SubmissionResponse)
def submit_paste(
    data: PasteSubmission,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit raw code for analysis.
    """
    service = SubmissionService(db)
    return service.process_paste(data.project_id, data.code, data.filename, background_tasks)

@router.post("/upload", response_model=SubmissionResponse)
def submit_upload(
    project_id: UUID = Form(...),
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a ZIP file for analysis.
    """
    service = SubmissionService(db)
    return service.process_upload(project_id, file, background_tasks)

@router.post("/github", response_model=SubmissionResponse)
def submit_github(
    data: GitHubSubmission,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a GitHub repository URL for analysis.
    """
    service = SubmissionService(db)
    return service.process_github(data.project_id, str(data.github_url), background_tasks)
