import sqlite3
from datetime import datetime

DB_NAME = "skillvolunteer.db"

def match_and_log():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Fetch all help requests
    cur.execute("SELECT * FROM requests")
    requests = cur.fetchall()

    # Fetch all volunteers
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    for req in requests:
        req_id, requester_name, requested_skill, req_location, req_avail = req
        best_match = None

        for user in users:
            user_id, name, skills, location, availability = user
            if (
                requested_skill.lower() in skills.lower()
                and req_avail.lower() == availability.lower()
            ):
                # Matching logic: skill and availability must match
                best_match = user
                break

        if best_match:
            _, volunteer_name, _, _, _ = best_match

            # You can later calculate real distance using location_utils.py
            distance_km = 1.0  # Placeholder

            # Score could be enhanced based on distance, skill priority, etc.
            score = 100

            # Log the match
            cur.execute("""
                INSERT INTO match_logs (requester_name, volunteer_name, skill, location, score)
                VALUES (?, ?, ?, ?, ?)
            """, (requester_name, volunteer_name, requested_skill, req_location, score))

    conn.commit()
    conn.close()
