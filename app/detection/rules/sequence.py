from datetime import datetime


def detect_sequence(event, context):
    user = event.get("user_id")

    timestamp = event.get("timestamp")

    if isinstance(timestamp, str):
        current_time = datetime.fromisoformat(timestamp)
    else:
        current_time = timestamp

    recent_logins = context.get_recent_logins(user, 600, current_time)
    recent_tx = context.get_recent_transactions(user, 600, current_time)

    if len(recent_logins) >= 3 and len(recent_tx) >= 1:
        return {
            "type": "suspicious_sequence",
            "severity": "high",
            "confidence": 0.8,
            "reason": "Multiple logins followed by transaction"
        }

    return None