from typing import List, Dict


def build_alerts_from_events(events: List[Dict]) -> List[Dict]:
    alerts = []

    for event in events:
        detection = event.get("detection", {})

        if not detection:
            continue

        detection_alerts = detection.get("alerts", [])

        for alert in detection_alerts:
            alert_obj = {
                "alert_id": f"{event['event_id']}::{alert.get('type', 'unknown')}",
                "timestamp": event.get("timestamp"),
                "user_id": event.get("user_id"),

                "type": alert.get("type", "unknown"),

                "severity": detection.get("severity"),
                "confidence": detection.get("confidence", 0.0),

                "reason": alert.get("reason", "No reason provided"),
                "mitre": alert.get("mitre", []),

                "event_id": event.get("event_id"),
            }

            alerts.append(alert_obj)

    # Sort newest first
    alerts.sort(key=lambda x: x["timestamp"], reverse=True)

    return alerts