from datetime import datetime
from typing import List, Optional


def filter_events(
    events: List[dict],
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    filtered = events

    if start_time:
        filtered = [
            e for e in filtered
            if datetime.fromisoformat(e["timestamp"]) >= start_time
        ]

    if end_time:
        filtered = [
            e for e in filtered
            if datetime.fromisoformat(e["timestamp"]) <= end_time
        ]

    if user_id:
        filtered = [e for e in filtered if e.get("user_id") == user_id]

    if event_type:
        filtered = [e for e in filtered if e.get("event_type") == event_type]

    if severity:
        filtered = [
            e for e in filtered
            if e.get("risk", {}).get("severity") == severity
        ]

    filtered.sort(key=lambda x: x["timestamp"], reverse=True)

    return filtered