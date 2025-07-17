import sqlite3

conn = sqlite3.connect("skillvolunteer.db")
cursor = conn.cursor()

# Add email columns if not already present
try:
    cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
except sqlite3.OperationalError:
    print("Column 'email' already exists in 'users'")

try:
    cursor.execute("ALTER TABLE requests ADD COLUMN email TEXT")
except sqlite3.OperationalError:
    print("Column 'email' already exists in 'requests'")

# Create matches table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_name TEXT,
        request_email TEXT,
        volunteer_name TEXT,
        volunteer_email TEXT,
        skill TEXT,
        location TEXT,
        availability TEXT,
        distance_km REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()

print("✅ Database schema updated.")
