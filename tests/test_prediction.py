"""Tests for URL prediction orchestration."""

from pathlib import Path

from app import create_app
from app.db.seed_data import seed_defaults
from app.ml.train_model import train_and_save_model
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


def test_analyze_url_uses_trained_model_when_available(tmp_path):
    dataset_path = Path("data/raw/phishing_urls.csv")
    model_path = tmp_path / "phishing_model.pkl"
    metrics_path = tmp_path / "metrics.json"
    train_and_save_model(dataset_path, model_path, metrics_path)

    app = create_app("testing")
    app.config["MODEL_PATH"] = str(model_path)

    with app.app_context():
        result = analyze_url("http://verify-bank-account.example.net/update")

    assert result["prediction"] in {"phishing", "legitimate"}
    assert 0.0 <= result["confidence"] <= 1.0
