from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_sync_success():
    """Test that the /sync endpoint successfully returns status, message, and documents_synced count."""
    response = client.post("/sync")
    
    # Assert successful HTTP response
    assert response.status_code == 200
    
    # Assert proper content type is returned
    assert response.headers["content-type"].startswith("application/json")
    
    data = response.json()
    
    # Assert expected response structure for the current project implementation
    assert "status" in data
    assert "message" in data
    assert "documents_synced" in data
    
    # Verify specific types and expected default values
    assert data["status"] == "success"
    assert isinstance(data["documents_synced"], int)
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0