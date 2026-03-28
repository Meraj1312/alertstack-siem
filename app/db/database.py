import sqlite3
from pathlib import Path
from app.config.settings import settings

# ----------------------------
# DB CONFIG (temporary - will move to config later)
# ----------------------------
DB_PATH = settings.DB_PATH


# ----------------------------
# GET CONNECTION
# ----------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # enables dict-like access
    return conn


# ----------------------------
# INIT DB (CREATE TABLES)
# ----------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            user_id TEXT,
            event_type TEXT,
            severity TEXT,

            raw_data TEXT,
            normalized_data TEXT,
            risk_data TEXT,
            correlation_data TEXT,
            detection_data TEXT
        )
    """)

    conn.commit()
    conn.close()