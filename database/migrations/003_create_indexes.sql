BEGIN TRANSACTION;

CREATE UNIQUE INDEX IF NOT EXISTS idx_reputation_entries_unique
    ON reputation_entries (reputation_list_id, entry_type, normalized_value);

CREATE INDEX IF NOT EXISTS idx_reputation_entries_normalized_value
    ON reputation_entries (normalized_value);

CREATE UNIQUE INDEX IF NOT EXISTS idx_trained_models_name_version
    ON trained_models (model_name, model_version);

CREATE INDEX IF NOT EXISTS idx_trained_models_input_type_active
    ON trained_models (input_type, is_active);

CREATE INDEX IF NOT EXISTS idx_scan_events_input_type_created_at
    ON scan_events (input_type, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_scan_events_prediction_created_at
    ON scan_events (prediction_label, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_scan_events_trained_model_id
    ON scan_events (trained_model_id);

CREATE INDEX IF NOT EXISTS idx_scan_details_scan_event_id
    ON scan_details (scan_event_id);

CREATE INDEX IF NOT EXISTS idx_scan_list_matches_scan_event_id
    ON scan_list_matches (scan_event_id);

CREATE INDEX IF NOT EXISTS idx_scan_list_matches_reputation_entry_id
    ON scan_list_matches (reputation_entry_id);

COMMIT;
