import sqlite3

DB_NAME = "skillvolunteer.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        skills TEXT NOT NULL,
        location TEXT NOT NULL,
        availability TEXT NOT NULL
    )
    """)

    # Create requests table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        requester_name TEXT NOT NULL,
        requested_skill TEXT NOT NULL,
        location TEXT NOT NULL,
        availability TEXT NOT NULL
    )
    """)

    # Create match logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS match_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        requester_name TEXT NOT NULL,
        volunteer_name TEXT NOT NULL,
        skill TEXT NOT NULL,
        location TEXT NOT NULL,
        score INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def add_user(name, skills, location, availability):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, skills, location, availability)
        VALUES (?, ?, ?, ?)
    """, (name, skills, location, availability))
    conn.commit()
    conn.close()

def add_request(name, skill, location, availability):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO requests (requester_name, requested_skill, location, availability)
        VALUES (?, ?, ?, ?)
    """, (name, skill, location, availability))
    conn.commit()
    conn.close()

def find_match(request_skill, request_location, request_availability):
    """
    Simple matching example:
    Find volunteers with matching skill and availability.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT name, skills, location, availability FROM users
        WHERE skills LIKE ? AND availability = ?
    """, (f"%{request_skill}%", request_availability))
    results = c.fetchall()
    conn.close()
    return results
