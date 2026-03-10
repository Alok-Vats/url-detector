"""Blacklist lookups against the SQLite datastore."""

from __future__ import annotations

from app.db.database import fetch_one
from app.utils.url_parser import extract_domain, normalize_url


def is_blacklisted(url: str) -> bool:
    """Return True when a URL or its domain appears in the blacklist."""
    return get_blacklist_match(url) is not None


def get_blacklist_match(url: str) -> dict | None:
    """Return blacklist match metadata for a URL or its domain."""
    domain = extract_domain(url)
    normalized_url = normalize_url(url)
    row = fetch_one(
        """
        SELECT id, url, domain, reason
        FROM blacklist_urls
        WHERE url = ? OR domain = ?
        LIMIT 1
        """,
        (normalized_url, domain),
    )
    if row is None:
        return None

    return dict(row)
