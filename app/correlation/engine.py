from datetime import datetime, UTC
import logging
from typing import Dict

from app.correlation.state_manager import StateManager
from app.correlation.alert_state import AlertState
from app.correlation.rules import detect_bruteforce, detect_transaction_spike

logger = logging.getLogger(__name__)

RULES = [
    detect_bruteforce,
    detect_transaction_spike
]


class CorrelationEngine:

    def __init__(self):
        self.state_manager = StateManager()
        self.alert_state = AlertState()

    def apply(self, event: Dict) -> Dict:

        try:
            behavioral_score = 0
            flags = []
            matched_rules = []
            mitre_matches = []
            contexts = []

            for rule in RULES:
                result = rule(event, self.state_manager)

                if not result:
                    continue

                user_id = event.get("user_id")
                rule_id = result["rule_id"]

                window_seconds = result.get("context", {}).get("window_seconds", 300)

                already_triggered = self.alert_state.has_triggered_recently(
                    user_id=user_id,
                    rule_id=rule_id,
                    current_event=event,
                    window_seconds=window_seconds
                )

                if not already_triggered:
                    behavioral_score += result["behavioral_score"]
                    flags.append(result["flag"])
                    matched_rules.append(rule_id)

                    # MITRE mapping
                    mitre_data = result.get("mitre")
                    if mitre_data:
                        mitre_matches.append(mitre_data)

                    # Context enrichment
                    context_data = result.get("context")
                    if context_data:
                        contexts.append(context_data)

                    self.alert_state.mark_triggered(
                        user_id=user_id,
                        rule_id=rule_id,
                        current_event=event
                    )
                else:
                    logger.info(f"Suppressed duplicate alert: {user_id} - {rule_id}")

            correlation = {
                "behavioral_score": behavioral_score,
                "flags": flags,
                "matched_rules": matched_rules,
                "mitre": mitre_matches,
                "context": contexts,
                "evaluated_at": datetime.now(UTC)
            }

        except Exception as e:
            logger.error(f"Correlation engine failure: {e}")
            correlation = None  # FAIL-OPEN

        enriched_event = dict(event)
        enriched_event["correlation"] = correlation

        return enriched_event