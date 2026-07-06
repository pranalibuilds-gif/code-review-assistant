import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base
from .enums import SubmissionType, ReviewStatus

if TYPE_CHECKING:
    from .project import Project
    from .review import Review

class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )

    submission_type: Mapped[SubmissionType] = mapped_column(
        SQLEnum(SubmissionType), nullable=False
    )
    status: Mapped[ReviewStatus] = mapped_column(
        SQLEnum(ReviewStatus), default=ReviewStatus.QUEUED, nullable=False
    )

    github_url: Mapped[str] = mapped_column(String(500), nullable=True)
    uploaded_filename: Mapped[str] = mapped_column(String(255), nullable=True)
    root_directory: Mapped[str] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="submissions")
    review: Mapped[Optional["Review"]] = relationship(
        "Review", back_populates="submission", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Submission {self.id} ({self.submission_type})>"
