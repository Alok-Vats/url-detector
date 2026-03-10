# Cloud-Based AI System for Phishing URL and Email Detection

This project detects phishing indicators in both URLs and email content using Flask, SQLite, rule-based analysis, and a trained URL classifier.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

Open `http://127.0.0.1:5000`.

## Current scope

- Flask application factory
- SQLite-backed whitelist and blacklist setup
- URL feature extraction and rule-based analysis
- Offline ML training pipeline for phishing URL classification
- Rule-based phishing email analysis
- Saved scan history and demo fixtures
- JSON and HTML responses
- Basic error handling

## Report assets

- `docs/architecture-diagram.md`
- `docs/demo-cases.md`
- `docs/report-assets.md`
- `docs/screenshots/README.md`
