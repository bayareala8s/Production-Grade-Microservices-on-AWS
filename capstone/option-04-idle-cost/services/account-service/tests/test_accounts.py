import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_login_link_account():
    email = f"finops-{time.time()}@example.com"
    assert client.post("/users", json={"email": email, "password": "password123"}).status_code == 201
    login = client.post("/auth/login", json={"email": email, "password": "password123"})
    assert login.status_code == 200
    linked = client.post(
        "/accounts/link",
        json={"aws_account_id": "123456789012", "role_arn": "arn:aws:iam::123456789012:role/FinOpsReadOnly"},
    )
    assert linked.status_code == 201
    assert linked.json()["mode"] == "read_only"
