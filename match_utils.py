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


from database import get_all_volunteers, add_match, get_help_request_by_email

def match_request_to_volunteer(requester_email: str):
    req = get_help_request_by_email(requester_email)
    if not req:
        return

    req_skill = (req.get("skills") or "").strip().lower()
    req_loc = (req.get("location") or "").strip().lower()
    req_av = (req.get("availability") or "").strip().lower()

    for vol in get_all_volunteers():
        v_skill = (vol.get("skills") or "").strip().lower()
        v_loc = (vol.get("location") or "").strip().lower()
        v_av = (vol.get("availability") or "").strip().lower()

        if req_skill == v_skill and req_loc == v_loc and req_av == v_av:
            add_match(
                request_name=req.get("name") or "",
                request_email=req.get("email") or "",
                volunteer_name=vol.get("name") or "",
                volunteer_email=vol.get("email") or "",
                skill=req.get("skills") or "",
                distance_km=None  # no geodistance needed with fixed city list
            )
