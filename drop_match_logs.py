import sqlite3

conn = sqlite3.connect("skillvolunteer.db")
cursor = conn.cursor()

# Drop the match_logs table if it exists
cursor.execute("DROP TABLE IF EXISTS match_logs")

conn.commit()
conn.close()

print("✅ match_logs table dropped.")
