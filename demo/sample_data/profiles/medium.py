from datetime import datetime, timezone

medium_profile = {
    "name": "medium",
    "display_name": "Medium Enterprise Demo",
    "seed": 6102,
    "user_count": 18,
    "project_count": 12,
    "min_reviews_per_project": 4,
    "max_reviews_per_project": 8,
    "audit_event_count": 1200,
    "start_date": datetime(2025, 4, 1, tzinfo=timezone.utc),
    "end_date": datetime(2026, 3, 31, tzinfo=timezone.utc),
    "timeline_events": [
        "Platform onboarding and secure API review",
        "Quarterly architecture review and optimization",
        "AI-assisted code quality improvement round",
    ],
}
