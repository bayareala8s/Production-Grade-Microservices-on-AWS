from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.main.publish_finding")
def test_recommendations_recommend_only(mock_pub):
    r = client.post(
        "/events",
        json={
            "source": "capstone.finops.analyzer",
            "detail-type": "IdleCostScored",
            "detail": {
                "scan_id": "scan-1",
                "findings": [
                    {
                        "resource_type": "NAT",
                        "resource_id": "nat-1",
                        "idle_score": 0.95,
                        "estimated_monthly_usd": 32.85,
                        "reason": "idle nat",
                    }
                ],
            },
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    assert body["recommendations"][0]["auto_destroy"] is False
    assert body["recommendations"][0]["action"] == "stop_nat_or_platform"
    listed = client.get("/recommendations").json()["recommendations"]
    assert listed
    mock_pub.assert_called()
