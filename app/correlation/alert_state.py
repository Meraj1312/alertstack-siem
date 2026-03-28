from datetime import datetime, timedelta
from typing import Dict


class AlertState:

    def __init__(self):

        self._state: Dict[str, datetime] = {}

    def _build_key(self, user_id: str, rule_id: str) -> str:
        return f"{user_id}:{rule_id}"

    def has_triggered_recently(
        self,
        user_id: str,
        rule_id: str,
        current_event: dict,
        window_seconds: int
    ) -> bool:

        key = self._build_key(user_id, rule_id)

        if key not in self._state:
            return False

        last_triggered = self._state[key]

        current_time = current_event.get("timestamp")

        if not current_time:
            return False

        return (current_time - last_triggered) <= timedelta(seconds=window_seconds)

    def mark_triggered(
        self,
        user_id: str,
        rule_id: str,
        current_event: dict
    ):

        key = self._build_key(user_id, rule_id)

        event_time = current_event.get("timestamp")

        if not event_time:
            event_time = datetime.utcnow()  # fallback safety

        self._state[key] = event_time

    def get_state(self) -> Dict[str, datetime]:
        return self._state