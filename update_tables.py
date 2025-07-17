import sqlite3

DB_NAME = "skillvolunteer.db"

def update_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Example: Add a new column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        print("Column already exists or error occurred")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_tables()
