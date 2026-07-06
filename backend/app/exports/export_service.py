import logging
from pathlib import Path
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.artifact import Artifact
from app.services.aggregation.aggregation_service import AggregationService
from app.core.config import settings
from .pdf_exporter import PDFExporter
from .markdown_exporter import MarkdownExporter
from .json_exporter import JSONExporter

logger = logging.getLogger(__name__)

class ExportService:
    def __init__(self, db: Session):
        self.db = db

    def generate_export(self, review_id: UUID, format: str) -> str:
        review = self.db.get(Review, review_id)
        if not review:
            raise ValueError("Review not found")

        if not review.cached_report:
            # Try to generate it if missing but analysis is complete
            if review.status in ["COMPLETED", "PARTIAL_SUCCESS"]:
                agg_service = AggregationService(self.db)
                report = agg_service.generate_report(review.id)
            else:
                raise ValueError("Report not ready for export")
        else:
            from app.services.aggregation.dto import CanonicalReviewReport
            report = CanonicalReviewReport.model_validate(review.cached_report)

        # Define workspace artifacts path
        workspace_path = Path(settings.UPLOAD_DIR) / str(review.submission_id)
        artifacts_dir = workspace_path / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        filename = f"review_{review.id}.{format}"
        output_path = artifacts_dir / filename

        # Generate the actual file
        if format == "pdf":
            PDFExporter.export(report, output_path)
        elif format == "md":
            MarkdownExporter.export(report, output_path)
        elif format == "json":
            JSONExporter.export(report, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")

        # Update Database Artifact
        self._record_artifact(review.id, format.upper(), str(output_path))

        return str(output_path)

    def _record_artifact(self, review_id: UUID, type: str, path: str):
        # Check if exists
        artifact = self.db.query(Artifact).filter(
            Artifact.review_id == review_id,
            Artifact.type == type
        ).first()

        if not artifact:
            artifact = Artifact(
                review_id=review_id,
                type=type,
                path=path
            )
            self.db.add(artifact)
        else:
            artifact.path = path

        self.db.commit()
