from typing import List, Dict, Optional
from datetime import datetime
import json

from app.db.database import get_connection


# ➕ Add event to DB
def add_event(event: Dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO events (
                id, timestamp, user_id, event_type, severity,
                raw_data, normalized_data, risk_data,
                correlation_data, detection_data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event["event_id"],
            event["timestamp"],
            event.get("user_id"),
            event.get("event_type"),
            event.get("risk", {}).get("severity", "low"),

            json.dumps(event.get("raw", {})),
            json.dumps(event.get("normalized", {})),
            json.dumps(event.get("risk", {})),
            json.dumps(event.get("correlation", {})),
            json.dumps(event.get("detection", {})),
        ))

        conn.commit()
        return True

    except Exception as e:
        print("DB Insert Error:", e)
        return False

    finally:
        conn.close()


# 📥 Get all events
def get_all_events() -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, user_id, event_type, severity
        FROM events
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# 🔍 Query events
def query_events(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, timestamp, user_id, event_type, severity
        FROM events
        WHERE 1=1
    """

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

    if start_time:
        query += " AND timestamp >= ?"
        params.append(start_time.isoformat())

    if end_time:
        query += " AND timestamp <= ?"
        params.append(end_time.isoformat())

    query += " ORDER BY timestamp DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]