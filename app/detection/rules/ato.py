def detect_ato(event, context):
    if event.get("event_type") != "login_success":
        return None

    user = event.get("user_id")
    if not user:
        return None

    current_time = event.get("timestamp")
    recent = context.get_recent_logins(user, 300, current_time)

    failed_attempts = [e for e in recent if e[0] == "login_failed"]

    if len(failed_attempts) >= 5:
        context.ato_flag[user] = True

        return {
            "type": "ATO",
            "severity": "high",
            "confidence": 85,
            "reason": f"{len(failed_attempts)} failed logins followed by success",
            "mitre": "T1110"
        }

    return None