"""Flask routes for the initial user-facing pages."""

from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request

from app.services.history_service import get_scan_history, save_scan_result
from app.services.prediction_service import analyze_url
from app.utils.validators import validate_url_input


main_bp = Blueprint("main", __name__)


def _prefers_json_response() -> bool:
    """Return True when the request explicitly prefers JSON output."""
    return request.is_json or request.accept_mimetypes.best == "application/json"


@main_bp.get("/")
def index():
    """Render the landing page with the URL analysis form."""
    return render_template("index.html")


@main_bp.post("/analyze")
def analyze():
    """Handle UI form submissions and JSON requests for URL analysis."""
    payload_url = request.form.get("url", "").strip()

    if request.is_json:
        payload = request.get_json(silent=True) or {}
        payload_url = str(payload.get("url", "")).strip()

    errors = validate_url_input(payload_url)
    if errors:
        if _prefers_json_response():
            return jsonify({"status": "error", "errors": errors}), 400

        return render_template("index.html", errors=errors, submitted_url=payload_url), 400

    result = analyze_url(payload_url)
    save_scan_result(result)
    if _prefers_json_response():
        return jsonify({"status": "success", "data": result}), 200

    return render_template("result.html", result=result)


@main_bp.get("/history")
def history():
    """Render a page showing recent URL scans."""
    records = get_scan_history()

    if _prefers_json_response():
        return jsonify({"status": "success", "data": records}), 200

    return render_template("history.html", records=records)


@main_bp.get("/health")
def health_check():
    """Expose a lightweight health endpoint for local verification."""
    return jsonify({"status": "ok"}), 200
