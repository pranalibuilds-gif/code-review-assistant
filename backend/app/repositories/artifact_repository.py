from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.artifact import Artifact

class ArtifactRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, artifact: Artifact) -> Artifact:
        self.db.add(artifact)
        self.db.commit()
        self.db.refresh(artifact)
        return artifact

    def list_by_review(self, review_id: UUID) -> List[Artifact]:
        return list(self.db.execute(
            select(Artifact).where(Artifact.review_id == review_id)
        ).scalars().all())
