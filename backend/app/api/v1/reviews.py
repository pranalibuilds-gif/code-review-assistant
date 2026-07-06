from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.security import get_current_user, get_db
from app.models.user import User
from app.models.review import Review
from app.schemas.report import ReviewDetailedResponse

router = APIRouter()

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
