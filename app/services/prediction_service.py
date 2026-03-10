"""High-level orchestration for URL analysis requests."""

from __future__ import annotations

import pandas as pd

from app.ml.feature_extractor import extract_features
from app.ml.model_loader import load_model
from app.services.blacklist_service import get_blacklist_match
from app.services.url_service import inspect_url
from app.services.whitelist_service import get_whitelist_match


def analyze_url(url: str) -> dict:
    """Return an analysis result using list matches, ML inference, or heuristics."""
    details = inspect_url(url)
    whitelist_match = get_whitelist_match(url)
    blacklist_match = get_blacklist_match(url)

    if whitelist_match:
        return _build_response(
            url,
            "legitimate",
            0.99,
            ["Matched trusted whitelist entry."],
            details,
            matched_list="whitelist",
            matched_entry=whitelist_match,
            model_source="whitelist",
        )

    if blacklist_match:
        return _build_response(
            url,
            "phishing",
            0.99,
            ["Matched known blacklist entry."],
            details,
            matched_list="blacklist",
            matched_entry=blacklist_match,
            model_source="blacklist",
        )

    model_result = _predict_with_model(url)
    if model_result is not None:
        prediction = model_result["prediction"]
        confidence = model_result["confidence"]
        reasons = details["reasons"] or ["Prediction generated from the trained URL model."]
        return _build_response(
            url,
            prediction,
            confidence,
            reasons,
            details,
            matched_list=None,
            matched_entry=None,
            model_source="ml_model",
        )

    risk_reasons = details["reasons"]
    if risk_reasons:
        return _build_response(
            url,
            "phishing",
            0.74,
            risk_reasons,
            details,
            matched_list=None,
            model_source="heuristic",
        )

    return _build_response(
        url,
        "legitimate",
        0.81,
        ["No suspicious heuristic flags were detected in the initial scan."],
        details,
        matched_list=None,
        model_source="heuristic",
    )


def _build_response(
    url: str,
    prediction: str,
    confidence: float,
    reasons: list[str],
    details: dict,
    matched_list: str | None,
    model_source: str,
    matched_entry: dict | None = None,
) -> dict:
    """Format response payloads consistently for UI and API consumers."""
    return {
        "url": url,
        "prediction": prediction,
        "confidence": confidence,
        "reasons": reasons,
        "details": details,
        "matched_list": matched_list,
        "model_source": model_source,
        "matched_entry": matched_entry,
    }


def _predict_with_model(url: str) -> dict | None:
    """Run inference using the saved model artifact when available."""
    try:
        model_bundle = load_model()
    except (OSError, ValueError):
        return None

    if model_bundle is None:
        return None

    features = extract_features(url)
    feature_row = pd.DataFrame([features]).reindex(columns=model_bundle["feature_names"], fill_value=0)
    model = model_bundle["model"]

    prediction = str(model.predict(feature_row)[0])
    probability_lookup = {}
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(feature_row)[0]
        probability_lookup = {
            label: float(probability)
            for label, probability in zip(model.classes_, probabilities, strict=False)
        }

    confidence = probability_lookup.get(prediction, 0.5)
    return {"prediction": prediction, "confidence": confidence}
