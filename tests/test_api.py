import requests

BASE_URL = "http://localhost:8000"


def test_status_endpoint():
    resp = requests.get(f"{BASE_URL}/status", timeout=5)
    assert resp.status_code == 200
    data = resp.json()
    assert "current_generation" in data
    assert "current_fitness" in data


def test_evolve_endpoint():
    resp = requests.post(f"{BASE_URL}/evolve", timeout=30)
    assert resp.status_code == 200
    data = resp.json()
    assert "success" in data
    assert "status" in data
