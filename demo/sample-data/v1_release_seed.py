import sys
import uuid
import random
import os
import json
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
from app.models.audit_log import AuditLog
from app.models.enums import SubmissionType, ReviewStatus, Severity, FindingSource
from app.services.password_service import PasswordService
from app.services.aggregation.scoring_service import ScoringService
from app.services.aggregation.dto import CanonicalReviewReport, StatisticsDTO, TrendDTO, FindingDTO, MetricDTO

def seed_v1():
    # Set seed for deterministic generation
    random.seed(42)

    db = SessionLocal()
    try:
        print("--- Starting Deterministic V1 Release Seeding ---")

        # 1. Create Diverse Users
        user_configs = [
            ("admin@codesage.local", "admin", "System Administrator", UserRole.ADMIN),
            ("pranali@codesage.local", "pranalimore", "Pranali More", UserRole.USER),
            ("alex@codesage.local", "ajohnson", "Alex Johnson", UserRole.USER),
            ("sarah@codesage.local", "sarahc", "Sarah Chen", UserRole.USER),
            ("omar@codesage.local", "ohassan", "Omar Hassan", UserRole.USER),
            ("emily@codesage.local", "emilyr", "Emily Rodriguez", UserRole.USER),
            ("david@codesage.local", "dkim", "David Kim", UserRole.USER),
        ]

        users = []
        for email, username, name, role in user_configs:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    email=email,
                    username=username,
                    full_name=name,
                    password_hash=PasswordService.hash_password("password123"),
                    role=role,
                    is_active=True,
                    is_verified=True
                )
                db.add(user)
                db.flush()
            users.append(user)

        # 2. Define Realistic Projects
        project_names = [
            "SmartERP", "Vita", "CodeSage", "InventoryHub", "ShopFlow API",
            "TaskPilot", "Finance Tracker", "DevBoard", "Learning Portal",
            "Library Manager", "HR Suite", "HealthSync", "Campus Connect",
            "Analytics Engine", "Payment Gateway", "Weather Dashboard",
            "Image Processor", "Blog Platform", "Chat Server", "Portfolio Website",
            "Auth Service", "Notification Engine", "Search Optimizer"
        ]

        projects = []
        for i, name in enumerate(project_names):
            owner = random.choice(users)
            p = db.query(Project).filter(Project.name == name, Project.owner_id == owner.id).first()
            if not p:
                p = Project(
                    owner_id=owner.id,
                    name=name,
                    description=f"Core engineering project focusing on {name.lower()} architecture.",
                    created_at=datetime.now(timezone.utc) - timedelta(days=180)
                )
                db.add(p)
                db.flush()
            projects.append(p)

        # 3. Time-Series Generation (Jan to June)
        start_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
        current_time = datetime(2026, 6, 30, tzinfo=timezone.utc)

        print(f"Generating 200+ reviews across {len(projects)} projects over 6 months...")

        ai_recommendations_pool = [
            "Reduce function complexity by extracting inner logic to private methods.",
            "Add type hints to improve IDE support and code clarity.",
            "Split oversized modules into cohesive service-oriented components.",
            "Replace duplicated logic with a shared utility function.",
            "Validate all external inputs before processing to prevent injection attacks.",
            "Improve exception handling by using specific exception types.",
            "Increase unit test coverage for edge cases in business logic.",
            "Introduce dependency injection to improve module testability.",
            "Simplify nested conditionals into guard clauses.",
            "Rename ambiguous variables like 'data' or 'x' to communicate intent.",
            "Replace magic numbers with named constants.",
            "Remove dead code and unused imports.",
            "Improve logging around external service calls for better observability.",
            "Use context managers consistently for resource handling (files, db)."
        ]

        total_reviews = 0
        total_findings = 0

        for project in projects:
            num_reviews = random.randint(6, 12)

            # Base quality level for this project (starts low, usually improves)
            base_quality = random.uniform(55, 80)

            for r_idx in range(num_reviews):
                # Distribute reviews over the 6 months
                review_days_offset = (180 // num_reviews) * r_idx + random.randint(0, 10)
                review_date = start_date + timedelta(days=review_days_offset)

                # Non-monotonic score evolution
                # Usually improves (+1 to +6), but 20% chance of regression (-2 to -8)
                if random.random() > 0.8 and r_idx > 0:
                    base_quality -= random.uniform(2, 8)
                else:
                    base_quality += random.uniform(1, 6)

                final_score = max(0, min(98, base_quality))

                # Determine status
                rand_status = random.random()
                if rand_status > 0.98:
                    status = ReviewStatus.FAILED
                elif rand_status > 0.91:
                    status = ReviewStatus.PARTIAL_SUCCESS
                else:
                    status = ReviewStatus.COMPLETED

                # Create Submission
                sub = Submission(
                    project_id=project.id,
                    submission_type=random.choice(list(SubmissionType)),
                    status=status,
                    created_at=review_date,
                    completed_at=review_date + timedelta(minutes=random.randint(1, 10))
                )
                db.add(sub)
                db.flush()

                # Create Review
                rev = Review(
                    submission_id=sub.id,
                    overall_score=final_score if status != ReviewStatus.FAILED else 0,
                    status=status,
                    started_at=review_date,
                    finished_at=sub.completed_at,
                    duration_ms=random.randint(5000, 45000),
                    summary=f"Analysis of {project.name} iteration {r_idx + 1}.",
                    ai_summary="High-level assessment suggests maintaining modularity and improving documentation." if status != ReviewStatus.FAILED else "Review aborted due to system failure."
                )

                # Add recommendations
                recs = []
                for _ in range(random.randint(2, 4)):
                    recs.append({
                        "title": "Mentor Tip",
                        "description": random.choice(ai_recommendations_pool),
                        "impact": random.choice(["High", "Medium", "Low"])
                    })
                rev.recommendations = json.dumps(recs)

                db.add(rev)
                db.flush()

                # Create Findings (if not failed)
                findings_dto = []
                if status != ReviewStatus.FAILED:
                    num_findings = int((100 - final_score) * random.uniform(0.5, 1.5))
                    for _ in range(num_findings):
                        sev_roll = random.random()
                        if sev_roll > 0.95: sev = Severity.CRITICAL
                        elif sev_roll > 0.80: sev = Severity.HIGH
                        elif sev_roll > 0.55: sev = Severity.MEDIUM
                        else: sev = Severity.LOW

                        f_source = random.choice(list(FindingSource))
                        f = Finding(
                            review_id=rev.id,
                            source=f_source,
                            severity=sev,
                            category=random.choice(["Security", "Complexity", "Style", "Logic", "Doc"]),
                            title=f"Potential {sev.value} Issue found by {f_source.value}",
                            description="Automatic detection of pattern violation or risk area.",
                            recommendation="Consider refactoring this section to follow best practices.",
                            file_path=f"app/{random.choice(['core', 'api', 'db', 'services'])}/module_{random.randint(1, 5)}.py",
                            line=random.randint(10, 500)
                        )
                        db.add(f)
                        findings_dto.append(FindingDTO.model_validate(f, from_attributes=True))
                        total_findings += 1

                # Create Metrics
                metrics_dto = []
                if status != ReviewStatus.FAILED:
                    m1 = Metric(review_id=rev.id, metric_name="Maintainability Index", metric_value=max(20, min(100, final_score + random.uniform(-5, 5))))
                    m2 = Metric(review_id=rev.id, metric_name="Average Cyclomatic Complexity", metric_value=random.uniform(2, 18))
                    db.add(m1)
                    db.add(m2)
                    metrics_dto.append(MetricDTO.model_validate(m1, from_attributes=True))
                    metrics_dto.append(MetricDTO.model_validate(m2, from_attributes=True))

                # Create Artifacts (PDF/MD/JSON)
                if status == ReviewStatus.COMPLETED:
                    for fmt in ["PDF", "MD", "JSON"]:
                        if random.random() > 0.3: # 70% chance an artifact was generated
                            art = Artifact(
                                review_id=rev.id,
                                type=fmt,
                                path=f"uploads/{sub.id}/artifacts/review_{rev.id}.{fmt.lower()}"
                            )
                            db.add(art)

                # Generate Cached Report Snapshot
                if status != ReviewStatus.FAILED:
                    stats = StatisticsDTO(
                        total_findings=len(findings_dto),
                        critical_count=len([f for f in findings_dto if f.severity == Severity.CRITICAL]),
                        high_count=len([f for f in findings_dto if f.severity == Severity.HIGH]),
                        medium_count=len([f for f in findings_dto if f.severity == Severity.MEDIUM]),
                        low_count=len([f for f in findings_dto if f.severity == Severity.LOW]),
                        security_count=len([f for f in findings_dto if f.source == FindingSource.BANDIT]),
                        quality_count=len([f for f in findings_dto if f.source == FindingSource.PYLINT]),
                        complexity_count=len([f for f in findings_dto if f.source == FindingSource.RADON]),
                        files_analyzed=random.randint(5, 45),
                        duration_ms=rev.duration_ms
                    )

                    report = CanonicalReviewReport(
                        review_id=rev.id,
                        submission_id=sub.id,
                        project_id=project.id,
                        score=final_score,
                        grade=ScoringService.get_grade(final_score),
                        status=status,
                        summary=rev.summary,
                        ai_summary=rev.ai_summary,
                        recommendations=recs,
                        findings=findings_dto[:50], # Sample limit
                        metrics=metrics_dto,
                        statistics=stats,
                        trend=TrendDTO(score_delta=random.uniform(-5, 8) if r_idx > 0 else 0),
                        created_at=review_date,
                        finished_at=rev.finished_at
                    )
                    rev.cached_report = report.model_dump(mode='json')

                total_reviews += 1

        # 4. Generate High-Volume Audit Logs
        print("Generating 3000+ audit events...")
        for _ in range(3500):
            event_user = random.choice(users)
            event_date = start_date + timedelta(seconds=random.randint(0, 180 * 24 * 3600))
            action = random.choice([
                "USER_LOGIN", "USER_LOGOUT", "REVIEW_SUBMITTED", "EXPORT_GENERATED",
                "PROJECT_CREATED", "SETTINGS_UPDATED", "ADMIN_CLEANUP", "PASSWORD_CHANGED"
            ])
            log = AuditLog(
                user_id=event_user.id,
                action=action,
                details=f"Automatic log for {action.lower()} activity.",
                request_id=str(uuid.uuid4())[:8],
                created_at=event_date
            )
            db.add(log)

        db.commit()
        print(f"--- Seeding Complete ---")
        print(f"Users: {len(users)}")
        print(f"Projects: {len(projects)}")
        print(f"Reviews: {total_reviews}")
        print(f"Findings: {total_findings}")
        print(f"Audit Logs: 3500+")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_v1()
