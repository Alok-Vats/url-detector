"""Route tests for health, prediction integration, and history."""

from app import create_app
from app.services.history_service import get_scan_history


def test_health_check():
    app = create_app("testing")

    with app.test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_analyze_route_saves_scan_history():
    app = create_app("testing")

    with app.test_client() as client:
        response = client.post("/analyze", data={"url": "https://www.google.com"})

        assert response.status_code == 200

        with app.app_context():
            history = get_scan_history()

    assert len(history) >= 1
    assert history[0]["input_value"] == "https://www.google.com"


def test_history_route_returns_recent_scans():
    app = create_app("testing")

    with app.test_client() as client:
        client.post("/analyze", json={"url": "http://secure-login-example.com"})
        response = client.get("/history", headers={"Accept": "application/json"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "success"
    assert len(payload["data"]) >= 1
