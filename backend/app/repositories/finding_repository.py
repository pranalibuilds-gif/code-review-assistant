from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.finding import Finding

class FindingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_many(self, findings: List[Finding]) -> List[Finding]:
        self.db.add_all(findings)
        self.db.commit()
        return findings

    def list_by_review(self, review_id: UUID) -> List[Finding]:
        return list(self.db.execute(
            select(Finding).where(Finding.review_id == review_id)
        ).scalars().all())
