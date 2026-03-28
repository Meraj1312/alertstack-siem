from typing import List, Optional
from pydantic import BaseModel


class AlertModel(BaseModel):
    alert_id: str
    timestamp: str
    user_id: Optional[str]

    type: str

    severity: Optional[str]
    confidence: float

    reason: str
    mitre: List[str]

    event_id: str


class AlertsAPIResponse(BaseModel):
    total: int
    alerts: List[AlertModel]