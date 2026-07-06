from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository

class ProjectService:
    def __init__(self, db: Session):
        self.repo = ProjectRepository(db)

    def create_project(self, owner_id: UUID, name: str, description: Optional[str] = None) -> Project:
        project = Project(
            owner_id=owner_id,
            name=name,
            description=description
        )
        return self.repo.create(project)

    def get_project(self, project_id: UUID) -> Optional[Project]:
        return self.repo.get_by_id(project_id)

    def list_user_projects(self, owner_id: UUID) -> List[Project]:
        return self.repo.list_by_owner(owner_id)
