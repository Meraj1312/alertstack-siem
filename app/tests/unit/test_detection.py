from app.detection.engine import DetectionEngine
from app.detection.context import DetectionContext


def test_detection_output():
    context = DetectionContext()
    engine = DetectionEngine(context)

    event = {
        "event_id": "d1",
        "timestamp": "2026-01-01T10:00:00",
        "user_id": "user-1",
        "event_type": "login",
        "risk": {"score": 80, "severity": "high"},
        "correlation": {}
    }

    context.add_event(event)
    result = engine.run(event)

    assert "alerts" in result
    assert "severity" in result
    assert "confidence" in result