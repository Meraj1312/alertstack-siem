from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime

from app.core.event_store import query_events
from app.core.alert_builder import build_alerts_from_events
from app.reporting.exporter import export_alerts_to_markdown

router = APIRouter()


@router.get("/reports/alerts")
def export_alerts_report(
    user_id: Optional[str] = None,
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    format: str = "json",
):
    events = query_events(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
    )

    alerts = build_alerts_from_events(events)

    if severity:
        alerts = [a for a in alerts if a.get("severity") == severity]

    if format == "markdown":
        report = export_alerts_to_markdown(alerts)
        return {"report": report}

    return {
        "total": len(alerts),
        "alerts": alerts
    }