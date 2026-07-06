import sys
import uuid
import random
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

# Add backend to sys.path
root = Path(__file__).parent.parent.parent
backend_path = root / "backend"
sys.path.insert(0, str(backend_path))

# Load .env from backend
load_dotenv(backend_path / ".env")

from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.submission import Submission
from app.models.review import Review
from app.models.finding import Finding
from app.models.metric import Metric
from app.models.artifact import Artifact
from app.models.enums import SubmissionType, ReviewStatus, Severity, FindingSource
from app.services.password_service import PasswordService
from app.services.aggregation.scoring_service import ScoringService

def seed_v1():
    db = SessionLocal()
    try:
        # 1. Create or get admin
        admin = db.query(User).filter(User.email == "admin@codesage.local").first()
        if not admin:
            admin = User(
                email="admin@codesage.local",
                username="admin",
                full_name="System Administrator",
                password_hash=PasswordService.hash_password("admin_password_123"),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
            db.flush()

        # 2. Generate 20+ Projects
        project_names = [
            "SmartERP Backend", "Inventory API", "Auth Microservice", "Data Scraper",
            "ML Preprocessor", "Logging Utility", "Config Manager", "Task Scheduler",
            "Payment Gateway", "File Storage Service", "Notification Engine",
            "User Analytics", "Search Optimizer", "Image Processor", "PDF Generator",
            "Validation Lib", "Mock API Server", "Cache Wrapper", "DB Migrator", "CLI Tool"
        ]

        projects = []
        for name in project_names:
            p = Project(
                owner_id=admin.id,
                name=name,
                description=f"A professional Python project focusing on {name.lower()}."
            )
            db.add(p)
            projects.append(p)
        db.flush()

        # 3. Generate 150+ Reviews
        print(f"Seeding {len(projects)} projects and 150+ reviews...")

        review_count = 0
        current_time = datetime.now(timezone.utc)

        for project in projects:
            # Each project has between 5 and 12 reviews over the last 3 months
            num_reviews = random.randint(5, 12)

            for i in range(num_reviews):
                review_date = current_time - timedelta(days=random.randint(0, 90))

                # Create Submission
                sub = Submission(
                    project_id=project.id,
                    submission_type=random.choice(list(SubmissionType)),
                    status=ReviewStatus.COMPLETED,
                    created_at=review_date,
                    completed_at=review_date + timedelta(minutes=random.randint(1, 5))
                )
                db.add(sub)
                db.flush()

                # Create Review
                score = random.uniform(65, 98)
                grade = ScoringService.get_grade(score)

                rev = Review(
                    submission_id=sub.id,
                    overall_score=score,
                    status=ReviewStatus.COMPLETED,
                    started_at=review_date,
                    finished_at=sub.completed_at,
                    duration_ms=random.randint(2000, 30000),
                    summary="Incremental quality assessment.",
                    ai_summary="AI Mentor recommends consistent type hinting and service separation."
                )
                db.add(rev)
                db.flush()

                # Create Findings
                num_findings = random.randint(3, 15)
                for _ in range(num_findings):
                    f = Finding(
                        review_id=rev.id,
                        source=random.choice(list(FindingSource)),
                        severity=random.choice(list(Severity)),
                        title=f"Sample {random.choice(['Security', 'Quality', 'Logic'])} Issue",
                        description="This is a generated issue for demo purposes.",
                        file_path="app/core/logic.py",
                        line=random.randint(1, 200)
                    )
                    db.add(f)

                # Create Metrics
                db.add(Metric(review_id=rev.id, metric_name="Maintainability Index", metric_value=random.uniform(70, 95)))
                db.add(Metric(review_id=rev.id, metric_name="Cyclomatic Complexity", metric_value=random.uniform(2, 15)))

                review_count += 1

        db.commit()
        print(f"Successfully seeded {review_count} reviews across {len(projects)} projects.")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_v1()
