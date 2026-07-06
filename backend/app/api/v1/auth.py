from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.security import get_db, get_current_user
from app.schemas.auth import UserCreate, UserResponse, LoginRequest, Token
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    auth_service = AuthService(db)
    user = auth_service.register_user(user_in)
    return {"success": True, "data": user}

@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password to get a JWT token.
    """
    auth_service = AuthService(db)
    token = auth_service.authenticate_user(login_data)
    return {"success": True, "data": token}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return {"success": True, "data": current_user}
