import json
from pathlib import Path
from app.services.aggregation.dto import CanonicalReviewReport

class JSONExporter:
    @staticmethod
    def export(report: CanonicalReviewReport, output_path: Path) -> str:
        data = report.model_dump(mode='json')
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return str(output_path)
