from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class RiskModel(BaseModel):
    score: int
    severity: str
    flags: List[str]


class CorrelationModel(BaseModel):
    signals: List[str] = []
    count: int = 0


class DetectionModel(BaseModel):
    alerts: List[Dict[str, Any]] = []
    flags: List[str] = []
    severity: Optional[str] = None
    confidence: float = 0.0


class EventResponse(BaseModel):
    event_id: str
    timestamp: str
    user_id: Optional[str]
    event_type: str

    risk: RiskModel
    correlation: Optional[CorrelationModel] = None
    detection: Optional[DetectionModel] = None


class EventsAPIResponse(BaseModel):
    total: int
    filters_applied: Dict[str, Any]
    events: List[EventResponse]