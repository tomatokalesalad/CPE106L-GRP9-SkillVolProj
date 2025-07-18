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
            email TEXT,
            skills TEXT NOT NULL,
            location TEXT NOT NULL,
            availability TEXT NOT NULL
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

    # ✅ Add this missing table
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

    conn.commit()
    conn.close()

# ──────────────── USER & REQUEST INSERTION ────────────────
def add_volunteer(name, skills, location, availability, email=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, email, skills, location, availability)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, skills, location, availability))
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

# ──────────────── MATCH FINDING ────────────────
def find_match(skill, location, availability):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT name, skills, location, availability, email FROM users
        WHERE skills LIKE ? AND availability = ?
    """, (f"%{skill}%", availability))
    results = c.fetchall()
    conn.close()
    return results

# ──────────────── MATCH LOGGING ────────────────
def insert_match_log(requester_name, volunteer_name, skill, distance_km):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO match_logs (requester_name, volunteer_name, skill, distance_km, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (requester_name, volunteer_name, skill, distance_km, timestamp))
    conn.commit()
    conn.close()

def view_match_logs():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM match_logs")
    logs = c.fetchall()
    conn.close()
    return logs

# ──────────────── MATCHING + LOGGING FUNCTION ────────────────
def match_request_to_volunteer(requester_name, requested_skill, location, availability, request_email=None):
    candidates = find_match(requested_skill, location, availability)

    if not candidates:
        return None

    volunteer = candidates[0]
    volunteer_name = volunteer[0]
    volunteer_email = volunteer[4]

    # Simulated distance (replace with haversine if needed)
    distance_km = 1.0

    insert_match_log(requester_name, volunteer_name, requested_skill, distance_km)
    log_match(requester_name, request_email, volunteer_name, volunteer_email, requested_skill, location, availability, distance_km)

    return volunteer_name, distance_km

def log_match(request_name, request_email, volunteer_name, volunteer_email, skill, location, availability, distance_km):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO matches (request_name, request_email, volunteer_name, volunteer_email, skill, location, availability, distance_km, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (request_name, request_email, volunteer_name, volunteer_email, skill, location, availability, distance_km, timestamp))
    conn.commit()
    conn.close()
