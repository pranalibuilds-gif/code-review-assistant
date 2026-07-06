import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
DEMO = ROOT / "demo"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(DEMO))
load_dotenv(BACKEND / ".env")

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.audit_log import AuditLog
from app.models.artifact import Artifact
from app.models.finding import Finding
from app.models.metric import Metric
from app.models.project import Project
from app.models.review import Review
from app.models.submission import Submission
from app.models.user import User, UserRole
from app.models.enums import SubmissionType, ReviewStatus, Severity, FindingSource
from app.services.password_service import PasswordService
from app.services.aggregation.scoring_service import ScoringService

from sample_data.profiles import get_profile
from sample_data.generators.users import seed_users
from sample_data.generators.projects import seed_projects
from sample_data.generators.reviews import seed_reviews
from sample_data.generators.audit_logs import seed_audit_logs


class DemoDataGenerator:
    def __init__(self, profile_name: str = "enterprise"):
        self.profile = get_profile(profile_name)
        random.seed(self.profile.get("seed", 42))

    def run(self, reset: bool = False) -> None:
        db = SessionLocal()
        try:
            print(f"Seeding demo dataset: {self.profile['display_name']}")
            if reset:
                self._clear_database(db)

            users = seed_users(db, self.profile)
            projects = seed_projects(db, self.profile, users)
            seed_reviews(db, self.profile, users, projects)
            seed_audit_logs(db, self.profile, users, projects)

            db.commit()
            self._print_credentials(users)
            print("Demo seeding complete.")
        except Exception as exc:
            db.rollback()
            raise
        finally:
            db.close()

    def _clear_database(self, db: Session) -> None:
        print("Clearing existing demo data...")
        db.execute(delete(AuditLog))
        db.execute(delete(Artifact))
        db.execute(delete(Finding))
        db.execute(delete(Metric))
        db.execute(delete(Review))
        db.execute(delete(Submission))
        db.execute(delete(Project))
        db.execute(delete(User))
        db.commit()

    def _print_credentials(self, users: dict[str, Any]) -> None:
        print("\nSeeded accounts:")
        print("  Admin:")
        print(f"    email: {users['admin'].email}")
        print(f"    password: {users['admin_password']}")
        print("  Demo user:")
        print(f"    email: {users['demo_user'].email}")
        print(f"    password: {users['demo_user_password']}")


if __name__ == "__main__":
    generator = DemoDataGenerator()
    generator.run(reset=True)
