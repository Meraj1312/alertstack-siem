from fastapi import APIRouter
from datetime import datetime
from typing import Optional
from app.db.repository import fetch_events, fetch_alerts
from app.config.settings import settings


router = APIRouter()


@router.get("/metrics")
def get_metrics(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    events = fetch_events(limit=settings.MAX_FETCH_LIMIT, offset=0)
    alerts = fetch_alerts(limit=settings.MAX_FETCH_LIMIT, offset=0)

    if start_time or end_time:
        filtered_events = []
        for e in events:
            event_time = datetime.fromisoformat(e["timestamp"])

            if start_time and event_time < start_time:
                continue
            if end_time and event_time > end_time:
                continue

            filtered_events.append(e)

        events = filtered_events

        filtered_alerts = []
        for a in alerts:
            alert_time = datetime.fromisoformat(a["timestamp"])

            if start_time and alert_time < start_time:
                continue
            if end_time and alert_time > end_time:
                continue

            filtered_alerts.append(a)

        alerts = filtered_alerts

    total_events = len(events)
    total_alerts = len(alerts)

    high_severity_alerts = len([
        a for a in alerts if a.get("severity") in ["high", "critical"]
    ])

    severity_breakdown = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }

    for e in events:
        sev = e.get("risk", {}).get("severity")
        if sev in severity_breakdown:
            severity_breakdown[sev] += 1

    event_type_breakdown = {}

    for e in events:
        etype = e.get("event_type", "unknown")
        event_type_breakdown[etype] = event_type_breakdown.get(etype, 0) + 1

    return {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "high_severity_alerts": high_severity_alerts,
        "severity_breakdown": severity_breakdown,
        "event_type_breakdown": event_type_breakdown
    }