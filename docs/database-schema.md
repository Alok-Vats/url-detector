# Database Schema

This document defines a normalized SQLite schema for the phishing URL and email detection project. It is designed as a target schema for production-style data management and reporting.

## Design goals

- keep blacklist and whitelist data in a single normalized reputation-entry model
- support both URL and email scans
- track which saved ML model produced a prediction
- separate scan metadata from scan details and list matches
- keep reporting queries efficient with explicit indexes

## Tables

### `reputation_lists`

Stores the types of curated reputation lists used by the system.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Surrogate key |
| `list_code` | `TEXT` | `NOT NULL UNIQUE` | Stable code such as `blacklist` or `whitelist` |
| `name` | `TEXT` | `NOT NULL` | Human-readable list name |
| `description` | `TEXT` | `NULL` | Optional description |
| `created_at` | `DATETIME` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Creation timestamp |

### `reputation_entries`

Stores normalized URL, domain, or sender records inside a list.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Surrogate key |
| `reputation_list_id` | `INTEGER` | `NOT NULL FK` | References `reputation_lists.id` |
| `entry_type` | `TEXT` | `NOT NULL` | `url`, `domain`, or `sender_email` |
| `raw_value` | `TEXT` | `NOT NULL` | Original submitted value |
| `normalized_value` | `TEXT` | `NOT NULL` | Canonical comparison value |
| `reason` | `TEXT` | `NULL` | Why the entry exists |
| `source` | `TEXT` | `NULL` | Optional source feed or admin note |
| `is_active` | `INTEGER` | `NOT NULL DEFAULT 1` | Soft-active flag |
| `created_at` | `DATETIME` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Creation timestamp |
| `updated_at` | `DATETIME` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Last update timestamp |

### `trained_models`

Stores model version and evaluation metadata.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Surrogate key |
| `model_name` | `TEXT` | `NOT NULL` | For example `phishing_url_classifier` |
| `model_version` | `TEXT` | `NOT NULL` | Semantic or timestamp version |
| `input_type` | `TEXT` | `NOT NULL` | `url` or `email` |
| `algorithm` | `TEXT` | `NOT NULL` | For example `RandomForestClassifier` |
| `artifact_path` | `TEXT` | `NOT NULL` | Saved artifact path |
| `accuracy` | `REAL` | `NULL` | Evaluation metric |
| `precision_score` | `REAL` | `NULL` | Evaluation metric |
| `recall_score` | `REAL` | `NULL` | Evaluation metric |
| `f1_score` | `REAL` | `NULL` | Evaluation metric |
| `is_active` | `INTEGER` | `NOT NULL DEFAULT 1` | Active model flag |
| `trained_at` | `DATETIME` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Training timestamp |

### `scan_events`

Stores the main prediction record for each scan request.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Surrogate key |
| `input_type` | `TEXT` | `NOT NULL` | `url` or `email` |
| `input_value` | `TEXT` | `NOT NULL` | Original submitted content |
| `normalized_value` | `TEXT` | `NOT NULL` | Canonical comparison value |
| `prediction_label` | `TEXT` | `NOT NULL` | `phishing` or `legitimate` |
| `confidence_score` | `REAL` | `NOT NULL` | Probability or rule confidence |
| `model_source` | `TEXT` | `NOT NULL` | `whitelist`, `blacklist`, `ml_model`, `heuristic`, `email_rules` |
| `trained_model_id` | `INTEGER` | `NULL FK` | References `trained_models.id` |
| `created_at` | `DATETIME` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Scan timestamp |

### `scan_details`

Stores JSON detail payloads separately from the main scan row.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Surrogate key |
| `scan_event_id` | `INTEGER` | `NOT NULL UNIQUE FK` | References `scan_events.id` |
| `reasons_json` | `TEXT` | `NOT NULL` | JSON array of human-readable reasons |
| `features_json` | `TEXT` | `NOT NULL` | JSON object of extracted features |
| `metadata_json` | `TEXT` | `NULL` | Additional structured details |
| `created_at` | `DATETIME` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Creation timestamp |

### `scan_list_matches`

Stores one or more reputation-list matches for a scan.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Surrogate key |
| `scan_event_id` | `INTEGER` | `NOT NULL FK` | References `scan_events.id` |
| `reputation_entry_id` | `INTEGER` | `NOT NULL FK` | References `reputation_entries.id` |
| `match_scope` | `TEXT` | `NOT NULL` | `exact`, `normalized`, or `domain` |
| `created_at` | `DATETIME` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Match timestamp |

## Relationships

- `reputation_lists` 1-to-many `reputation_entries`
- `trained_models` 1-to-many `scan_events`
- `scan_events` 1-to-1 `scan_details`
- `scan_events` 1-to-many `scan_list_matches`
- `reputation_entries` 1-to-many `scan_list_matches`

## Index strategy

- `reputation_lists.list_code` unique lookup index
- `reputation_entries(reputation_list_id, entry_type, normalized_value)` unique index
- `reputation_entries(normalized_value)` search index
- `trained_models(model_name, model_version)` unique index
- `trained_models(input_type, is_active)` filter index
- `scan_events(input_type, created_at DESC)` reporting index
- `scan_events(prediction_label, created_at DESC)` reporting index
- `scan_events(trained_model_id)` join index
- `scan_list_matches(scan_event_id)` join index
- `scan_list_matches(reputation_entry_id)` join index

## Normalization notes

- blacklist and whitelist are not separate tables; they are values in `reputation_lists`
- detailed scan JSON is moved out of `scan_events` into `scan_details`
- list matches are modeled as a proper junction table instead of a single text column
- model metrics are stored once per trained model version
