import sqlite3

def create_match_history_table():
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_history (
            id TEXT PRIMARY KEY,
            volunteer_name TEXT,
            volunteer_email TEXT,
            requester_name TEXT,
            requester_need TEXT,
            matched_skill TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

create_match_history_table()
