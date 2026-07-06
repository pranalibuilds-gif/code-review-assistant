from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.security import get_current_active_admin, get_db
from app.services.admin.health_service import SystemHealthService
from app.services.admin.job_service import JobService
from app.services.admin.audit_service import AuditService
from app.services.admin.maintenance_service import MaintenanceService

router = APIRouter()

@router.get("/health")
async def get_system_health(
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    service = SystemHealthService(db)
    return await service.get_full_health()

@router.get("/jobs")
def get_jobs(
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    service = JobService(db)
    return {
        "jobs": service.list_active_jobs(),
        "stats": service.get_job_stats()
    }

@router.get("/audit")
def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    service = AuditService(db)
    return service.list_logs(skip, limit)

@router.post("/maintenance/cleanup")
def run_cleanup(
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    service = MaintenanceService(db)
    purged = service.purge_old_workspaces()
    return {"message": f"Cleanup complete. Purged {purged} workspaces."}
