import sqlite3

conn = sqlite3.connect("skillvolunteer.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS match_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_name TEXT,
    volunteer_name TEXT,
    skill TEXT,
    location TEXT,
    score INTEGER
)
""")

conn.commit()
conn.close()

print("match_logs table created.")
