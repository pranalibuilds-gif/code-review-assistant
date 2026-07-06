from datetime import datetime, timezone, timedelta

small_profile = {
    "name": "small",
    "display_name": "Small Team Demo",
    "seed": 1103,
    "user_count": 8,
    "project_count": 6,
    "min_reviews_per_project": 3,
    "max_reviews_per_project": 5,
    "audit_event_count": 250,
    "start_date": datetime(2025, 8, 1, tzinfo=timezone.utc),
    "end_date": datetime(2025, 12, 31, tzinfo=timezone.utc),
    "timeline_events": [
        "Initial code quality baseline established",
        "Security assessment and remediation sprint",
        "Release readiness review completed",
    ],
}
