"""Persistence helpers for scan history records."""

from __future__ import annotations

import json

from app.db.database import execute_query, fetch_all


def save_scan_result(result: dict) -> None:
    """Persist a completed scan result for later review."""
    details = result.get("details", {})
    input_type = result.get("input_type", "url")
    input_value = result.get("url") if input_type == "url" else result.get("sender", "")
    normalized_value = (
        details.get("normalized_url", input_value)
        if input_type == "url"
        else details.get("normalized_sender", input_value)
    )
    execute_query(
        """
        INSERT INTO scan_history (
            input_type,
            input_value,
            normalized_value,
            prediction,
            confidence,
            matched_list,
            model_source,
            reasons,
            features
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            input_type,
            input_value,
            normalized_value,
            result["prediction"],
            float(result["confidence"]),
            result.get("matched_list"),
            result.get("model_source", "heuristic"),
            json.dumps(result.get("reasons", [])),
            json.dumps(details.get("features", {})),
        ),
    )


def get_scan_history(limit: int = 20) -> list[dict]:
    """Return recent scan history records ordered by newest first."""
    safe_limit = max(1, min(limit, 100))
    rows = fetch_all(
        """
        SELECT
            id,
            input_type,
            input_value,
            normalized_value,
            prediction,
            confidence,
            matched_list,
            model_source,
            reasons,
            features,
            created_at
        FROM scan_history
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (safe_limit,),
    )

    records: list[dict] = []
    for row in rows:
        record = dict(row)
        record["reasons"] = json.loads(record["reasons"])
        record["features"] = json.loads(record["features"])
        records.append(record)

    return records
