import sqlite3
from datetime import datetime

DB_FILE = "skillvolunteer.db"

# ---------- INIT DB ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT,
            skills TEXT,
            location TEXT,
            availability TEXT,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            name TEXT,
            skills TEXT,
            location TEXT,
            availability TEXT,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            skills TEXT,
            location TEXT,
            availability TEXT,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_name TEXT,
            request_email TEXT,
            volunteer_name TEXT,
            volunteer_email TEXT,
            skill TEXT,
            distance_km REAL,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            logged_at TEXT
        )
    """)

    # Ensure columns exist for backwards compatibility
    _ensure_column_exists("users", "created_at", "TEXT")
    _ensure_column_exists("volunteers", "created_at", "TEXT")
    _ensure_column_exists("help_requests", "created_at", "TEXT")
    _ensure_column_exists("matches", "created_at", "TEXT")

    # Default admin account
    c.execute("SELECT * FROM users WHERE email='admin'")
    if not c.fetchone():
        c.execute("""
            INSERT INTO users (name, email, password, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, ("Admin", "admin", "1234", "Admin", datetime.now().isoformat()))

    conn.commit()
    conn.close()


def _ensure_column_exists(table, column, coltype):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table})")
    cols = [info[1] for info in c.fetchall()]
    if column not in cols:
        c.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")
    conn.commit()
    conn.close()

# ---------- USER MANAGEMENT ----------
def add_user(name, email, password, role):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, email, password, role, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, password, role, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def verify_login(email, password):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def record_sign_in(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO login_logs (email, logged_at) VALUES (?, ?)",
              (email, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# ---------- VOLUNTEER ----------
def upsert_volunteer_profile(email, name, skills, location, availability):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Upsert into volunteers table
    c.execute("SELECT * FROM volunteers WHERE email=?", (email,))
    exists = c.fetchone()
    if exists:
        c.execute("""
            UPDATE volunteers
            SET name=?, skills=?, location=?, availability=?
            WHERE email=?
        """, (name, skills, location, availability, email))
    else:
        c.execute("""
            INSERT INTO volunteers (email, name, skills, location, availability, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email, name, skills, location, availability, datetime.now().isoformat()))

    # Also update main users table
    c.execute("""
        UPDATE users
        SET skills=?, location=?, availability=?
        WHERE email=?
    """, (skills, location, availability, email))

    conn.commit()
    conn.close()

def get_all_volunteers():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM volunteers")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

# ---------- HELP REQUEST ----------
def add_help_request(name, email, skills, location, availability):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO help_requests (name, email, skills, location, availability, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, skills, location, availability, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_help_request_by_email(email):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM help_requests WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

# ---------- MATCHES ----------
def add_match(request_name, request_email, volunteer_name, volunteer_email, skill, distance_km):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO matches (request_name, request_email, volunteer_name, volunteer_email, skill, distance_km, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (request_name, request_email, volunteer_name, volunteer_email, skill, distance_km, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def admin_all_matches():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM matches ORDER BY created_at DESC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

# ---------- ADMIN ----------
def admin_all_users():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def admin_login_logs():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM login_logs ORDER BY logged_at DESC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

# ---------- INIT ----------
init_db()
