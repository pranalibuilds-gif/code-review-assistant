from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: UUID) -> Optional[Project]:
        return self.db.get(Project, project_id)

    def list_by_owner(self, owner_id: UUID, skip: int = 0, limit: int = 100) -> List[Project]:
        return list(self.db.execute(
            select(Project).where(Project.owner_id == owner_id).offset(skip).limit(limit)
        ).scalars().all())

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project: Project) -> Project:
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()
