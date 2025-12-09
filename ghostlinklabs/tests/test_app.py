import json
import pytest
from fastapi.testclient import TestClient

from ghostlink.main import app, ipfs, items


@pytest.fixture(autouse=True)
def clear_state():
    from ghostlink.database import Database
    from ghostlink.main import set_db
    
    # Reset the app state
    items.clear()
    ipfs.storage.clear()
    
    # Use a test database
    test_db = Database("sqlite:///:memory:")
    set_db(test_db)


client = TestClient(app)


def test_post_items_stores_data():
    payload = {"name": "item1", "value": 42}
    response = client.post("/items", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "item1"
    assert "hash" in data

    items_resp = client.get("/items")
    assert items_resp.status_code == 200
    items_data = items_resp.json()
    assert len(items_data) == 1
    assert items_data[0]["hash"] == data["hash"]

    ipfs_resp = client.get(f"/ipfs/{data['hash']}")
    assert ipfs_resp.status_code == 200
    assert ipfs_resp.json()["data"] == json.dumps(payload)


def test_symbolic_reasoning():
    resp = client.post("/reasoning/", json={"text": "Life and love through darkness"})
    assert resp.status_code == 200
    assert resp.json()["processed"] == "journey and light through adversity"


def test_ipfs_store_and_retrieve():
    store_resp = client.post("/ipfs/store", json={"data": "hello"})
    assert store_resp.status_code == 200
    cid = store_resp.json()["cid"]

    get_resp = client.get(f"/ipfs/{cid}")
    assert get_resp.status_code == 200
    assert get_resp.json()["data"] == "hello"
