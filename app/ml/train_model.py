"""Training pipeline for the phishing URL classifier."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from app.ml.preprocess import build_feature_frame, load_dataset


DEFAULT_RANDOM_STATE = 42


def train_and_save_model(
    dataset_path: str | Path,
    model_output_path: str | Path,
    metrics_output_path: str | Path,
) -> dict:
    """Train the phishing URL model, evaluate it, and persist the artifacts."""
    dataset = load_dataset(dataset_path)
    features, labels = build_feature_frame(dataset)

    if labels.nunique() < 2:
        raise ValueError("Training requires at least two label classes.")

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.25,
        random_state=DEFAULT_RANDOM_STATE,
        stratify=labels,
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        min_samples_split=2,
        random_state=DEFAULT_RANDOM_STATE,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, pos_label="phishing")), 4),
        "recall": round(float(recall_score(y_test, predictions, pos_label="phishing")), 4),
        "f1_score": round(float(f1_score(y_test, predictions, pos_label="phishing")), 4),
        "train_size": int(len(x_train)),
        "test_size": int(len(x_test)),
        "feature_count": int(features.shape[1]),
    }

    model_bundle = {
        "model": model,
        "feature_names": list(features.columns),
        "labels": sorted(labels.unique().tolist()),
    }
    _save_artifacts(model_bundle, metrics, model_output_path, metrics_output_path)
    return metrics


def _save_artifacts(
    model_bundle: dict,
    metrics: dict,
    model_output_path: str | Path,
    metrics_output_path: str | Path,
) -> None:
    """Persist trained model and evaluation metrics to disk."""
    model_path = Path(model_output_path)
    metrics_path = Path(metrics_output_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model_bundle, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    metrics = train_and_save_model(
        dataset_path=BASE_DIR / "data" / "raw" / "phishing_urls.csv",
        model_output_path=BASE_DIR / "models" / "phishing_url_model.pkl",
        metrics_output_path=BASE_DIR / "models" / "phishing_url_model_metrics.json",
    )
    print(json.dumps(metrics, indent=2))
