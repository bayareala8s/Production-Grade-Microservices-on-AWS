from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["service"] == "order-service"


@patch("app.main.fetch_product")
@patch("app.main.publish_event")
def test_create_order(mock_publish, mock_fetch):
    mock_fetch.return_value = {
        "id": "prod-1",
        "name": "Test Product",
        "price": 10.0,
        "stock": 5,
    }
    response = client.post(
        "/orders",
        json={"user_id": "user-1", "items": [{"product_id": "prod-1", "quantity": 1}]},
    )
    assert response.status_code == 201
    mock_publish.assert_called_once()


@patch("app.main.fetch_product")
def test_create_order_insufficient_stock(mock_fetch):
    mock_fetch.return_value = {
        "id": "prod-1",
        "name": "Test Product",
        "price": 10.0,
        "stock": 0,
    }
    response = client.post(
        "/orders",
        json={"user_id": "user-1", "items": [{"product_id": "prod-1", "quantity": 1}]},
    )
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


@patch("app.main.fetch_product")
def test_create_order_product_not_found(mock_fetch):
    mock_fetch.side_effect = HTTPException(status_code=404, detail="Product missing not found")
    response = client.post(
        "/orders",
        json={"user_id": "user-1", "items": [{"product_id": "missing", "quantity": 1}]},
    )
    assert response.status_code == 404
