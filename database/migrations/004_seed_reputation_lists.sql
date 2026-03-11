BEGIN TRANSACTION;

INSERT OR IGNORE INTO reputation_lists (list_code, name, description)
VALUES
    ('blacklist', 'Blacklist', 'Known malicious URLs, domains, or senders'),
    ('whitelist', 'Whitelist', 'Trusted URLs, domains, or senders');

COMMIT;
