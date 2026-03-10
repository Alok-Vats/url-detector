"""SQLite database utilities for the Flask app."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import current_app, g


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS blacklist_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    domain TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS whitelist_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    domain TEXT NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def get_db() -> sqlite3.Connection:
    """Return a request-scoped SQLite connection."""
    if "db" not in g:
        db_path = Path(current_app.config["DATABASE_PATH"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None) -> None:
    """Close the current request's database connection if one exists."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Create the initial database schema."""
    db = get_db()
    db.executescript(SCHEMA_SQL)
    db.commit()


def init_app(app) -> None:
    """Register CLI-like hooks for automatic database initialization."""

    @app.before_request
    def ensure_database_ready():
        """Make sure the schema exists before handling a request."""
        init_db()


def fetch_one(query: str, params: tuple = ()) -> sqlite3.Row | None:
    """Fetch a single row from the database."""
    cursor = get_db().execute(query, params)
    row = cursor.fetchone()
    cursor.close()
    return row
