from fastapi import APIRouter
from models import User, Request
import sqlite3

router = APIRouter()

# ───────────────────────────────
# POST /register
@router.post("/register")
def register_user(user: User):
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, skills, location, availability)
        VALUES (?, ?, ?, ?)
    """, (user.name, user.skills, user.location, user.availability.value))
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}

# ───────────────────────────────
# POST /request-help
@router.post("/request-help")
def request_help(request: Request):
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO requests (requester_name, requested_skill, location, availability)
        VALUES (?, ?, ?, ?)
    """, (request.requester_name, request.requested_skill, request.location, request.availability.value))
    conn.commit()
    conn.close()
    return {"message": "Request submitted successfully"}

# ───────────────────────────────
# GET /users
@router.get("/users")
def get_users():
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, skills, location, availability FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = [
        {"name": row[0], "skills": row[1], "location": row[2], "availability": row[3]}
        for row in rows
    ]
    return {"users": users}

# ───────────────────────────────
# GET /match
@router.get("/match")
def match_requests():
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()

    cursor.execute("SELECT requester_name, requested_skill, location, availability FROM requests")
    requests = cursor.fetchall()

    cursor.execute("SELECT name, skills, location, availability FROM users")
    users = cursor.fetchall()

    matches = []
    unmatched_requests = []

    for req in requests:
        requester_name, requested_skill, req_location, req_availability = req
        best_match = None
        best_score = -1

        for user in users:
            user_name, user_skills, user_location, user_availability = user
            score = 0

            if requested_skill.lower() in user_skills.lower():
                score += 1
            if req_location.lower() == user_location.lower():
                score += 1
            if req_availability.lower() == user_availability.lower():
                score += 1

            if score > best_score:
                best_score = score
                best_match = user_name

        if best_match and best_score > 0:
            matches.append({
                "requester": requester_name,
                "volunteer": best_match,
                "skill": requested_skill,
                "location": req_location,
                "availability": req_availability,
                "score": best_score
            })

            cursor.execute("""
                INSERT INTO match_logs (requester_name, volunteer_name, skill, location, score)
                VALUES (?, ?, ?, ?, ?)
            """, (requester_name, best_match, requested_skill, req_location, best_score))
        else:
            unmatched_requests.append({
                "requester": requester_name,
                "requested_skill": requested_skill,
                "location": req_location,
                "availability": req_availability
            })

    conn.commit()
    conn.close()
    return {
        "matches": matches,
        "unmatched_requests": unmatched_requests
    }

# ───────────────────────────────
# GET /match-logs
@router.get("/match-logs")
def get_match_logs():
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()
    cursor.execute("SELECT requester_name, volunteer_name, skill, location, score FROM match_logs")
    rows = cursor.fetchall()
    conn.close()

    logs = [
        {"requester": row[0], "volunteer": row[1], "skill": row[2], "location": row[3], "score": row[4]}
        for row in rows
    ]
    return {"match_logs": logs}
