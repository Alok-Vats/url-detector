"""Tests for URL prediction orchestration."""

from app import create_app
from app.db.seed_data import seed_defaults
from app.services.prediction_service import analyze_url


def test_analyze_url_returns_whitelist_match():
    app = create_app("testing")

    with app.app_context():
        seed_defaults()
        result = analyze_url("https://www.google.com")

    assert result["prediction"] == "legitimate"
    assert result["matched_list"] == "whitelist"


def test_analyze_url_returns_heuristic_phishing_when_not_listed():
    app = create_app("testing")

    with app.app_context():
        result = analyze_url("http://very-secure-login-update.example.com")

    assert result["prediction"] == "phishing"
    assert result["matched_list"] is None
