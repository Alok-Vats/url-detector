"""Input validation helpers."""

from __future__ import annotations

import ipaddress

from app.utils.url_parser import parse_url


def validate_url_input(url: str) -> list[str]:
    """Validate submitted URLs and return a list of user-facing errors."""
    errors: list[str] = []

    if not url:
        return ["URL is required."]

    if any(character.isspace() for character in url):
        errors.append("URL must not contain spaces.")

    parsed = parse_url(url)
    if parsed.scheme not in {"http", "https"}:
        errors.append("URL must start with http:// or https://.")
    if not parsed.hostname:
        errors.append("URL must include a valid domain name.")
        return errors

    if len(parsed.hostname) > 253:
        errors.append("URL domain is too long.")

    if "." not in parsed.hostname:
        try:
            ipaddress.ip_address(parsed.hostname)
        except ValueError:
            errors.append("URL must include a valid public domain or IP address.")

    return errors
