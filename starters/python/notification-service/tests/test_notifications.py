import pytest
from fastapi.testclient import TestClient

from app.main import EVENT_LOG, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_events():
    EVENT_LOG.clear()
    yield
    EVENT_LOG.clear()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "notification-service"


def test_welcome_page():
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "BayAreaLa8s" in r.text
    assert "/products" in r.text


def test_receive_order_placed_event():
    payload = {
        "source": "course.orders",
        "detail-type": "OrderPlaced",
        "detail": {
            "order_id": "ord-1",
            "user_id": "user-1",
            "total": 49.99,
            "items": [],
        },
    }
    r = client.post("/events", json=payload)
    assert r.status_code == 200
    assert r.json()["detail_type"] == "OrderPlaced"

    events = client.get("/events").json()["events"]
    assert any(e["detail_type"] == "OrderPlaced" for e in events)
