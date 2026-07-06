from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union
from jose import jwt
from app.core.config import settings

class JWTService:
    @staticmethod
    def create_access_token(
        subject: Union[str, Any],
        role: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {"exp": expire, "sub": str(subject), "role": role}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        return jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
