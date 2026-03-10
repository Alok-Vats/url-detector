"""High-level orchestration for URL analysis requests."""

from __future__ import annotations

from app.services.blacklist_service import get_blacklist_match
from app.services.url_service import inspect_url
from app.services.whitelist_service import get_whitelist_match


def analyze_url(url: str) -> dict:
    """Return a deterministic result using list matches and extracted features."""
    details = inspect_url(url)
    whitelist_match = get_whitelist_match(url)
    blacklist_match = get_blacklist_match(url)

    if whitelist_match:
        return _build_response(
            url,
            "legitimate",
            0.99,
            ["Matched trusted whitelist entry."],
            details,
            matched_list="whitelist",
            matched_entry=whitelist_match,
        )

    if blacklist_match:
        return _build_response(
            url,
            "phishing",
            0.99,
            ["Matched known blacklist entry."],
            details,
            matched_list="blacklist",
            matched_entry=blacklist_match,
        )

    risk_reasons = details["reasons"]
    if risk_reasons:
        return _build_response(url, "phishing", 0.74, risk_reasons, details, matched_list=None)

    return _build_response(
        url,
        "legitimate",
        0.81,
        ["No suspicious heuristic flags were detected in the initial scan."],
        details,
        matched_list=None,
    )


def _build_response(
    url: str,
    prediction: str,
    confidence: float,
    reasons: list[str],
    details: dict,
    matched_list: str | None,
    matched_entry: dict | None = None,
) -> dict:
    """Format response payloads consistently for UI and API consumers."""
    return {
        "url": url,
        "prediction": prediction,
        "confidence": confidence,
        "reasons": reasons,
        "details": details,
        "matched_list": matched_list,
        "matched_entry": matched_entry,
    }
