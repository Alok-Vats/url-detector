"""Helpers for safely extracting URL components."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class ParsedUrl:
    """Normalized URL parts reused across the analysis pipeline."""

    original: str
    normalized: str
    scheme: str
    netloc: str
    hostname: str
    path: str
    query: str


def normalize_url(url: str) -> str:
    """Return a canonical representation of a submitted URL."""
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    query = f"?{parsed.query}" if parsed.query else ""
    return f"{scheme}://{netloc}{path}{query}"


def parse_url(url: str) -> ParsedUrl:
    """Parse a raw URL into normalized reusable components."""
    parsed = urlparse(url.strip())
    return ParsedUrl(
        original=url,
        normalized=normalize_url(url),
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        hostname=(parsed.hostname or "").lower(),
        path=parsed.path or "/",
        query=parsed.query,
    )


def extract_domain(url: str) -> str:
    """Return the lower-cased hostname from a URL."""
    return parse_url(url).hostname
