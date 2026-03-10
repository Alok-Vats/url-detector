"""Feature extraction utilities for URL phishing analysis."""

from __future__ import annotations

import ipaddress
from urllib.parse import parse_qsl

from app.utils.url_parser import parse_url


SUSPICIOUS_KEYWORDS = ("login", "verify", "secure", "update", "account", "bank", "signin")


def extract_features(url: str) -> dict:
    """Extract deterministic URL features for rules and future ML models."""
    parsed = parse_url(url)
    lexical_target = f"{parsed.hostname}{parsed.path}".lower()
    dot_count = parsed.hostname.count(".")
    hyphen_count = parsed.hostname.count("-")
    special_character_count = sum(url.count(char) for char in ("@", "?", "&", "=", "_", "%"))
    digit_count = sum(character.isdigit() for character in url)
    query_params = parse_qsl(parsed.query, keep_blank_values=True)

    return {
        "url_length": len(parsed.normalized),
        "domain_length": len(parsed.hostname),
        "path_length": len(parsed.path),
        "subdomain_count": max(dot_count - 1, 0),
        "dot_count": dot_count,
        "hyphen_count": hyphen_count,
        "digit_count": digit_count,
        "special_character_count": special_character_count,
        "query_parameter_count": len(query_params),
        "uses_https": int(parsed.scheme == "https"),
        "contains_ip_address": int(_contains_ip_address(parsed.hostname)),
        "contains_at_symbol": int("@" in url),
        "contains_suspicious_keyword": int(
            any(keyword in lexical_target for keyword in SUSPICIOUS_KEYWORDS)
        ),
    }


def _contains_ip_address(hostname: str) -> bool:
    """Return True when the hostname is an IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        return False
    return True
