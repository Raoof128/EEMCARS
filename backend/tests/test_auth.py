"""
Tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.core.security import verify_password


@pytest.mark.asyncio
class TestAuth:
    """Test authentication endpoints."""

    def test_login_success(self, client: TestClient, test_user: User):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/token",
            data={
                "username": "test@example.com",
                "password": "testpassword123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_email(self, client: TestClient):
        """Test login with invalid email."""
        response = client.post(
            "/api/v1/auth/token",
            data={
                "username": "nonexistent@example.com",
                "password": "testpassword123",
            },
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_invalid_password(self, client: TestClient, test_user: User):
        """Test login with invalid password."""
        response = client.post(
            "/api/v1/auth/token",
            data={
                "username": "test@example.com",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_inactive_user(self, client: TestClient, db: AsyncSession):
        """Test login with inactive user."""
        # Create inactive user
        from app.core.security import get_password_hash
        inactive_user = User(
            email="inactive@example.com",
            hashed_password=get_password_hash("password123"),
            first_name="Inactive",
            last_name="User",
            role="secops",
            is_active=False,
        )
        db.add(inactive_user)
        db.commit()

        response = client.post(
            "/api/v1/auth/token",
            data={
                "username": "inactive@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 401
        assert "Inactive user" in response.json()["detail"]

    def test_get_current_user(self, auth_client: TestClient):
        """Test getting current user."""
        response = auth_client.get("/api/v1/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["role"] == "secops"

    def test_get_current_user_unauthenticated(self, client: TestClient):
        """Test getting current user without authentication."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_password_hashing(self):
        """Test password hashing."""
        from app.core.security import get_password_hash, verify_password

        password = "testpassword123"
        hashed = get_password_hash(password)

        # Verify hash is different from password
        assert hashed != password

        # Verify password verification works
        assert verify_password(password, hashed)
        assert not verify_password("wrongpassword", hashed)

    def test_jwt_token_creation(self):
        """Test JWT token creation."""
        from app.core.security import create_access_token

        token = create_access_token(data={"sub": "test@example.com"})
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
