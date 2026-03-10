"""Whitelist lookups against the SQLite datastore."""

from __future__ import annotations

from app.db.database import fetch_one
from app.utils.url_parser import extract_domain


def is_whitelisted(url: str) -> bool:
    """Return True when a URL or its domain appears in the whitelist."""
    domain = extract_domain(url)
    row = fetch_one(
        """
        SELECT id
        FROM whitelist_urls
        WHERE url = ? OR domain = ?
        LIMIT 1
        """,
        (url, domain),
    )
    return row is not None
