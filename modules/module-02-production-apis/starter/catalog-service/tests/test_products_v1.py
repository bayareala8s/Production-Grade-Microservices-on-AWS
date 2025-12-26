from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_v1_list_products_contract() -> None:
    r = client.get("/api/v1/products")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert "X-Request-Id" in r.headers


def test_v1_create_product_validation_error_contract() -> None:
    # missing price_usd
    r = client.post("/api/v1/products", json={"name": "Keyboard"})
    assert r.status_code == 422
    body = r.json()
    assert body["error"]["code"] == "validation_error"
    assert body["request_id"]
    assert "X-Request-Id" in r.headers


def test_v1_create_and_get_product() -> None:
    create = client.post("/api/v1/products", json={"name": "Keyboard", "price_usd": 99.5})
    assert create.status_code == 201
    created = create.json()
    assert created["id"]
    assert created["name"] == "Keyboard"
    assert created["price_usd"] == 99.5

    getp = client.get(f"/api/v1/products/{created['id']}")
    assert getp.status_code == 200
    fetched = getp.json()
    assert fetched["id"] == created["id"]


