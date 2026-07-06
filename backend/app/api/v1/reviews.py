from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID
import os

from app.core.security import get_current_user, get_db
from app.models.user import User
from app.models.review import Review
from app.schemas.report import ReviewDetailedResponse
from app.exports.export_service import ExportService

router = APIRouter()

@router.get("")
def list_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all reviews belonging to the current user's projects.
    """
    from app.models.submission import Submission
    from app.models.project import Project
    from sqlalchemy import select, desc

    stmt = (
        select(Review)
        .join(Submission)
        .join(Project)
        .where(Project.owner_id == current_user.id)
        .where(Review.status.in_(["COMPLETED", "PARTIAL_SUCCESS"]))
        .order_by(desc(Review.finished_at))
    )

    reviews = db.execute(stmt).scalars().all()

    return {
        "success": True,
        "data": [r.cached_report for r in reviews if r.cached_report]
    }

@router.get("/{review_id}", response_model=ReviewDetailedResponse)
def get_review_report(
    review_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve the canonical report for a specific review.
    Uses the cached version if available.
    """
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Check ownership (Simple project-based check)
    if review.submission.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this review")

    if not review.cached_report:
        raise HTTPException(status_code=400, detail="Report not yet generated or analysis failed")

    return {
        "success": True,
        "data": review.cached_report,
        "request_id": getattr(request.state, "request_id", "N/A")
    }

@router.get("/{review_id}/export/{format}")
def export_review(
    review_id: UUID,
    format: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate and download a review report in the specified format (pdf, md, json).
    """
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.submission.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = ExportService(db)
    try:
        file_path = service.generate_export(review_id, format.lower())

        # Determine media type
        media_types = {
            "pdf": "application/pdf",
            "md": "text/markdown",
            "json": "application/json"
        }

        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type=media_types.get(format.lower(), "application/octet-stream")
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
