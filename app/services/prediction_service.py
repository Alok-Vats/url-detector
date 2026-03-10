"""High-level orchestration for URL analysis requests."""

from __future__ import annotations

from app.services.blacklist_service import is_blacklisted
from app.services.url_service import inspect_url
from app.services.whitelist_service import is_whitelisted


def analyze_url(url: str) -> dict:
    """Return a deterministic result using list checks and heuristics."""
    details = inspect_url(url)

    if is_whitelisted(url):
        return _build_response(url, "legitimate", 0.99, ["Matched trusted whitelist entry."], details)

    if is_blacklisted(url):
        return _build_response(url, "phishing", 0.99, ["Matched known blacklist entry."], details)

    risk_reasons = details["reasons"]
    if risk_reasons:
        return _build_response(url, "phishing", 0.74, risk_reasons, details)

    return _build_response(
        url,
        "legitimate",
        0.81,
        ["No suspicious heuristic flags were detected in the initial scan."],
        details,
    )


def _build_response(
    url: str, prediction: str, confidence: float, reasons: list[str], details: dict
) -> dict:
    """Format response payloads consistently for UI and API consumers."""
    return {
        "url": url,
        "prediction": prediction,
        "confidence": confidence,
        "reasons": reasons,
        "details": details,
    }
