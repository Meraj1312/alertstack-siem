from app.detection.rules.ato import detect_ato
from app.detection.rules.fraud import detect_fraud
from app.detection.rules.geo import detect_geo
from app.detection.rules.sequence import detect_sequence


RULES = [
    detect_ato,
    detect_fraud,
    detect_geo,
    detect_sequence
]


class DetectionEngine:
    def __init__(self, context):
        self.context = context

    def run(self, event):
        alerts = []

        for rule in RULES:
            result = rule(event, self.context)
            if result:
                alerts.append(result)

        # 🔥 Cross-event escalation (correct version)
        user = event.get("user_id")
        current_time = event.get("timestamp")

        last_ato = self.context.ato_flag.get(user)

        if (
            user
            and last_ato
            and current_time
            and (current_time - last_ato).seconds <= 600
            and event.get("event_type") == "transaction"
        ):
            alerts.append({
                "type": "ATO_FRAUD_COMBO",
                "severity": "critical",
                "confidence": 95,
                "reason": "Transaction within 10 minutes of suspected account takeover",
                "mitre": "T1078"
            })

        seen = set()
        unique_alerts = []

        for a in alerts:
            if a["type"] not in seen:
                unique_alerts.append(a)
                seen.add(a["type"])

        alerts = unique_alerts

        return {
            "alerts": alerts,
            "flags": [a["type"] for a in alerts],
            "severity": self._max_severity(alerts),
            "confidence": self._avg_confidence(alerts)
        }

    def _max_severity(self, alerts):
        order = ["low", "medium", "high", "critical"]
        if not alerts:
            return "low"
        return max(alerts, key=lambda x: order.index(x["severity"]))["severity"]

    def _avg_confidence(self, alerts):
        if not alerts:
            return 0
        return int(sum(a["confidence"] for a in alerts) / len(alerts))