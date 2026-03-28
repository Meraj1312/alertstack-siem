from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
from app.db.repository import fetch_alerts
from app.schemas.alert_response import AlertsAPIResponse
from app.config.settings import settings


router = APIRouter()


@router.get("/alerts", response_model=AlertsAPIResponse)
def get_alerts(
    user_id: Optional[str] = None,
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = settings.DEFAULT_LIMIT,
    offset: int = 0,
):
    alerts = fetch_alerts(limit=limit, offset=offset)

    filtered = []

    for alert in alerts:
        if user_id and alert.get("user_id") != user_id:
            continue

        if severity and alert.get("severity") != severity:
            continue

        if start_time or end_time:
            event_time = datetime.fromisoformat(alert["timestamp"])

            if start_time and event_time < start_time:
                continue
            if end_time and event_time > end_time:
                continue

        filtered.append(alert)

    paginated = filtered[offset: offset + limit]

    return {
        "total": len(filtered),
        "alerts": paginated
    }