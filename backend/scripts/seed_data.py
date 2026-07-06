import sys
from os.path import abspath, dirname

# Add project root to sys.path
sys.path.insert(0, abspath(dirname(dirname(__file__))))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.submission import Submission
from app.models.review import Review
from app.models.finding import Finding
from app.models.metric import Metric
from app.models.artifact import Artifact
from app.models.enums import SubmissionType, ReviewStatus, Severity, FindingSource
from app.repositories.user_repository import UserRepository
from app.services.aggregation.aggregation_service import AggregationService

def seed_data():
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        admin = repo.get_by_email("admin@codesage.local")
        if not admin:
            print("Admin user not found. Please run seed_admin.py first.")
            return

        # 1. Create Project
        project = Project(
            owner_id=admin.id,
            name="Sample Project",
            description="A project to test the domain model graph."
        )
        db.add(project)
        db.flush()
        print(f"Created project: {project.name}")

        # 2. Create Submission
        submission = Submission(
            project_id=project.id,
            submission_type=SubmissionType.GITHUB,
            github_url="https://github.com/example/repo",
            status=ReviewStatus.COMPLETED
        )
        db.add(submission)
        db.flush()
        print(f"Created submission for project: {project.name}")

        # 3. Create Review
        review = Review(
            submission_id=submission.id,
            overall_score=85.5,
            summary="Code quality is generally good, but some security issues were found.",
            status=ReviewStatus.COMPLETED
        )
        db.add(review)
        db.flush()
        print(f"Created review with score: {review.overall_score}")

        # 4. Create Finding
        finding = Finding(
            review_id=review.id,
            source=FindingSource.BANDIT,
            severity=Severity.HIGH,
            title="Hardcoded Secret",
            description="A hardcoded AWS secret key was found in settings.py",
            file_path="app/settings.py",
            line=42
        )
        db.add(finding)
        print(f"Created finding: {finding.title}")

        # 5. Create Metric
        metric = Metric(
            review_id=review.id,
            metric_name="Cyclomatic Complexity",
            metric_value=12.4,
            unit="avg"
        )
        db.add(metric)
        print(f"Created metric: {metric.metric_name}")

        db.commit()

        # Trigger Aggregation
        print("\nTriggering Report Aggregation...")
        agg_service = AggregationService(db)
        report = agg_service.generate_report(review.id)
        print(f"Aggregation complete. Final Score: {report.score}, Grade: {report.grade}")

        print("\nSeed data completed successfully. Object graph verified.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
