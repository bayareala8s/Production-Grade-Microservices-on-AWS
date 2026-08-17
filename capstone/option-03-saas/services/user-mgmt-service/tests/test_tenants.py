from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_tenant_invite_isolation():
    t = client.post("/tenants", json={"name": "Acme Corp"})
    assert t.status_code == 201
    tid = t.json()["id"]
    inv = client.post(f"/tenants/{tid}/invites", json={"email": "dev@acme.example", "role": "admin"})
    assert inv.status_code == 201
    assert inv.json()["tenant_id"] == tid
    members = client.get(f"/tenants/{tid}/members")
    assert len(members.json()) == 1
