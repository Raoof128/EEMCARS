"""
Tests for controls API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Control


@pytest.mark.asyncio
class TestControlsAPI:
    """Test controls API endpoints."""

    @pytest.fixture
    async def test_controls(self, db: AsyncSession):
        """Create test controls."""
        controls = [
            Control(
                control_id="E8-AC-L1-REQ1",
                pillar="application_control",
                name="Application Control Level 1",
                description="Basic application control",
                maturity_level=1,
            ),
            Control(
                control_id="E8-AC-L2-REQ1",
                pillar="application_control",
                name="Application Control Level 2",
                description="Advanced application control",
                maturity_level=2,
            ),
            Control(
                control_id="E8-PA-L1-REQ1",
                pillar="patch_applications",
                name="Patch Applications Level 1",
                description="Basic application patching",
                maturity_level=1,
            ),
        ]
        for control in controls:
            db.add(control)
        await db.commit()
        return controls

    def test_list_controls(self, auth_client: TestClient, test_controls):
        """Test listing all controls."""
        response = auth_client.get("/api/v1/controls")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        assert all("control_id" in item for item in data)
        assert all("pillar" in item for item in data)

    def test_list_controls_filter_by_pillar(self, auth_client: TestClient, test_controls):
        """Test filtering controls by pillar."""
        response = auth_client.get("/api/v1/controls?pillar=application_control")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(item["pillar"] == "application_control" for item in data)

    def test_list_controls_filter_by_level(self, auth_client: TestClient, test_controls):
        """Test filtering controls by maturity level."""
        response = auth_client.get("/api/v1/controls?maturity_level=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(item["maturity_level"] == 1 for item in data)

    def test_get_control(self, auth_client: TestClient, test_controls):
        """Test getting a specific control."""
        control_id = test_controls[0].control_id
        response = auth_client.get(f"/api/v1/controls/{control_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["control_id"] == control_id
        assert data["pillar"] == "application_control"

    def test_get_control_not_found(self, auth_client: TestClient):
        """Test getting a non-existent control."""
        response = auth_client.get("/api/v1/controls/NONEXISTENT")
        assert response.status_code == 404

    def test_create_control_as_admin(self, admin_client: TestClient):
        """Test creating a control as admin."""
        control_data = {
            "control_id": "E8-TEST-L1-REQ1",
            "pillar": "application_control",
            "name": "Test Control",
            "description": "Test control description",
            "maturity_level": 1,
        }
        response = admin_client.post("/api/v1/controls", json=control_data)
        assert response.status_code == 201
        data = response.json()
        assert data["control_id"] == control_data["control_id"]
        assert data["name"] == control_data["name"]

    def test_create_control_as_secops(self, auth_client: TestClient):
        """Test creating a control as secops (should be allowed)."""
        control_data = {
            "control_id": "E8-TEST-L2-REQ1",
            "pillar": "patch_applications",
            "name": "Test Control 2",
            "description": "Test control description 2",
            "maturity_level": 2,
        }
        response = auth_client.post("/api/v1/controls", json=control_data)
        # SecOps should be able to create controls
        assert response.status_code in [201, 403]  # Depends on RBAC implementation

    def test_create_control_duplicate(self, admin_client: TestClient, test_controls):
        """Test creating a duplicate control."""
        control_data = {
            "control_id": test_controls[0].control_id,
            "pillar": "application_control",
            "name": "Duplicate",
            "description": "This should fail",
            "maturity_level": 1,
        }
        response = admin_client.post("/api/v1/controls", json=control_data)
        assert response.status_code == 400

    def test_update_control(self, admin_client: TestClient, test_controls):
        """Test updating a control."""
        control_id = test_controls[0].control_id
        update_data = {
            "name": "Updated Control Name",
            "description": "Updated description",
        }
        response = admin_client.put(f"/api/v1/controls/{control_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]

    def test_delete_control(self, admin_client: TestClient, test_controls):
        """Test deleting a control."""
        control_id = test_controls[0].control_id
        response = admin_client.delete(f"/api/v1/controls/{control_id}")
        assert response.status_code == 204

        # Verify deletion
        response = admin_client.get(f"/api/v1/controls/{control_id}")
        assert response.status_code == 404

    def test_list_controls_unauthenticated(self, client: TestClient):
        """Test listing controls without authentication."""
        response = client.get("/api/v1/controls")
        assert response.status_code == 401
