"""Seed helpers for inserting starter whitelist and blacklist records."""

from __future__ import annotations

from app.db.database import get_db
from app.utils.url_parser import extract_domain, normalize_url


def seed_defaults() -> None:
    """Insert a small set of demo rows without duplicating existing records."""
    db = get_db()
    trusted_url = "https://www.google.com"
    known_bad_url = "http://secure-login-example.com"
    db.execute(
        """
        INSERT OR IGNORE INTO whitelist_urls (url, domain, note)
        VALUES (?, ?, ?)
        """,
        (normalize_url(trusted_url), extract_domain(trusted_url), "Trusted demo entry"),
    )
    db.execute(
        """
        INSERT OR IGNORE INTO blacklist_urls (url, domain, reason)
        VALUES (?, ?, ?)
        """,
        (
            normalize_url(known_bad_url),
            extract_domain(known_bad_url),
            "Known demo phishing entry",
        ),
    )
    db.commit()
