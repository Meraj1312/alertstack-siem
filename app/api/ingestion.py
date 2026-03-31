from fastapi import APIRouter, HTTPException
from app.schemas.event_schema import RawEvent
from app.core.normalization import normalize_event
from app.risk.engine import RiskEngine
from app.risk.config import PolicyManager
from app.correlation.engine import CorrelationEngine
from app.detection.engine import DetectionEngine
from app.detection.context import DetectionContext
from app.db.repository import save_event
from app.config.settings import settings


router = APIRouter()

policy_manager = PolicyManager(settings.POLICY_PATH)
policy_manager.load_policy()

risk_engine = RiskEngine(policy_manager)
correlation_engine = CorrelationEngine()

detection_context = DetectionContext()
detection_engine = DetectionEngine(detection_context)


@router.post("/ingest")
def ingest_event(event: RawEvent):
    raw_event_dict = event.model_dump()

    normalized_event = normalize_event(event)

    enriched_event = risk_engine.apply(normalized_event)

    correlated_event = correlation_engine.apply(enriched_event)

    detection_context.add_event(correlated_event)
    detection_result = detection_engine.run(correlated_event)

    correlated_event["detection"] = detection_result
    correlated_event["raw"] = raw_event_dict


    try:
        save_event(correlated_event)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to store event: {str(e)}"
        )
    return {
        "status": "success",
        "message": "Event ingested successfully",
        "event_id": event.event_id,
        "risk": correlated_event["risk"],
        "correlation": correlated_event.get("correlation", None),
        "detection": correlated_event["detection"]
    }

@router.get("/events/flat")
def get_events_flat():
    data = get_all_events()
    return data["events"]