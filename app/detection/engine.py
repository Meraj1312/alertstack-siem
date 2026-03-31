from app.detection.rules.ato import detect_ato
from app.detection.rules.fraud import detect_fraud
from app.detection.rules.geo import detect_geo
from app.detection.rules.sequence import detect_sequence
from datetime import datetime


RULES = [
    detect_ato,
    detect_fraud,
    detect_geo,
    detect_sequence
]


class DetectionEngine:
    def __init__(self, context):
        self.context = context

    def _parse_time(self, ts):
        if isinstance(ts, str):
            return datetime.fromisoformat(ts)
        return ts

    def run(self, event):
        alerts = []

        for rule in RULES:
            result = rule(event, self.context)
            if result:
                alerts.append(result)

        user = event.get("user_id")
        current_time = self._parse_time(event.get("timestamp"))

        last_ato = self.context.ato_flag.get(user)

        # ✅ Ensure last_ato is datetime
        if isinstance(last_ato, str):
            last_ato = datetime.fromisoformat(last_ato)

        if (
            user
            and isinstance(last_ato, datetime)
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

        # ✅ Dedup
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