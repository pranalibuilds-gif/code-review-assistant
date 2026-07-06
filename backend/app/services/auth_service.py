from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, LoginRequest, Token
from app.services.password_service import PasswordService
from app.services.jwt_service import JWTService

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def register_user(self, user_in: UserCreate) -> User:
        if self.repo.get_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )

        if self.repo.get_by_username(user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username is already taken."
            )

        hashed_password = PasswordService.hash_password(user_in.password)
        db_user = User(
            email=user_in.email.lower(),
            username=user_in.username,
            full_name=user_in.full_name,
            password_hash=hashed_password
        )
        return self.repo.create(db_user)

    def authenticate_user(self, login_data: LoginRequest) -> Token:
        user = self.repo.get_by_email(login_data.email)
        if not user or not PasswordService.verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is inactive"
            )

        # Update last login
        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

        access_token = JWTService.create_access_token(
            subject=user.id,
            role=user.role.value
        )

        return Token(access_token=access_token, token_type="bearer")
