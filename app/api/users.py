from fastapi import APIRouter
from typing import Optional
from datetime import datetime

from app.db.repository import fetch_user_activity

router = APIRouter()


@router.get("/users/{user_id}/activity")
def get_user_activity(
    user_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
):
    events = fetch_user_activity(user_id)

    # oldest → newest (timeline view)
    events = list(reversed(events))

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

    timeline = events[:limit]

    return {
        "user_id": user_id,
        "total_events": len(events),
        "timeline": timeline
    }