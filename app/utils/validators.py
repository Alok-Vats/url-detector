"""Input validation helpers."""

from __future__ import annotations

from urllib.parse import urlparse


def validate_url_input(url: str) -> list[str]:
    """Validate submitted URLs and return a list of user-facing errors."""
    errors: list[str] = []

    if not url:
        return ["URL is required."]

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        errors.append("URL must start with http:// or https://.")
    if not parsed.netloc:
        errors.append("URL must include a valid domain name.")

    return errors
