"""Tests for validation and list lookup services."""

from pathlib import Path

from app import create_app
from app.db.seed_data import seed_defaults
from app.ml.preprocess import build_feature_frame, load_dataset
from app.services.blacklist_service import get_blacklist_match
from app.services.whitelist_service import get_whitelist_match
from app.utils.validators import validate_url_input


def test_validate_url_input_rejects_invalid_values():
    errors = validate_url_input("ftp://bad url")

    assert "URL must not contain spaces." in errors
    assert "URL must start with http:// or https://." in errors


def test_blacklist_and_whitelist_services_find_seeded_matches():
    app = create_app("testing")

    with app.app_context():
        seed_defaults()
        whitelist_match = get_whitelist_match("https://www.google.com")
        blacklist_match = get_blacklist_match("http://secure-login-example.com")

    assert whitelist_match is not None
    assert blacklist_match is not None


def test_dataset_loading_and_feature_preparation():
    dataset = load_dataset(Path("data/raw/phishing_urls.csv"))
    feature_frame, labels = build_feature_frame(dataset)

    assert not dataset.empty
    assert feature_frame.shape[0] == labels.shape[0]
    assert "uses_https" in feature_frame.columns
