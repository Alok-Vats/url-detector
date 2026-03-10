"""Tests for URL feature extraction."""

from app.ml.email_feature_extractor import extract_email_features
from app.ml.feature_extractor import extract_features


def test_extract_features_flags_suspicious_url_patterns():
    features = extract_features("http://192.168.0.1/login/verify?session=123&redirect=secure")

    assert features["uses_https"] == 0
    assert features["contains_ip_address"] == 1
    assert features["contains_suspicious_keyword"] == 1
    assert features["query_parameter_count"] == 2


def test_extract_features_for_legitimate_https_url():
    features = extract_features("https://docs.python.org/3/library/pathlib.html")

    assert features["uses_https"] == 1
    assert features["contains_ip_address"] == 0
    assert features["contains_at_symbol"] == 0


def test_extract_email_features_flags_urgent_message():
    features = extract_email_features(
        "Security Team <alerts@fake-bank.example>",
        "Urgent: Verify your password",
        "Click immediately: http://reset-account.example/login",
    )

    assert features["contains_urgent_language"] == 1
    assert features["contains_suspicious_keyword"] == 1
    assert features["url_count"] == 1
