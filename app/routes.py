"""Flask routes for the initial user-facing pages."""

from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request

from app.services.prediction_service import analyze_url
from app.utils.validators import validate_url_input


main_bp = Blueprint("main", __name__)


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
        if request.is_json:
            return jsonify({"status": "error", "errors": errors}), 400

        return render_template("index.html", errors=errors, submitted_url=payload_url), 400

    result = analyze_url(payload_url)
    if request.is_json:
        return jsonify({"status": "success", "data": result}), 200

    return render_template("result.html", result=result)


@main_bp.get("/health")
def health_check():
    """Expose a lightweight health endpoint for local verification."""
    return jsonify({"status": "ok"}), 200
