"""URL analysis helpers built on top of extracted features."""

from __future__ import annotations

from app.ml.feature_extractor import extract_features
from app.utils.url_parser import parse_url


def inspect_url(url: str) -> dict:
    """Return derived URL attributes plus human-readable risk reasons."""
    parsed = parse_url(url)
    features = extract_features(url)

    reasons: list[str] = []
    if not features["uses_https"]:
        reasons.append("URL does not use HTTPS.")
    if features["contains_at_symbol"]:
        reasons.append("URL contains '@', which is often used to obscure the real destination.")
    if features["contains_ip_address"]:
        reasons.append("URL uses an IP address instead of a domain name.")
    if features["hyphen_count"] >= 2:
        reasons.append("URL contains multiple hyphens in the domain.")
    if features["contains_suspicious_keyword"]:
        reasons.append("URL contains phishing-associated keywords.")
    if features["subdomain_count"] >= 3:
        reasons.append("URL contains an unusually large number of subdomains.")
    if features["special_character_count"] >= 4:
        reasons.append("URL contains many special characters.")

    return {
        "normalized_url": parsed.normalized,
        "hostname": parsed.hostname,
        "scheme": parsed.scheme,
        "path": parsed.path,
        "length": features["url_length"],
        "uses_https": bool(features["uses_https"]),
        "features": features,
        "reasons": reasons,
    }
