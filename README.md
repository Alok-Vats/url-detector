# Cloud-Based AI System for Phishing URL and Email Detection

Phase 1 provides the initial Flask setup, SQLite configuration, and a simple web UI for URL checking.

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
- Simple URL analysis form
- JSON and HTML responses
- Basic error handling
