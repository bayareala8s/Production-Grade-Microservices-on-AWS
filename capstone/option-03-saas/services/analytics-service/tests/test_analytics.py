from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.main.publish_usage")
def test_record_usage(mock_publish):
    r = client.post(
        "/usage",
        json={"tenant_id": "t-1", "metric": "api_calls", "units": 10},
    )
    assert r.status_code == 201
    assert r.json()["units"] == 10
    mock_publish.assert_called_once()
    listed = client.get("/tenants/t-1/usage")
    assert len(listed.json()) >= 1
