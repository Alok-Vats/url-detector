"""Tests that validate the documented demo cases used in the project report."""

import json
from pathlib import Path

from app import create_app
from app.db.seed_data import seed_defaults
from app.services.email_service import analyze_email_content
from app.services.prediction_service import analyze_url


def test_documented_demo_cases_are_stable():
    demo_cases = json.loads(Path("tests/fixtures/demo_cases.json").read_text(encoding="utf-8"))
    app = create_app("testing")

    with app.app_context():
        seed_defaults()

        for case in demo_cases["url_cases"]:
            result = analyze_url(case["input"])
            assert result["prediction"] == case["expected_prediction"]

    for case in demo_cases["email_cases"]:
        result = analyze_email_content(case["sender"], case["subject"], case["body"])
        assert result["prediction"] == case["expected_prediction"]
