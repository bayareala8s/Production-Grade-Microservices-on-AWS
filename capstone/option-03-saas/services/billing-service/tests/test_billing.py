from fastapi.testclient import TestClient

from app.main import app


def test_subscribe_and_usage_overage_invoice():
    with TestClient(app) as client:
        plans = client.get("/plans")
        assert plans.status_code == 200
        assert any(p["name"] == "starter" for p in plans.json())

        sub = client.post("/subscriptions", json={"tenant_id": "t-1", "plan_name": "starter"})
        assert sub.status_code == 201

        ev = client.post(
            "/events",
            json={
                "source": "capstone.saas.analytics",
                "detail-type": "UsageRecorded",
                "detail": {"tenant_id": "t-1", "units": 1500, "metric": "api_calls"},
            },
        )
        assert ev.status_code == 200
        assert ev.json()["status"] == "invoiced"

        invoices = client.get("/tenants/t-1/invoices").json()
        assert len(invoices) >= 2
