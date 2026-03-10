"""Utilities for loading a trained phishing URL model safely."""

from __future__ import annotations

from pathlib import Path

import joblib
from flask import current_app


def load_model(model_path: str | None = None) -> dict | None:
    """Load a saved model bundle and return None when no artifact exists."""
    resolved_path = Path(model_path or current_app.config["MODEL_PATH"])
    if not resolved_path.exists():
        return None

    model_bundle = joblib.load(resolved_path)
    if not isinstance(model_bundle, dict):
        raise ValueError("Model artifact format is invalid.")

    required_keys = {"model", "feature_names", "labels"}
    missing = required_keys - set(model_bundle.keys())
    if missing:
        missing_keys = ", ".join(sorted(missing))
        raise ValueError(f"Model artifact is missing keys: {missing_keys}")

    return model_bundle
