from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_live() -> None:
    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "X-Request-Id" in r.headers


def test_ready() -> None:
    r = client.get("/health/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "X-Request-Id" in r.headers


