"""
Simplified API Key Tests

These tests demonstrate that the API key functionality works correctly
by testing the core functionality directly.
"""

import pytest
from ghostlink.database import Database, ApiKey
from ghostlink.main import set_db
from fastapi.testclient import TestClient
from ghostlink.main import app


def test_api_key_creation_and_validation():
    """Test that API keys can be created and validated."""
    # Set up test database
    test_db = Database("sqlite:///:memory:")
    set_db(test_db)
    
    client = TestClient(app)
    
    # Test 1: Create an API key
    response = client.post("/api_keys", json={
        "user_id": "test_user",
        "permissions": "read,write"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["permissions"] == "read,write"
    assert len(data["key"]) > 20  # Should be a substantial token
    
    api_key = data["key"]
    
    # Test 2: Validate the API key
    response = client.get("/api_keys/validate", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    
    validation_data = response.json()
    assert validation_data["valid"] is True
    assert validation_data["user_id"] == "test_user"
    assert validation_data["permissions"] == "read,write"


def test_protected_endpoint_requires_api_key():
    """Test that protected endpoints require valid API keys."""
    # Set up test database
    test_db = Database("sqlite:///:memory:")
    set_db(test_db)
    
    client = TestClient(app)
    
    # Test 1: Access protected endpoint without API key (should fail)
    response = client.get("/external_api/data")
    assert response.status_code == 401
    assert "API key required" in response.json()["detail"]
    
    # Test 2: Create API key
    response = client.post("/api_keys", json={
        "user_id": "test_user",
        "permissions": "read"
    })
    api_key = response.json()["key"]
    
    # Test 3: Access protected endpoint with API key (should work)
    response = client.get("/external_api/data", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Secured data access"
    assert data["user_id"] == "test_user"


def test_optional_api_key_endpoints():
    """Test that optional API key endpoints work with and without keys."""
    # Set up test database
    test_db = Database("sqlite:///:memory:")
    set_db(test_db)
    
    client = TestClient(app)
    
    # Test 1: Create item without API key
    response = client.post("/items", json={"name": "test", "value": 42})
    assert response.status_code == 200
    
    item_data = response.json()
    assert item_data["name"] == "test"
    assert "created_by" not in item_data
    
    # Test 2: Create API key and use it
    response = client.post("/api_keys", json={
        "user_id": "creator_user",
        "permissions": "read,write"
    })
    api_key = response.json()["key"]
    
    # Test 3: Create item with API key
    response = client.post("/items", 
                          json={"name": "authenticated", "value": 100},
                          headers={"X-API-Key": api_key})
    assert response.status_code == 200
    
    item_data = response.json()
    assert item_data["name"] == "authenticated"
    assert item_data["created_by"] == "creator_user"


def test_invalid_api_key_rejected():
    """Test that invalid API keys are properly rejected."""
    # Set up test database
    test_db = Database("sqlite:///:memory:")
    set_db(test_db)
    
    client = TestClient(app)
    
    # Test with invalid API key
    response = client.get("/external_api/data", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 403
    assert "Invalid or expired API key" in response.json()["detail"]


def test_api_key_permissions():
    """Test API key permission system."""
    # Test the ApiKey model directly
    api_key = ApiKey(permissions="read,write")
    
    assert api_key.has_permission("read") is True
    assert api_key.has_permission("write") is True
    assert api_key.has_permission("admin") is False
    
    # Test empty permissions
    empty_key = ApiKey(permissions="")
    assert empty_key.has_permission("read") is False
    
    # Test None permissions
    none_key = ApiKey(permissions=None)
    assert none_key.has_permission("read") is False


if __name__ == "__main__":
    # Run tests directly
    test_api_key_creation_and_validation()
    test_protected_endpoint_requires_api_key()
    test_optional_api_key_endpoints()
    test_invalid_api_key_rejected()
    test_api_key_permissions()
    print("✅ All simplified API key tests passed!")