"""Tests for URL feature extraction."""

from app.ml.feature_extractor import extract_features


def test_extract_features_flags_suspicious_url_patterns():
    features = extract_features("http://192.168.0.1/login/verify?session=123&redirect=secure")

    assert features["uses_https"] == 0
    assert features["contains_ip_address"] == 1
    assert features["contains_suspicious_keyword"] == 1
    assert features["query_parameter_count"] == 2
