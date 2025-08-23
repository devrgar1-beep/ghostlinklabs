#!/usr/bin/env python3
"""
GhostLink API Key Demonstration Script

This script demonstrates the API key functionality implemented in GhostLink.
It shows:
1. API key creation
2. API key validation
3. Using API keys for authentication
4. Permission-based access control
"""

import uvicorn
from ghostlink.main import app, set_db
from ghostlink.database import Database, ApiKey
from fastapi.testclient import TestClient
import json


def main():
    """Demonstrate API key functionality."""
    print("🔑 GhostLink API Key Functionality Demo")
    print("=" * 50)
    
    # Set up a persistent database for the demo
    db = Database("sqlite:///./demo_ghostlink.db")
    set_db(db)
    
    # Create test client
    client = TestClient(app)
    
    print("\n1. 📝 Creating API Keys...")
    
    # Create different API keys with different permissions
    keys = []
    
    # Read-only key
    response = client.post("/api_keys", json={
        "user_id": "reader_user",
        "permissions": "read"
    })
    if response.status_code == 200:
        read_key = response.json()
        keys.append(("READ", read_key))
        print(f"   ✓ Read-only key: {read_key['key'][:20]}...")
    
    # Read-write key
    response = client.post("/api_keys", json={
        "user_id": "writer_user", 
        "permissions": "read,write"
    })
    if response.status_code == 200:
        write_key = response.json()
        keys.append(("WRITE", write_key))
        print(f"   ✓ Read-write key: {write_key['key'][:20]}...")
    
    # Admin key
    response = client.post("/api_keys", json={
        "user_id": "admin_user",
        "permissions": "read,write,admin"
    })
    if response.status_code == 200:
        admin_key = response.json()
        keys.append(("ADMIN", admin_key))
        print(f"   ✓ Admin key: {admin_key['key'][:20]}...")
    
    print(f"\n2. 🔍 Validating API Keys...")
    for key_type, key_data in keys:
        response = client.get("/api_keys/validate", headers={"X-API-Key": key_data["key"]})
        if response.status_code == 200:
            print(f"   ✓ {key_type} key valid: {key_data['permissions']}")
        else:
            print(f"   ✗ {key_type} key invalid")
    
    print(f"\n3. 🚪 Testing Endpoint Access...")
    
    # Test without API key (should work for most endpoints)
    response = client.get("/items")
    print(f"   Public access to /items: {'✓' if response.status_code == 200 else '✗'}")
    
    # Test external API without key (should fail)
    response = client.get("/external_api/data")
    print(f"   External API without key: {'✗ Blocked' if response.status_code == 401 else '✓ Allowed'}")
    
    # Test external API with read key (should work)
    read_key_data = keys[0][1]
    response = client.get("/external_api/data", headers={"X-API-Key": read_key_data["key"]})
    print(f"   External API with read key: {'✓ Allowed' if response.status_code == 200 else '✗ Blocked'}")
    
    print(f"\n4. 📊 Creating Test Data with API Keys...")
    
    # Create items with different API keys
    write_key_data = keys[1][1]
    
    response = client.post("/items", json={"name": "Public Item", "value": 100})
    print(f"   Create item without key: {'✓' if response.status_code == 200 else '✗'}")
    
    response = client.post("/items", 
                          json={"name": "Writer Item", "value": 200}, 
                          headers={"X-API-Key": write_key_data["key"]})
    if response.status_code == 200:
        item_data = response.json()
        print(f"   Create item with API key: ✓ (created_by: {item_data.get('created_by', 'N/A')})")
    
    print(f"\n5. 🔒 Testing Permission Levels...")
    
    # Get data with different permission levels
    for key_type, key_data in keys:
        response = client.get("/external_api/data", headers={"X-API-Key": key_data["key"]})
        if response.status_code == 200:
            data = response.json()
            items_returned = len(data.get('data', []))
            print(f"   {key_type} user sees {items_returned} items")
    
    print(f"\n✅ API Key Demo Complete!")
    print(f"\n📋 Summary:")
    print(f"   • Created {len(keys)} API keys with different permission levels")
    print(f"   • Demonstrated permission-based access control")
    print(f"   • Showed API key validation and authentication")
    print(f"   • Tested both public and protected endpoints")
    
    print(f"\n🔗 Available Endpoints:")
    print(f"   POST /api_keys           - Create API keys")
    print(f"   GET  /api_keys/validate  - Validate API keys")
    print(f"   GET  /external_api/data  - Protected endpoint (requires API key)")
    print(f"   POST /items              - Create items (optional API key)")
    print(f"   GET  /items              - List items (optional API key)")
    print(f"   POST /reasoning/         - Process text (optional API key)")
    print(f"   POST /ipfs/store         - Store data (optional API key)")
    print(f"   GET  /ipfs/{{hash}}        - Retrieve data (optional API key)")
    
    print(f"\n🌐 To start the server: uvicorn ghostlink.main:app --reload")


if __name__ == "__main__":
    main()