def detect_fraud(event, context):
    if event.get("event_type") != "transaction":
        return None

    user = event.get("user_id")
    if not user:
        return None

    amount = event.get("event_data", {}).get("amount", 0)
    current_time = event.get("timestamp")

    recent = context.get_recent_transactions(user, 300, current_time)

    count = context.transaction_counts[user]
    if count > 1:
        avg = (context.transaction_totals[user] - amount) / (count - 1)
    else:
        avg = 0

    alerts = []

    if len(recent) >= 5:
        alerts.append({
            "type": "FRAUD_VELOCITY",
            "severity": "high",
            "confidence": 80,
            "reason": f"{len(recent)} transactions within 5 minutes",
            "mitre": "T1499"
        })

    if avg > 0 and amount > (avg * 3):
        alerts.append({
            "type": "FRAUD_ANOMALY",
            "severity": "high",
            "confidence": 85,
            "reason": f"Transaction {amount} vs user avg {round(avg, 2)}",
            "mitre": "T1499"
        })

    if alerts:
        return alerts[0]  # keep system simple

    return None