BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS trained_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    input_type TEXT NOT NULL CHECK (input_type IN ('url', 'email')),
    algorithm TEXT NOT NULL,
    artifact_path TEXT NOT NULL,
    accuracy REAL,
    precision_score REAL,
    recall_score REAL,
    f1_score REAL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    trained_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scan_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_type TEXT NOT NULL CHECK (input_type IN ('url', 'email')),
    input_value TEXT NOT NULL,
    normalized_value TEXT NOT NULL,
    prediction_label TEXT NOT NULL CHECK (prediction_label IN ('phishing', 'legitimate')),
    confidence_score REAL NOT NULL CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    model_source TEXT NOT NULL CHECK (
        model_source IN ('whitelist', 'blacklist', 'ml_model', 'heuristic', 'email_rules')
    ),
    trained_model_id INTEGER,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trained_model_id) REFERENCES trained_models(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS scan_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_event_id INTEGER NOT NULL UNIQUE,
    reasons_json TEXT NOT NULL,
    features_json TEXT NOT NULL,
    metadata_json TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_event_id) REFERENCES scan_events(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS scan_list_matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_event_id INTEGER NOT NULL,
    reputation_entry_id INTEGER NOT NULL,
    match_scope TEXT NOT NULL CHECK (match_scope IN ('exact', 'normalized', 'domain')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_event_id) REFERENCES scan_events(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (reputation_entry_id) REFERENCES reputation_entries(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

COMMIT;
