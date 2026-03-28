import json
from typing import List, Optional
from app.db.database import get_connection


# ----------------------------
# SAVE EVENT
# ----------------------------
def save_event(event: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (
            id,
            timestamp,
            user_id,
            event_type,
            severity,
            raw_data,
            normalized_data,
            risk_data,
            correlation_data,
            detection_data
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get("event_id"),
        str(event.get("timestamp")),  
        event.get("user_id"),
        event.get("event_type"),
        event.get("detection", {}).get("severity"),

        json.dumps(event.get("raw", {}), default=str),          
        json.dumps(event.get("normalized", {}), default=str),   
        json.dumps(event.get("risk", {}), default=str),         
        json.dumps(event.get("correlation", {}), default=str),  
        json.dumps(event.get("detection", {}), default=str),    
    ))

    conn.commit()
    conn.close()

# ----------------------------
# FETCH EVENTS (WITH FILTERS)
# ----------------------------
def fetch_events(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[dict]:

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)

    if event_type:
        query += " AND event_type = ?"
        params.append(event_type)

    if severity:
        query += " AND severity = ?"
        params.append(severity)

    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()

    return [_row_to_event(row) for row in rows]


# ----------------------------
# FETCH ALERTS (SOC VIEW)
# ----------------------------
def fetch_alerts(limit: int = 50, offset: int = 0) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM events
        WHERE severity IN ('medium', 'high', 'critical')
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))

    rows = cursor.fetchall()
    conn.close()

    alerts = []

    for row in rows:
        event = _row_to_event(row)
        detection = event.get("detection", {})

        for alert in detection.get("alerts", []):
            alerts.append({
                "event_id": event["event_id"],
                "timestamp": event["timestamp"],
                "user_id": event["user_id"],
                "type": alert.get("type"),
                "severity": detection.get("severity"),
                "confidence": detection.get("confidence"),
                "reason": alert.get("reason"),
                "mitre": alert.get("mitre"),
            })

    return alerts


# ----------------------------
# FETCH USER TIMELINE
# ----------------------------
def fetch_user_activity(user_id: str) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM events
        WHERE user_id = ?
        ORDER BY timestamp ASC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [_row_to_event(row) for row in rows]


# ----------------------------
# INTERNAL HELPER
# ----------------------------
def _row_to_event(row) -> dict:
    return {
        "event_id": row[0],
        "timestamp": row[1],
        "user_id": row[2],
        "event_type": row[3],
        "severity": row[4],

        "raw": json.loads(row[5]) if row[5] else {},
        "normalized": json.loads(row[6]) if row[6] else {},
        "risk": json.loads(row[7]) if row[7] else {},
        "correlation": json.loads(row[8]) if row[8] else {},
        "detection": json.loads(row[9]) if row[9] else {},
    }