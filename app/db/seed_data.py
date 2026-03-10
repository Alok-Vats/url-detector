"""Seed helpers for inserting starter whitelist and blacklist records."""

from __future__ import annotations

from app.db.database import get_db


def seed_defaults() -> None:
    """Insert a small set of demo rows without duplicating existing records."""
    db = get_db()
    db.execute(
        """
        INSERT OR IGNORE INTO whitelist_urls (url, domain, note)
        VALUES (?, ?, ?)
        """,
        ("https://www.google.com", "www.google.com", "Trusted demo entry"),
    )
    db.execute(
        """
        INSERT OR IGNORE INTO blacklist_urls (url, domain, reason)
        VALUES (?, ?, ?)
        """,
        ("http://secure-login-example.com", "secure-login-example.com", "Known demo phishing entry"),
    )
    db.commit()
