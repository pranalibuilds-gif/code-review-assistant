import random
from datetime import datetime, timezone
from typing import Dict

from app.models.user import User, UserRole
from app.services.password_service import PasswordService


def seed_users(db, profile) -> Dict[str, object]:
    default_users = [
        {"email": "admin@codesage.local", "username": "admin", "full_name": "Platform Admin", "role": UserRole.ADMIN},
        {"email": "sharma@codesage.local", "username": "sharmadev", "full_name": "Mira Sharma", "role": UserRole.USER},
        {"email": "tayler@codesage.local", "username": "tayler", "full_name": "Tayler Brooks", "role": UserRole.USER},
        {"email": "kwon@codesage.local", "username": "kwon", "full_name": "Soo Kwon", "role": UserRole.USER},
        {"email": "nguyen@codesage.local", "username": "nguyent", "full_name": "Tien Nguyen", "role": UserRole.USER},
        {"email": "garcia@codesage.local", "username": "garciar", "full_name": "Lucia Garcia", "role": UserRole.USER},
    ]

    demo_password = "Demo2026!"
    seeded = {"admin_password": demo_password, "demo_user_password": demo_password}

    users = []
    for user_def in default_users:
        existing = db.query(User).filter(User.email == user_def["email"]).first()
        if existing:
            users.append(existing)
            continue

        user = User(
            email=user_def["email"],
            username=user_def["username"],
            full_name=user_def["full_name"],
            role=user_def["role"],
            password_hash=PasswordService.hash_password(demo_password),
            is_active=True,
            is_verified=True,
        )
        db.add(user)
        db.flush()
        users.append(user)

    demo_user = next((u for u in users if u.username == "tayler"), users[-1])
    seeded["admin"] = next(u for u in users if u.username == "admin")
    seeded["demo_user"] = demo_user
    return seeded
