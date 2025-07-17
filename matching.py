import sqlite3

def match_and_log():
    conn = sqlite3.connect("skillvolunteer.db")
    cur = conn.cursor()

    # Fetch requests
    cur.execute("SELECT * FROM requests")
    requests = cur.fetchall()

    # Fetch volunteers
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    for req in requests:
        req_id, requester_name, requested_skill, req_location, req_avail = req

        best_match = None
        for user in users:
            user_id, name, skills, location, availability = user
            if requested_skill.lower() in skills.lower() and req_avail.lower() == availability.lower():
                # Simple scoring: match if skill + availability match
                best_match = user
                break

        if best_match:
            _, volunteer_name, _, _, _ = best_match
            cur.execute("""
                INSERT INTO match_logs (requester_name, volunteer_name, skill, location, score)
                VALUES (?, ?, ?, ?, ?)
            """, (requester_name, volunteer_name, requested_skill, req_location, 100))

    conn.commit()
    conn.close()
