import sqlite3

def match_request_to_volunteer(request_id):
    conn = sqlite3.connect("volunteer_exchange.db")
    cursor = conn.cursor()

    # Get the skill for this request
    cursor.execute("SELECT skill FROM requests WHERE id = ?", (request_id,))
    request = cursor.fetchone()

    if request is None:
        conn.close()
        return None

    skill_needed = request[0]

    # Find available volunteer with that skill
    cursor.execute("""
        SELECT id FROM volunteers 
        WHERE skill = ? AND available = 1
        LIMIT 1
    """, (skill_needed,))
    volunteer = cursor.fetchone()

    if volunteer is None:
        conn.close()
        return None

    volunteer_id = volunteer[0]

    # Insert into matches table
    cursor.execute("""
        INSERT INTO matches (volunteer_id, request_id)
        VALUES (?, ?)
    """, (volunteer_id, request_id))

    # Mark volunteer as unavailable
    cursor.execute("UPDATE volunteers SET available = 0 WHERE id = ?", (volunteer_id,))

    conn.commit()
    conn.close()

    return volunteer_id
