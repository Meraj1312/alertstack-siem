FAKE_IP_MAP = {
    "1.1.1.1": "IN",
    "2.2.2.2": "US",
    "3.3.3.3": "UK"
}


def detect_geo(event, context):
    if event.get("event_type") != "login_success":
        return None

    user = event.get("user_id")
    if not user:
        return None

    ip = event.get("source_ip")
    if not ip:
        return None

    current_location = FAKE_IP_MAP.get(ip)
    last_location = context.last_location.get(user)

    if current_location:
        context.last_location[user] = current_location

    if last_location and current_location and last_location != current_location:
        return {
            "type": "IMPOSSIBLE_TRAVEL",
            "severity": "high",
            "confidence": 90,
            "reason": f"Login from {last_location} to {current_location}",
            "mitre": "T1078"
        }

    return None