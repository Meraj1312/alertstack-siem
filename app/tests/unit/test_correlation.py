from app.correlation.engine import CorrelationEngine


def test_correlation_engine():
    engine = CorrelationEngine()

    event = {
        "event_id": "c1",
        "timestamp": "2026-01-01T10:00:00",
        "user_id": "user-1",
        "event_type": "login"
    }

    result = engine.apply(event)

    assert "correlation" in result