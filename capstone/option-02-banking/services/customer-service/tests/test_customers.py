from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["service"] == "customer-service"


def test_create_and_approve_kyc():
    email = "alice@bank.example"
    r = client.post("/customers", json={"email": email, "full_name": "Alice Example"})
    # may 409 on re-run in same process — use unique email
    if r.status_code == 409:
        r = client.post(
            "/customers",
            json={"email": f"alice-{id(r)}@bank.example", "full_name": "Alice Example"},
        )
    assert r.status_code == 201
    cid = r.json()["id"]
    assert r.json()["kyc_status"] == "PENDING"

    kyc = client.patch(f"/customers/{cid}/kyc", json={"kyc_status": "APPROVED"})
    assert kyc.status_code == 200
    assert kyc.json()["kyc_status"] == "APPROVED"
