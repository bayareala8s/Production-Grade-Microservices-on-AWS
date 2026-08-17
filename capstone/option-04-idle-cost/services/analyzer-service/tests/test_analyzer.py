from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.main.publish_scored")
def test_score_idle_resources(mock_pub):
    r = client.post(
        "/events",
        json={
            "source": "capstone.finops.inventory",
            "detail-type": "InventoryScanCompleted",
            "detail": {
                "scan_id": "scan-1",
                "aws_account_id": "123456789012",
                "resources": [
                    {
                        "resource_type": "NAT",
                        "resource_id": "nat-1",
                        "signals": {"bytes_out_7d": 0},
                    },
                    {
                        "resource_type": "EIP",
                        "resource_id": "eip-1",
                        "signals": {"associated": False},
                    },
                ],
            },
        },
    )
    assert r.status_code == 200
    assert r.json()["finding_count"] == 2
    findings = client.get("/findings/scan-1").json()
    assert findings["estimated_monthly_usd_total"] > 0
    mock_pub.assert_called_once()
