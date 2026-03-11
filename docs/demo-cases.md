# Demo Cases

These cases are stored in [tests/fixtures/demo_cases.json](/home/user/Desktop/mProject/tests/fixtures/demo_cases.json) and validated by automated tests.

## URL cases

1. `https://www.google.com`
   Expected: `legitimate`
   Reason: trusted whitelist example

2. `http://secure-login-example.com`
   Expected: `phishing`
   Reason: known blacklist example

3. `http://very-secure-login-update.example.com`
   Expected: `phishing`
   Reason: suspicious lexical patterns

## Email cases

1. Sender: `alerts@fake-bank.example`
   Subject: `Urgent account verification`
   Expected: `phishing`
   Reason: urgent language, suspicious URL, attachment hint, and reply-to mismatch cue

2. Sender: `events@college.edu`
   Subject: `Workshop schedule for tomorrow`
   Expected: `legitimate`
   Reason: normal academic communication without phishing indicators
