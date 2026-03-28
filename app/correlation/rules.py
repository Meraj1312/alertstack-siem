from app.correlation.state_manager import StateManager

TIME_WINDOW_SECONDS = 300


def detect_bruteforce(event: dict, state_manager: StateManager):

    if event.get("event_type") != "login_failed":
        return None

    user_id = event.get("user_id")

    if not user_id:
        return None

    recent_events = state_manager.get_events_by_user_and_type(
        user_id=user_id,
        event_type="login_failed",
        current_event=event,
        window_seconds=TIME_WINDOW_SECONDS
    )

    total_attempts = len(recent_events) + 1

    context = {
        "attempt_count": total_attempts,
        "window_seconds": TIME_WINDOW_SECONDS
    }

    if total_attempts >= 20:
        return {
            "rule_id": "BRUTE_FORCE_CRITICAL",
            "behavioral_score": 90,
            "flag": "BRUTE_FORCE_CRITICAL",
            "level": "critical",
            "context": context,
            "mitre": {
                "technique_id": "T1110",
                "technique": "Brute Force"
            }
        }

    elif total_attempts >= 10:
        return {
            "rule_id": "BRUTE_FORCE_HIGH",
            "behavioral_score": 70,
            "flag": "BRUTE_FORCE_HIGH",
            "level": "high",
            "context": context,
            "mitre": {
                "technique_id": "T1110",
                "technique": "Brute Force"
            }
        }

    elif total_attempts >= 5:
        return {
            "rule_id": "BRUTE_FORCE_MEDIUM",
            "behavioral_score": 40,
            "flag": "BRUTE_FORCE_MEDIUM",
            "level": "medium",
            "context": context,
            "mitre": {
                "technique_id": "T1110",
                "technique": "Brute Force"
            }
        }

    return None


def detect_transaction_spike(event: dict, state_manager: StateManager):

    if event.get("event_type") != "transaction":
        return None

    user_id = event.get("user_id")

    if not user_id:
        return None

    window_seconds = 120

    recent_events = state_manager.get_events_by_user_and_type(
        user_id=user_id,
        event_type="transaction",
        current_event=event,
        window_seconds=window_seconds
    )

    total_tx = len(recent_events) + 1

    if total_tx >= 5:
        return {
            "rule_id": "TRANSACTION_SPIKE",
            "behavioral_score": 60,
            "flag": "TRANSACTION_SPIKE",
            "level": "high",
            "context": {
                "transaction_count": total_tx,
                "window_seconds": window_seconds
            },
            "mitre": {
                "technique_id": "T1499",
                "technique": "Endpoint Denial of Service (Simulated)"
            }
        }

    return None