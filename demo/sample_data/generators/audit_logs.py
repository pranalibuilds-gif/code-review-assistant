import random
from datetime import timedelta
from typing import Dict, List

from app.models.audit_log import AuditLog

AUDIT_ACTIONS = [
    "USER_LOGIN", "USER_LOGOUT", "REVIEW_SUBMITTED", "EXPORT_GENERATED",
    "PROJECT_CREATED", "SETTINGS_UPDATED", "PASSWORD_CHANGED", "PERMISSION_UPDATED",
    "AUDIT_REVIEWED", "SECURITY_SCAN_RUN", "DEPLOYMENT_APPROVED"
]

AUDIT_TEMPLATES = [
    "Recorded security remediation tasks.",
    "Tracked review velocity and team progress.",
    "Logged governance updates for compliance readiness.",
    "Captured system access and session activity.",
    "Documented platform configuration changes.",
    "Stored audit trail for production release activity.",
]


def seed_audit_logs(db, profile, users, projects: List):
    logs = []
    user_candidates = [u for key, u in users.items() if key not in {"admin_password", "demo_user_password"}]
    for _ in range(profile["audit_event_count"]):
        user = random.choice(user_candidates)
        action = random.choice(AUDIT_ACTIONS)
        details = random.choice(AUDIT_TEMPLATES)
        log = AuditLog(
            user_id=user.id,
            action=action,
            details=details,
            request_id=f"req_{random.randint(1000,9999)}",
            ip_address=f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
        )
        logs.append(log)
    db.add_all(logs)
    print(f"Seeded {len(logs)} audit events.")
