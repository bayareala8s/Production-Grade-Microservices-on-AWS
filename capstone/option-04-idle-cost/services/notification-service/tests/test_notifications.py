import pytest
from fastapi.testclient import TestClient

from app.main import EVENT_LOG, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear():
    EVENT_LOG.clear()
    yield
    EVENT_LOG.clear()


def test_welcome_and_finding():
    assert "Idle Cost" in client.get("/").text
    r = client.post(
        "/events",
        json={
            "source": "capstone.finops.recommendation",
            "detail-type": "IdleCostFinding",
            "detail": {"action": "release_eip", "auto_destroy": False},
        },
    )
    assert r.status_code == 200
    assert any(e["detail_type"] == "IdleCostFinding" for e in client.get("/events").json()["events"])
