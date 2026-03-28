from app.risk.engine import RiskEngine
from app.risk.config import PolicyManager


def test_risk_scoring():
    policy = PolicyManager("app/risk/policy.json")
    policy.load_policy()

    engine = RiskEngine(policy)

    event = {
        "event_id": "r1",
        "timestamp": "2026-01-01T10:00:00",
        "user_id": "user-1",
        "event_type": "login",
        "ip_address": "1.1.1.1"
    }

    result = engine.apply(event)

    assert "risk" in result
    assert "score" in result["risk"]
    assert result["risk"]["severity"] in ["low", "medium", "high"]