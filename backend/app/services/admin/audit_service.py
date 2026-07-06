from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.audit_log import AuditLog

class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        action: str,
        user_id: Optional[UUID] = None,
        target: Optional[str] = None,
        details: Optional[str] = None,
        request_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            target=target,
            details=details,
            request_id=request_id,
            ip_address=ip_address
        )
        self.db.add(log_entry)
        self.db.commit()
        return log_entry

    def list_logs(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        stmt = select(AuditLog).order_by(desc(AuditLog.created_at)).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())
