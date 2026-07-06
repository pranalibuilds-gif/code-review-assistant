from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.execute(
            select(User).where(User.email == email.lower())
        ).scalar_one_or_none()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        return list(self.db.execute(
            select(User).offset(skip).limit(limit)
        ).scalars().all())

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
