from typing import List, Dict, Optional
from datetime import datetime

EVENTS: List[Dict] = []
EVENT_IDS = set()


def add_event(event: Dict) -> bool:
    if event["event_id"] in EVENT_IDS:
        return False

    EVENTS.append(event)
    EVENT_IDS.add(event["event_id"])
    return True


def get_all_events() -> List[Dict]:
    return EVENTS


def query_events(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    results = EVENTS.copy()

    if start_time:
        results = [
            e for e in results
            if datetime.fromisoformat(e["timestamp"]) >= start_time
        ]

    if end_time:
        results = [
            e for e in results
            if datetime.fromisoformat(e["timestamp"]) <= end_time
        ]

    if user_id:
        results = [e for e in results if e.get("user_id") == user_id]

    if event_type:
        results = [e for e in results if e.get("event_type") == event_type]

    if severity:
        results = [
            e for e in results
            if e.get("risk", {}).get("severity") == severity
        ]

    results.sort(key=lambda x: x["timestamp"], reverse=True)

    return results