from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.security import get_current_user, get_db
from app.models.user import User
from app.services.aggregation.dashboard_service import DashboardService

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve aggregated dashboard statistics for the current user.
    """
    service = DashboardService(db)
    summary = service.get_user_summary(current_user.id)

    return {
        "success": True,
        "data": summary,
        "request_id": getattr(request.state, "request_id", "N/A")
    }
