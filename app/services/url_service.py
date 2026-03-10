"""URL inspection logic used before the ML layer exists."""

from __future__ import annotations

from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = ("login", "verify", "secure", "update", "account", "bank")


def inspect_url(url: str) -> dict:
    """Return basic derived URL attributes and simple risk indicators."""
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    path = parsed.path.lower()

    reasons: list[str] = []
    if parsed.scheme != "https":
        reasons.append("URL does not use HTTPS.")
    if "@" in url:
        reasons.append("URL contains '@', which is often used to obscure the real destination.")
    if sum(char in "-_" for char in hostname) > 2:
        reasons.append("URL contains several separator characters in the domain.")
    if any(keyword in f"{hostname}{path}" for keyword in SUSPICIOUS_KEYWORDS):
        reasons.append("URL contains phishing-associated keywords.")

    return {
        "hostname": hostname,
        "scheme": parsed.scheme,
        "path": parsed.path,
        "length": len(url),
        "uses_https": parsed.scheme == "https",
        "reasons": reasons,
    }
