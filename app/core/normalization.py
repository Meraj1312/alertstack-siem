from datetime import datetime, UTC
from app.schemas.event_schema import RawEvent

EVENT_CATEGORY_MAP = {
    "login": "authentication",
    "login_success": "authentication",
    "login_failed": "authentication",
    "logout": "authentication",
    "password_change": "authentication",
    "transaction": "financial",
    "payment": "financial",
    "transfer": "financial",
    "api_call": "system",
    "file_access": "system",
}


def normalize_event(raw_event: RawEvent) -> dict:
    normalized_type = raw_event.event_type.lower()

    event_category = EVENT_CATEGORY_MAP.get(
        normalized_type,
        "unknown"
    )

    return {
        "event_id": raw_event.event_id,
        "event_type": normalized_type,
        "event_category": event_category,
        "timestamp": raw_event.timestamp,
        "source_ip": raw_event.source_ip,
        "outcome": raw_event.outcome,
        "user_id": raw_event.user_id,
        "event_data": raw_event.event_data,
        "context": raw_event.context,

        "ingested_at": datetime.now(UTC),
        "schema_version": "1.0"
    }