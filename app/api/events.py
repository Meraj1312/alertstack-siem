from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
from app.db.repository import fetch_events
from app.config.settings import settings

router = APIRouter()


@router.get("/events")
def get_events(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = settings.DEFAULT_LIMIT,
    offset: int = 0,
):
    if start_time and end_time and start_time > end_time:
        return {"total": 0, "events": []}

    events = fetch_events(
        user_id=user_id,
        event_type=event_type,
        severity=severity,
        limit=limit,
        offset=offset
    )

    if start_time or end_time:
        filtered = []

        for event in events:
            event_time = datetime.fromisoformat(event["timestamp"])

            if start_time and event_time < start_time:
                continue
            if end_time and event_time > end_time:
                continue

            filtered.append(event)

        events = filtered

    return {
        "total": len(events),
        "filters": {
            "user_id": user_id,
            "event_type": event_type,
            "severity": severity
        },
        "events": events
    }