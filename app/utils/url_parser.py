"""Helpers for safely extracting URL components."""

from __future__ import annotations

from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    """Return the lower-cased hostname from a URL."""
    return urlparse(url).netloc.lower()
