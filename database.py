import sqlite3
from datetime import datetime

DB_NAME = "skillvolunteer.db"

# ──────────────── DATABASE INITIALIZATION ────────────────
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT,
            skills TEXT,
            location TEXT,
            availability TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_name TEXT NOT NULL,
            email TEXT,
            requested_skill TEXT NOT NULL,
            location TEXT NOT NULL,
            availability TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_name TEXT NOT NULL,
            volunteer_name TEXT NOT NULL,
            skill TEXT NOT NULL,
            distance_km REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_name TEXT NOT NULL,
            request_email TEXT,
            volunteer_name TEXT NOT NULL,
            volunteer_email TEXT,
            skill TEXT NOT NULL,
            location TEXT NOT NULL,
            availability TEXT NOT NULL,
            distance_km REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ──────────────── USER & REQUEST INSERTION ────────────────

def add_volunteer(name, email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (name, email, password, "volunteer"))
    conn.commit()
    conn.close()

def add_requester(name, email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (name, email, password, "requester"))
    except sqlite3.IntegrityError:
        conn.close()
        raise

    c.execute("SELECT * FROM requesters WHERE email = ?", (email,))
    if not c.fetchone():
        c.execute("""
            INSERT INTO requesters (name, email)
            VALUES (?, ?)
        """, (name, email))

    conn.commit()
    conn.close()

def add_request(name, skill, location, availability, email=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO requests (requester_name, email, requested_skill, location, availability)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, skill, location, availability))
    conn.commit()
    conn.close()

# ──────────────── LOGIN VALIDATION ────────────────

def volunteer_exists(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND role = 'volunteer'", (email,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def requester_exists(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND role = 'requester'", (email,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def verify_login(email, password, role):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ? AND role = ?", (email, password, role))
    valid = c.fetchone() is not None
    conn.close()
    return valid

def delete_user(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE email = ?", (email,))
    c.execute("DELETE FROM requesters WHERE email = ?", (email,))
    conn.commit()
    conn.close()

def get_requester_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, email, password FROM users WHERE email = ? AND role = 'requester'", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "email": row[1], "password": row[2]}
    return None

# ──────────────── MATCHING & LOGGING ────────────────

def find_match(skill, location, availability):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT name, email, skills, location, availability FROM users
        WHERE role = 'volunteer'
    """)
    rows = c.fetchall()
    conn.close()

    matches = []
    for row in rows:
        volunteer_name, volunteer_email, skills, v_location, v_availability = row
        if skill.lower() in (skills or "").lower():
            matches.append((volunteer_name, volunteer_email, v_location, v_availability))
    return matches

def log_match(request_name, request_email, volunteer_name, volunteer_email, skill, location, availability, distance_km):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO matches (request_name, request_email, volunteer_name, volunteer_email,
                             skill, location, availability, distance_km, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (request_name, request_email, volunteer_name, volunteer_email,
          skill, location, availability, distance_km, datetime.now().isoformat()))

    c.execute("""
        INSERT INTO match_logs (requester_name, volunteer_name, skill, distance_km, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (request_name, volunteer_name, skill, distance_km, datetime.now().isoformat()))
    conn.commit()
    conn.close()
