import sys
import os
from os.path import abspath, dirname

# Add project root to sys.path
sys.path.insert(0, abspath(dirname(dirname(__file__))))

from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.services.password_service import PasswordService
from app.repositories.user_repository import UserRepository

def seed_admin():
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        admin_email = "admin@codesage.local"

        if not repo.get_by_email(admin_email):
            print("Creating admin user...")
            admin_user = User(
                email=admin_email,
                username="admin",
                full_name="System Administrator",
                password_hash=PasswordService.hash_password("admin_password_123"),
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True
            )
            repo.create(admin_user)
            print(f"Admin user created successfully: {admin_email}")
        else:
            print(f"Admin user already exists: {admin_email}")

    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
