from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.metric import Metric

class MetricRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_many(self, metrics: List[Metric]) -> List[Metric]:
        self.db.add_all(metrics)
        self.db.commit()
        return metrics

    def list_by_review(self, review_id: UUID) -> List[Metric]:
        return list(self.db.execute(
            select(Metric).where(Metric.review_id == review_id)
        ).scalars().all())
