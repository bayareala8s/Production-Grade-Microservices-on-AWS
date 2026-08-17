from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["service"] == "inventory-service"


def test_reserve_and_release():
    with TestClient(app) as client:
        client.put(
            "/inventory/prod-1",
            json={"product_id": "prod-1", "available": 10},
        )
        r = client.post(
            "/inventory/prod-1/reserve",
            json={"quantity": 3, "order_id": "ord-1"},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["available"] == 7
        assert body["reserved"] == 3

        r2 = client.post(
            "/inventory/prod-1/release",
            json={"quantity": 3, "order_id": "ord-1"},
        )
        assert r2.status_code == 200
        assert r2.json()["available"] == 10
        assert r2.json()["reserved"] == 0


def test_reserve_insufficient_stock():
    with TestClient(app) as client:
        client.put(
            "/inventory/prod-1",
            json={"product_id": "prod-1", "available": 1},
        )
        r = client.post(
            "/inventory/prod-1/reserve",
            json={"quantity": 5, "order_id": "ord-2"},
        )
        assert r.status_code == 409
