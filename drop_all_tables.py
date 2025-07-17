import sqlite3
conn = sqlite3.connect("skillvolunteer.db")
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS requests")
c.execute("DROP TABLE IF EXISTS match_logs")
conn.commit()
conn.close()
print("✅ All tables dropped")
