from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, Form
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.security import get_current_user, get_db
from app.models.user import User
from app.schemas.submission import SubmissionResponse, PasteSubmission, GitHubSubmission
from app.services.submission_service import SubmissionService

router = APIRouter()

@router.post("/paste")
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
    result = service.process_paste(data.project_id, data.code, data.filename, background_tasks)
    return {"success": True, "data": result}

@router.post("/upload")
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
    result = service.process_upload(project_id, file, background_tasks)
    return {"success": True, "data": result}

@router.post("/github")
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
    result = service.process_github(data.project_id, str(data.github_url), background_tasks)
    return {"success": True, "data": result}

@router.get("/status/{submission_id}")
def get_status(
    submission_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the status of a submission.
    """
    service = SubmissionService(db)
    submission = service.repo.get_by_id(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Simple check if project belongs to user
    if submission.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # If completed, find the review_id
    review_id = None
    if submission.review:
        review_id = submission.review.id

    return {
        "success": True,
        "data": {
            "id": submission.id,
            "status": submission.status,
            "project_id": submission.project_id,
            "review_id": review_id
        }
    }
