import pytest
from fastapi.testclient import TestClient

from app.main import EVENT_LOG, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear():
    EVENT_LOG.clear()
    yield
    EVENT_LOG.clear()


def test_health_and_welcome():
    assert client.get("/health").json()["service"] == "notification-service"
    assert "Banking" in client.get("/").text


def test_receive_fraud_alert():
    r = client.post(
        "/events",
        json={
            "source": "capstone.banking.fraud",
            "detail-type": "FraudAlert",
            "detail": {"transfer_id": "t1", "risk_score": 0.9, "decision": "REVIEW"},
        },
    )
    assert r.status_code == 200
    assert any(e["detail_type"] == "FraudAlert" for e in client.get("/events").json()["events"])
