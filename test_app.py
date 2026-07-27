import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "cpu_percent" in data
    assert "memory_percent" in data
