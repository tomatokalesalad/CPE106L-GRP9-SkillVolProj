import sqlite3
from datetime import datetime

def log_match(volunteer_id, requester_id):
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteer_id INTEGER,
            requester_id INTEGER,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO matches (volunteer_id, requester_id, timestamp)
        VALUES (?, ?, ?)
    """, (volunteer_id, requester_id, datetime.now().isoformat()))

    conn.commit()
    conn.close()
