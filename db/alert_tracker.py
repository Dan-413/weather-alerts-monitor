import sqlite3
from pathlib import Path

DB_PATH = Path("db/alerts.db")

# Ensure the DB folder exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seen_alerts (
                id TEXT PRIMARY KEY,
                event TEXT,
                headline TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()

def alert_seen(alert_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM seen_alerts WHERE id = ?", (alert_id,))
        return cursor.fetchone() is not None

def mark_alert_seen(alert_id: str, event: str, headline: str, timestamp: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO seen_alerts (id, event, headline, timestamp) VALUES (?, ?, ?, ?)",
            (alert_id, event, headline, timestamp)
        )
        conn.commit()
