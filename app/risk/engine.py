from datetime import datetime, UTC
import logging
from app.risk.rules import evaluate_rule

logger = logging.getLogger(__name__)


class RiskEngine:

    def __init__(self, policy_manager):
        self.policy_manager = policy_manager

    def apply(self, event: dict) -> dict:

        try:
            policy = self.policy_manager.get_policy()

            total_score = policy["global_settings"]["default_risk_score"]
            flags = []

            for rule in policy["rules"]:
                if not rule["enabled"]:
                    continue

                if evaluate_rule(event, rule):
                    total_score += rule["risk_score"]
                    flags.append(rule["rule_id"])

            max_score = policy["global_settings"]["max_risk_score"]
            total_score = min(total_score, max_score)

            severity = self._resolve_severity(total_score, policy)

            risk = {
                "score": total_score,
                "severity": severity,
                "flags": flags,
                "calculated_at": datetime.now(UTC),
                "policy_version": policy["policy_version"]
            }

        except Exception as e:
            logger.error(f"Risk engine failure: {e}")

            risk = {
                "score": None,
                "severity": None,
                "flags": [],
                "calculated_at": None,
                "policy_version": getattr(
                    self.policy_manager,
                    "active_policy_version",
                    "unknown"
                )
            }

        enriched_event = dict(event)
        enriched_event["risk"] = risk

        return enriched_event

    def _resolve_severity(self, score: int, policy: dict) -> str:
        for level in policy["severity_levels"]:
            if level["min"] <= score <= level["max"]:
                return level["label"]
        return "low"