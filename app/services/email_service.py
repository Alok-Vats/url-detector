"""Rule-based email phishing detection service."""

from __future__ import annotations

from app.ml.email_feature_extractor import extract_email_features, extract_urls_from_email


def analyze_email_content(sender: str, subject: str, body: str) -> dict:
    """Analyze email content using deterministic phishing rules."""
    features = extract_email_features(sender, subject, body)
    reasons = _build_reasons(features)
    linked_urls = extract_urls_from_email(body)
    risk_score = _calculate_risk_score(features)

    if risk_score >= 4:
        prediction = "phishing"
        confidence = min(0.95, 0.55 + (risk_score * 0.08))
    else:
        prediction = "legitimate"
        confidence = max(0.55, 0.88 - (risk_score * 0.07))

    if not reasons:
        reasons.append("No high-risk phishing indicators were detected in the email content.")

    return {
        "input_type": "email",
        "sender": sender.strip(),
        "subject": subject.strip(),
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "reasons": reasons,
        "matched_list": None,
        "matched_entry": None,
        "model_source": "email_rules",
        "details": {
            "normalized_sender": sender.strip().lower(),
            "subject": subject.strip(),
            "body_preview": body.strip()[:180],
            "linked_urls": linked_urls,
            "features": features,
        },
    }


def _calculate_risk_score(features: dict) -> int:
    """Aggregate rule triggers into a simple phishing risk score."""
    return int(
        features["contains_urgent_language"]
        + features["contains_suspicious_keyword"]
        + features["contains_attachment_hint"]
        + features["contains_html_link"]
        + features["contains_reply_to_mismatch_hint"]
        + features["display_name_mismatch_hint"]
        + (2 if features["url_count"] >= 2 else 0)
        + (1 if features["body_length"] < 40 else 0)
    )


def _build_reasons(features: dict) -> list[str]:
    """Translate triggered feature flags into human-readable reasons."""
    reasons: list[str] = []
    if features["contains_urgent_language"]:
        reasons.append("Email uses urgent or action-forcing language.")
    if features["contains_suspicious_keyword"]:
        reasons.append("Email contains phishing-associated keywords.")
    if features["url_count"] >= 1:
        reasons.append("Email contains one or more embedded URLs.")
    if features["contains_html_link"]:
        reasons.append("Email body appears to contain HTML links.")
    if features["contains_attachment_hint"]:
        reasons.append("Email references an attachment or executable-like file.")
    if features["display_name_mismatch_hint"]:
        reasons.append("Sender field includes a display name and mailbox combination.")
    if features["contains_reply_to_mismatch_hint"]:
        reasons.append("Email references a reply-to instruction that may hide the real sender.")
    return reasons
