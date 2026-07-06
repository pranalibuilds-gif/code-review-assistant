from datetime import datetime, timezone

six_year_history_profile = {
    "name": "six_year_history",
    "display_name": "Six-Year History Demo",
    "seed": 9921,
    "user_count": 35,
    "project_count": 34,
    "min_reviews_per_project": 15,
    "max_reviews_per_project": 28,
    "audit_event_count": 7200,
    "start_date": datetime(2020, 1, 1, tzinfo=timezone.utc),
    "end_date": datetime(2026, 12, 31, tzinfo=timezone.utc),
    "timeline_events": [
        "Initial architecture build and secure deployment",
        "Maturity growth with quarterly review cadence",
        "Regulatory compliance and audit readiness",
        "AI-first quality assurance and continuous delivery",
    ],
}
