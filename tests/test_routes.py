"""Basic route tests for the Phase 1 setup."""

from app import create_app


def test_health_check():
    app = create_app("testing")

    with app.test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
