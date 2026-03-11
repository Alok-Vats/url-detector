BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS reputation_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reputation_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reputation_list_id INTEGER NOT NULL,
    entry_type TEXT NOT NULL CHECK (entry_type IN ('url', 'domain', 'sender_email')),
    raw_value TEXT NOT NULL,
    normalized_value TEXT NOT NULL,
    reason TEXT,
    source TEXT,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reputation_list_id) REFERENCES reputation_lists(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

COMMIT;
