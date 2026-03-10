"""Input validation helpers."""

from __future__ import annotations

import ipaddress
import re

from app.utils.url_parser import parse_url


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


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


def validate_email_input(sender: str, subject: str, body: str) -> list[str]:
    """Validate submitted email fields and return user-facing errors."""
    errors: list[str] = []
    normalized_sender = sender.strip()

    if not normalized_sender:
        errors.append("Sender email is required.")
    elif not _looks_like_email_address(normalized_sender):
        errors.append("Sender email must be a valid email address.")

    if not subject.strip():
        errors.append("Email subject is required.")

    if not body.strip():
        errors.append("Email body is required.")

    return errors


def _looks_like_email_address(sender: str) -> bool:
    """Return True when the sender value resembles a mailbox string."""
    if EMAIL_PATTERN.match(sender):
        return True

    if "<" in sender and ">" in sender:
        mailbox = sender.split("<", maxsplit=1)[-1].rstrip(">").strip()
        return bool(EMAIL_PATTERN.match(mailbox))

    return False
