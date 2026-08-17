from decimal import Decimal
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import AccountModel

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["service"] == "payment-service"


@patch("app.main.require_approved_customer")
@patch("app.main.publish_payment_event")
def test_transfer_double_entry(mock_publish, mock_kyc):
    mock_kyc.return_value = None
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    a = AccountModel(customer_id="c1", currency="USD", balance=Decimal("100.00"))
    b = AccountModel(customer_id="c2", currency="USD", balance=Decimal("0.00"))
    db.add_all([a, b])
    db.commit()
    db.refresh(a)
    db.refresh(b)
    from_id, to_id = a.id, b.id
    db.close()

    r = client.post(
        "/transfers",
        json={"from_account_id": from_id, "to_account_id": to_id, "amount": "25.50"},
    )
    assert r.status_code == 201
    tid = r.json()["id"]
    ledger = client.get(f"/transfers/{tid}/ledger").json()["entries"]
    assert len(ledger) == 2
    types = {e["entry_type"] for e in ledger}
    assert types == {"DEBIT", "CREDIT"}
    mock_publish.assert_called_once()
