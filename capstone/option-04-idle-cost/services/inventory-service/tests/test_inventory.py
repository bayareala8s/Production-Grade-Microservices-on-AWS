from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.main.publish_scan_completed")
def test_mock_scan(mock_pub):
    r = client.post("/scans", json={"aws_account_id": "123456789012"})
    assert r.status_code == 201
    body = r.json()
    assert body["resource_count"] >= 4
    assert body["mode"] in ("mock", "mock_fallback", "aws")
    resources = client.get(f"/scans/{body['id']}/resources").json()["resources"]
    types = {x["resource_type"] for x in resources}
    assert {"NAT", "ALB", "ECS_SERVICE", "EIP"}.issubset(types)
    mock_pub.assert_called_once()
