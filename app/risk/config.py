import json
from typing import Dict, Any


class PolicyValidationError(Exception):
    pass


class PolicyManager:

    REQUIRED_TOP_LEVEL = {
        "policy_version",
        "global_settings",
        "severity_levels",
        "rules",
    }

    REQUIRED_RULE_FIELDS = {
        "rule_id",
        "enabled",
        "description",
        "conditions",
        "risk_score",
    }

    def __init__(self, policy_path: str):
        self.policy_path = policy_path
        self.policy = None
        self.active_policy_version = None

    def load_policy(self):
        with open(self.policy_path, "r") as f:
            policy = json.load(f)

        self._validate_policy(policy)

        self.policy = policy
        self.active_policy_version = policy["policy_version"]

    def get_policy(self):
        if not self.policy:
            raise RuntimeError("Policy not loaded")
        return self.policy

    def _validate_policy(self, policy: Dict[str, Any]):

        missing = self.REQUIRED_TOP_LEVEL - policy.keys()
        if missing:
            raise PolicyValidationError(f"Missing keys: {missing}")

        global_settings = policy["global_settings"]

        if "default_risk_score" not in global_settings:
            raise PolicyValidationError("Missing default_risk_score")

        if "max_risk_score" not in global_settings:
            raise PolicyValidationError("Missing max_risk_score")

        max_score = global_settings["max_risk_score"]

        if not isinstance(max_score, int) or max_score <= 0:
            raise PolicyValidationError("Invalid max_risk_score")

        self._validate_severity(policy["severity_levels"], max_score)
        self._validate_rules(policy["rules"], max_score)

    def _validate_severity(self, levels, max_score):

        ranges = []

        for level in levels:
            if not {"min", "max", "label"} <= level.keys():
                raise PolicyValidationError("Invalid severity structure")

            if level["min"] > level["max"]:
                raise PolicyValidationError("Invalid severity range")

            ranges.append((level["min"], level["max"]))

        ranges.sort()

        for i in range(len(ranges) - 1):
            if ranges[i][1] >= ranges[i + 1][0]:
                raise PolicyValidationError("Overlapping severity ranges")

        if max(r[1] for r in ranges) < max_score:
            raise PolicyValidationError("Severity does not cover max score")

    def _validate_rules(self, rules, max_score):

        rule_ids = set()

        for rule in rules:

            missing = self.REQUIRED_RULE_FIELDS - rule.keys()
            if missing:
                raise PolicyValidationError(f"Rule missing {missing}")

            if rule["rule_id"] in rule_ids:
                raise PolicyValidationError("Duplicate rule_id")

            rule_ids.add(rule["rule_id"])

            if not isinstance(rule["risk_score"], int):
                raise PolicyValidationError("Invalid risk_score")

            if rule["risk_score"] > max_score:
                raise PolicyValidationError("risk_score exceeds max")