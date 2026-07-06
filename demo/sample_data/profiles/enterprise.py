from datetime import datetime, timezone

enterprise_profile = {
    "name": "enterprise",
    "display_name": "Enterprise Portfolio Demo",
    "seed": 2317,
    "user_count": 28,
    "project_count": 24,
    "min_reviews_per_project": 6,
    "max_reviews_per_project": 12,
    "audit_event_count": 3200,
    "start_date": datetime(2025, 1, 1, tzinfo=timezone.utc),
    "end_date": datetime(2026, 6, 30, tzinfo=timezone.utc),
    "timeline_events": [
        "Executive kickoff and enterprise architecture alignment",
        "Security hardening and DevOps automation wave",
        "Operational risk review and production readiness sprint",
        "AI-driven maintenance and technical debt remediation",
    ],
}
