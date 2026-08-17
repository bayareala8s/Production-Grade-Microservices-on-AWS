import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_login_includes_tenant_claim():
    from jose import jwt
    from app.security import JWT_SECRET, JWT_ALGORITHM

    email = f"user-{time.time()}@saas.example"
    r = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "password123",
            "tenant_id": "tenant-abc",
            "role": "admin",
        },
    )
    assert r.status_code == 201
    assert r.json()["tenant_id"] == "tenant-abc"

    login = client.post("/auth/login", json={"email": email, "password": "password123"})
    assert login.status_code == 200
    claims = jwt.decode(login.json()["access_token"], JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert claims["tenant_id"] == "tenant-abc"
    assert claims["role"] == "admin"
