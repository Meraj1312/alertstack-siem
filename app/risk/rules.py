def evaluate_rule(event: dict, rule: dict) -> bool:

    conditions = rule.get("conditions", {})

    if event.get("event_type") != conditions.get("event_type"):
        return False

    if "amount_gt" in conditions:
        amount = event.get("event_data", {}).get("amount")
        if amount is None or amount <= conditions["amount_gt"]:
            return False

    return True