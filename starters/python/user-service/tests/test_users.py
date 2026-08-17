import time

from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["service"] == "user-service"


def test_create_and_login_user():
    email = f"test-{int(time.time())}@example.com"
    with TestClient(app) as client:
        client.post(
            "/users",
            json={"email": email, "name": "Test User", "password": "password123"},
        )
        login = client.post(
            "/auth/login", json={"email": email, "password": "password123"}
        )
        assert login.status_code == 200
        assert "access_token" in login.json()


def test_duplicate_email_returns_409():
    email = f"dup-{int(time.time())}@example.com"
    payload = {"email": email, "name": "Test User", "password": "password123"}
    with TestClient(app) as client:
        assert client.post("/users", json=payload).status_code == 201
        conflict = client.post("/users", json=payload)
        assert conflict.status_code == 409
        assert "already registered" in conflict.json()["detail"].lower()


def test_login_invalid_password_returns_401():
    email = f"badpw-{int(time.time())}@example.com"
    with TestClient(app) as client:
        client.post(
            "/users",
            json={"email": email, "name": "Test User", "password": "password123"},
        )
        login = client.post(
            "/auth/login", json={"email": email, "password": "wrong-password"}
        )
        assert login.status_code == 401
