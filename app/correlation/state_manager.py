from datetime import timedelta
from typing import List, Dict
from app.core.event_store import get_all_events


class StateManager:

    def __init__(self):
        pass

    def get_events_by_user_and_type(
        self,
        user_id: str,
        event_type: str,
        current_event: Dict,
        window_seconds: int
    ) -> List[Dict]:

        events = get_all_events()
        result = []

        current_time = current_event["timestamp"]

        for event in events:
            if event.get("user_id") != user_id:
                continue

            if event.get("event_type") != event_type:
                continue

            event_time = event.get("timestamp")

            if not event_time:
                continue

            # Time window check
            if current_time - event_time <= timedelta(seconds=window_seconds):
                result.append(event)

        return result