from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_v2_create_and_list_product_contract() -> None:
    create = client.post(
        "/api/v2/products",
        json={"name": "Mouse", "price": {"amount": 25.0, "currency": "USD"}},
    )
    assert create.status_code == 201
    created = create.json()
    assert created["id"]
    assert created["price"]["amount"] == 25.0
    assert created["price"]["currency"] == "USD"

    r = client.get("/api/v2/products")
    assert r.status_code == 200
    items = r.json()
    assert any(p["id"] == created["id"] for p in items)


def test_v2_discount_validation_error_contract() -> None:
    create = client.post(
        "/api/v2/products",
        json={"name": "Headset", "price": {"amount": 80.0, "currency": "USD"}},
    )
    pid = create.json()["id"]

    r = client.post(f"/api/v2/products/{pid}/discount?percent=200")
    assert r.status_code == 400
    body = r.json()
    # Our StarletteHTTPException handler standardizes these too
    assert body["request_id"]
    assert body["error"]["message"]


