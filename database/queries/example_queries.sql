-- 1. Insert a blacklist URL entry
INSERT INTO reputation_entries (
    reputation_list_id,
    entry_type,
    raw_value,
    normalized_value,
    reason,
    source
)
SELECT
    rl.id,
    'url',
    'http://secure-login-example.com',
    'http://secure-login-example.com/',
    'Known phishing landing page',
    'manual_review'
FROM reputation_lists rl
WHERE rl.list_code = 'blacklist';

-- 2. Find whether a normalized URL exists in blacklist or whitelist
SELECT
    rl.list_code,
    re.id,
    re.entry_type,
    re.normalized_value,
    re.reason
FROM reputation_entries re
JOIN reputation_lists rl
    ON rl.id = re.reputation_list_id
WHERE re.normalized_value = 'https://www.google.com/'
  AND re.is_active = 1;

-- 3. Record a URL scan event
INSERT INTO scan_events (
    input_type,
    input_value,
    normalized_value,
    prediction_label,
    confidence_score,
    model_source,
    trained_model_id
)
VALUES (
    'url',
    'http://verify-bank-account.example.net/update',
    'http://verify-bank-account.example.net/update',
    'phishing',
    0.91,
    'ml_model',
    1
);

-- 4. Add scan details for the last scan
INSERT INTO scan_details (
    scan_event_id,
    reasons_json,
    features_json,
    metadata_json
)
VALUES (
    1,
    '["URL contains phishing-associated keywords.","URL does not use HTTPS."]',
    '{"url_length":48,"uses_https":0,"contains_suspicious_keyword":1}',
    '{"hostname":"verify-bank-account.example.net","scheme":"http"}'
);

-- 5. Link a scan to the reputation entry that matched
INSERT INTO scan_list_matches (
    scan_event_id,
    reputation_entry_id,
    match_scope
)
VALUES (1, 3, 'exact');

-- 6. Fetch recent phishing scans with associated model version
SELECT
    se.id,
    se.input_type,
    se.normalized_value,
    se.prediction_label,
    se.confidence_score,
    se.model_source,
    tm.model_name,
    tm.model_version,
    se.created_at
FROM scan_events se
LEFT JOIN trained_models tm
    ON tm.id = se.trained_model_id
WHERE se.prediction_label = 'phishing'
ORDER BY se.created_at DESC
LIMIT 10;

-- 7. Fetch complete details for a scan
SELECT
    se.id,
    se.input_type,
    se.input_value,
    se.prediction_label,
    se.confidence_score,
    sd.reasons_json,
    sd.features_json,
    sd.metadata_json
FROM scan_events se
JOIN scan_details sd
    ON sd.scan_event_id = se.id
WHERE se.id = 1;

-- 8. Count scans by day and label
SELECT
    DATE(created_at) AS scan_day,
    prediction_label,
    COUNT(*) AS total_scans
FROM scan_events
GROUP BY DATE(created_at), prediction_label
ORDER BY scan_day DESC, prediction_label;
