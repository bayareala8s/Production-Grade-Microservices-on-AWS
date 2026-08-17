import pytest
from fastapi.testclient import TestClient

from app.main import EVENT_LOG, SCORES, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear():
    EVENT_LOG.clear()
    SCORES.clear()
    yield
    EVENT_LOG.clear()
    SCORES.clear()


def test_health():
    assert client.get("/health").json()["service"] == "fraud-service"


def test_score_high_value_payment():
    r = client.post(
        "/events",
        json={
            "source": "capstone.banking.payments",
            "detail-type": "PaymentPlaced",
            "detail": {
                "transfer_id": "t1",
                "customer_id": "c1",
                "amount": "15000.00",
                "high_value": True,
            },
        },
    )
    assert r.status_code == 200
    assert r.json()["score"]["decision"] == "REVIEW"
    assert client.get("/scores").json()["scores"]
