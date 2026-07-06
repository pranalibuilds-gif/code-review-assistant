import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base
from .enums import Severity, FindingSource

if TYPE_CHECKING:
    from .review import Review

class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False
    )

    source: Mapped[FindingSource] = mapped_column(SQLEnum(FindingSource), nullable=False)
    severity: Mapped[Severity] = mapped_column(SQLEnum(Severity), nullable=False)

    category: Mapped[str] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    recommendation: Mapped[str] = mapped_column(Text, nullable=True)

    file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    line: Mapped[int] = mapped_column(Integer, nullable=True)
    rule_id: Mapped[str] = mapped_column(String(100), nullable=True)

    # Relationships
    review: Mapped["Review"] = relationship("Review", back_populates="findings")

    def __repr__(self) -> str:
        return f"<Finding {self.title} ({self.severity})>"
