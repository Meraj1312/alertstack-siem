from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class RawEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    source_ip: str
    outcome: str
    user_id: Optional[str] = None
    event_data: Dict[str, Any]
    context: Dict[str, Any]