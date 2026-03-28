from typing import List, Dict
from datetime import datetime


def export_alerts_to_markdown(alerts: List[Dict]) -> str:
    now = datetime.utcnow().isoformat()

    lines = []
    lines.append("#  AlertStack Incident Report\n")
    lines.append(f"## Summary\n")
    lines.append(f"- Total Alerts: {len(alerts)}")
    lines.append(f"- Generated At: {now}\n")
    lines.append("---\n")

    for i, alert in enumerate(alerts, start=1):
        lines.append(f"## Alert {i}: {alert.get('type', 'unknown').title()}\n")

        lines.append(f"- Alert ID: {alert.get('alert_id')}")
        lines.append(f"- User: {alert.get('user_id')}")
        lines.append(f"- Severity: {str(alert.get('severity')).upper()}")
        lines.append(f"- Confidence: {alert.get('confidence')}\n")

        lines.append("### Reason")
        lines.append(f"{alert.get('reason')}\n")

        lines.append("### MITRE Mapping")
        for m in alert.get("mitre", []):
            lines.append(f"- {m}")
        lines.append("")

        lines.append("### Timestamp")
        lines.append(f"{alert.get('timestamp')}\n")

        lines.append("---\n")

    return "\n".join(lines)