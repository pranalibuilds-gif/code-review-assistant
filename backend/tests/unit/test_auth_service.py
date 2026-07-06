import pytest
from unittest.mock import MagicMock
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate, LoginRequest
from app.models.user import User, UserRole

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def auth_service(mock_db):
    return AuthService(mock_db)

def test_register_user_success(auth_service, mock_db):
    user_in = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        full_name="Test User"
    )

    # Mock repo behaviors
    auth_service.repo.get_by_email = MagicMock(return_value=None)
    auth_service.repo.get_by_username = MagicMock(return_value=None)
    auth_service.repo.create = MagicMock(side_effect=lambda x: x)

    user = auth_service.register_user(user_in)

    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert "password123" not in user.password_hash # Should be hashed

def test_register_duplicate_email(auth_service):
    user_in = UserCreate(email="dup@example.com", username="u", password="p12345678")
    auth_service.repo.get_by_email = MagicMock(return_value=User(email="dup@example.com"))

    with pytest.raises(Exception) as exc:
        auth_service.register_user(user_in)
    assert "already exists" in str(exc.value)

def test_authenticate_user_success(auth_service):
    login_data = LoginRequest(email="test@example.com", password="password123")

    from app.services.password_service import PasswordService
    hashed = PasswordService.hash_password("password123")

    mock_user = User(
        id="550e8400-e29b-41d4-a716-446655440000",
        email="test@example.com",
        password_hash=hashed,
        is_active=True,
        role=UserRole.USER
    )

    auth_service.repo.get_by_email = MagicMock(return_value=mock_user)

    token = auth_service.authenticate_user(login_data)
    assert token.access_token is not None
    assert token.token_type == "bearer"
