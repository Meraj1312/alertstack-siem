import uuid


def test_full_pipeline_flow(client):
    # ----------------------------
    # Create unique event
    # ----------------------------
    event_id = f"test-{uuid.uuid4()}"

    event = {
        "event_id": event_id,
        "event_type": "login",
        "timestamp": "2026-01-01T10:00:00",
        "source_ip": "1.1.1.1",
        "outcome": "success",
        "user_id": "user-123",
        "event_data": {
            "device": "chrome"
        },
        "context": {
            "location": "IN"
        }
    }

    # ----------------------------
    # 1. INGEST EVENT
    # ----------------------------
    response = client.post("/ingest", json=event)
    print(response.json()) 
    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["event_id"] == event_id
    assert "risk" in data
    assert "detection" in data

    # ----------------------------
    # 2. VERIFY EVENT STORED
    # ----------------------------
    events_res = client.get("/events")
    assert events_res.status_code == 200

    events_data = events_res.json()
    events = events_data["events"]

    assert any(e["event_id"] == event_id for e in events)

    # ----------------------------
    # 3. VERIFY USER ACTIVITY
    # ----------------------------
    user_res = client.get(f"/users/{event['user_id']}/activity")
    assert user_res.status_code == 200

    user_data = user_res.json()

    assert user_data["user_id"] == event["user_id"]
    assert any(e["event_id"] == event_id for e in user_data["timeline"])

    # ----------------------------
    # 4. VERIFY ALERTS STRUCTURE
    # ----------------------------
    alerts_res = client.get("/alerts")
    assert alerts_res.status_code == 200

    alerts_data = alerts_res.json()

    assert "alerts" in alerts_data

    # Even if no alerts triggered, structure must exist
    assert isinstance(alerts_data["alerts"], list)

    # ----------------------------
    # 5. VERIFY METRICS
    # ----------------------------
    metrics_res = client.get("/metrics")
    assert metrics_res.status_code == 200

    metrics = metrics_res.json()

    assert "total_events" in metrics
    assert "total_alerts" in metrics
    assert "severity_breakdown" in metrics
    assert "event_type_breakdown" in metrics

    assert metrics["total_events"] >= 1

    # ----------------------------
    # 6. TIME FILTER TEST
    # ----------------------------
    filtered_events_res = client.get(
        "/events",
        params={
            "start_time": "2026-01-01T09:00:00",
            "end_time": "2026-01-01T11:00:00"
        }
    )

    assert filtered_events_res.status_code == 200

    filtered_events = filtered_events_res.json()["events"]

    assert any(e["event_id"] == event_id for e in filtered_events)