import json
import random
from datetime import timedelta
from typing import Dict, List

from app.models.submission import Submission
from app.models.review import Review
from app.models.finding import Finding
from app.models.metric import Metric
from app.models.artifact import Artifact
from app.models.enums import SubmissionType, ReviewStatus, Severity, FindingSource
from app.services.aggregation.scoring_service import ScoringService
from app.services.aggregation.dto import CanonicalReviewReport, StatisticsDTO, TrendDTO, FindingDTO, MetricDTO


RECOMMENDATIONS = [
    "Reduce function complexity by extracting inner logic to private methods.",
    "Add explicit type hints and improve docstrings for developer handoff.",
    "Split large modules into smaller maintainable packages.",
    "Replace duplicated logic with shared utilities.",
    "Validate external inputs to prevent injection risk.",
    "Improve exception handling with specific error classes.",
    "Increase unit test coverage around edge cases.",
    "Use dependency injection for better testability.",
    "Rename ambiguous variables to communicate intent clearly.",
    "Remove dead code and reduce imported modules.",
    "Improve logging around external service calls for observability.",
]

FINDING_CATEGORIES = ["Security", "Complexity", "Style", "Logic", "Documentation", "Compliance"]


def _create_findings(review, final_score):
    findings = []
    num_findings = max(1, int((100 - final_score) * random.uniform(0.35, 0.8)))
    for _ in range(num_findings):
        sev_roll = random.random()
        severity = Severity.CRITICAL if sev_roll > 0.92 else Severity.HIGH if sev_roll > 0.74 else Severity.MEDIUM if sev_roll > 0.48 else Severity.LOW
        source = random.choice(list(FindingSource))
        finding = Finding(
            review_id=review.id,
            source=source,
            severity=severity,
            category=random.choice(FINDING_CATEGORIES),
            title=f"{severity.value.title()} risk in {source.value.lower()} check",
            description="Detected an implementation issue requiring review.",
            recommendation="Refactor and add guard logic to reduce future defects.",
            file_path=f"src/{random.choice(['app', 'services', 'api', 'models', 'utils'])}/module_{random.randint(1,8)}.py",
            line=random.randint(10, 350),
            rule_id=f"RULE-{random.randint(100, 999)}"
        )
        findings.append(finding)
    return findings


def _create_metrics(review, final_score):
    metrics = [
        Metric(
            review_id=review.id,
            metric_name="Maintainability Index",
            metric_value=max(20.0, min(100.0, final_score + random.uniform(-4.5, 4.5)))
        ),
        Metric(
            review_id=review.id,
            metric_name="Average Cyclomatic Complexity",
            metric_value=max(2.0, min(20.0, random.uniform(2.0, 17.5)))
        )
    ]
    return metrics


def seed_reviews(db, profile, users, projects: List):
    review_sum = 0
    finding_sum = 0
    for project in projects:
        quality = random.uniform(52, 78)
        review_count = random.randint(profile["min_reviews_per_project"], profile["max_reviews_per_project"])
        review_times = [profile["start_date"] + timedelta(days=int(i * ((profile["end_date"] - profile["start_date"]).days / review_count))) for i in range(review_count)]

        for idx, review_date in enumerate(review_times):
            quality += random.uniform(-3.5, 5.5)
            final_score = max(0.0, min(98.0, quality))
            status = ReviewStatus.COMPLETED if final_score >= 65 or random.random() > 0.12 else ReviewStatus.PARTIAL_SUCCESS
            if random.random() > 0.975:
                status = ReviewStatus.FAILED
                final_score = max(0.0, final_score - random.uniform(15, 30))

            submission = Submission(
                project_id=project.id,
                submission_type=random.choice(list(SubmissionType)),
                status=status,
                created_at=review_date,
                completed_at=review_date + timedelta(minutes=random.randint(2, 25))
            )
            db.add(submission)
            db.flush()

            review = Review(
                submission_id=submission.id,
                overall_score=final_score if status != ReviewStatus.FAILED else 0,
                status=status,
                started_at=review_date,
                finished_at=submission.completed_at,
                duration_ms=random.randint(8000, 42000),
                summary=f"Review for {project.name} sprint {idx+1}.",
                ai_summary="Analysis indicates further refactoring will improve maintainability." if status == ReviewStatus.COMPLETED else "Review stopped early due to unresolved issues."
            )
            db.add(review)
            db.flush()

            findings = []
            metrics = []
            if status != ReviewStatus.FAILED:
                findings = _create_findings(review, final_score)
                metrics = _create_metrics(review, final_score)
                db.add_all(findings)
                db.add_all(metrics)

            if status == ReviewStatus.COMPLETED and random.random() > 0.2:
                for artifact_type in ["PDF", "MD", "JSON"]:
                    if random.random() > 0.35:
                        db.add(Artifact(
                            review_id=review.id,
                            type=artifact_type,
                            path=f"uploads/{submission.id}/artifacts/{project.name.replace(' ', '_').lower()}_{artifact_type.lower()}.{artifact_type.lower()}"
                        ))

            if status != ReviewStatus.FAILED:
                stats = StatisticsDTO(
                    total_findings=len(findings),
                    critical_count=sum(1 for f in findings if f.severity == Severity.CRITICAL),
                    high_count=sum(1 for f in findings if f.severity == Severity.HIGH),
                    medium_count=sum(1 for f in findings if f.severity == Severity.MEDIUM),
                    low_count=sum(1 for f in findings if f.severity == Severity.LOW),
                    security_count=sum(1 for f in findings if f.source == FindingSource.BANDIT),
                    quality_count=sum(1 for f in findings if f.source == FindingSource.PYLINT),
                    complexity_count=sum(1 for f in findings if f.source == FindingSource.RADON),
                    files_analyzed=random.randint(8, 42),
                    duration_ms=review.duration_ms,
                )

                report = CanonicalReviewReport(
                    review_id=review.id,
                    submission_id=submission.id,
                    project_id=project.id,
                    score=final_score,
                    grade=ScoringService.get_grade(final_score),
                    status=status,
                    summary=review.summary,
                    ai_summary=review.ai_summary,
                    recommendations=[
                        {"title": "AI Recommendation", "description": rec, "impact": "Medium"}
                        for rec in random.sample(RECOMMENDATIONS, k=random.randint(2, 4))
                    ],
                    findings=[FindingDTO.model_validate(f, from_attributes=True) for f in findings[:40]],
                    metrics=[MetricDTO.model_validate(m, from_attributes=True) for m in metrics],
                    statistics=stats,
                    trend=TrendDTO(score_delta=random.uniform(-5.0, 8.0)),
                    created_at=review.started_at,
                    finished_at=review.finished_at,
                )
                review.cached_report = report.model_dump(mode="json")

            review_sum += 1
            finding_sum += len(findings)

    print(f"Seeded {review_sum} reviews and {finding_sum} findings.")
