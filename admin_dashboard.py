import flet as ft
import sqlite3
from typing import List, Dict

DB_PATH = "skillvolunteer.db"

# ----------------------------- Utilities -----------------------------

def _table_exists(cur, name: str) -> bool:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name)=LOWER(?)", (name,))
    return cur.fetchone() is not None

def _safe_exec(cur, sql: str, params: tuple = ()):
    try:
        cur.execute(sql, params)
    except Exception:
        # Swallow errors for optional tables/columns so UI keeps working
        pass

def _show_snack(page: ft.Page, msg: str, ok: bool = True):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(msg),
        bgcolor="#2ecc71" if ok else "#e74c3c",
    )
    page.snack_bar.open = True
    page.update()

# -------------------------- DB fetch helpers -------------------------

def fetch_users_with_profiles() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Join with optional tables if they exist
    left_join_vol = "LEFT JOIN volunteers v ON LOWER(v.email) = LOWER(u.email)" if _table_exists(cur, "volunteers") else ""
    left_join_req = "LEFT JOIN help_requests h ON LOWER(h.email) = LOWER(u.email)" if _table_exists(cur, "help_requests") else ""
    # Also support legacy "requests" table name
    if not _table_exists(cur, "help_requests") and _table_exists(cur, "requests"):
        left_join_req = "LEFT JOIN requests h ON LOWER(h.email) = LOWER(u.email)"

    query = f"""
        SELECT 
            u.id,
            u.name,
            u.email,
            u.role,
            COALESCE(v.skills, h.skills, u.skills) AS skills,
            COALESCE(v.location, h.location, u.location) AS location,
            COALESCE(v.availability, h.availability, u.availability) AS availability,
            u.created_at
        FROM users u
        {left_join_vol}
        {left_join_req}
        ORDER BY u.created_at DESC
    """
    cur.execute(query)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def fetch_all_matches_full() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Decide which match table & columns exist
    match_table = "matches" if _table_exists(cur, "matches") else ("match_logs" if _table_exists(cur, "match_logs") else None)
    if not match_table:
        conn.close()
        return []  # No match data at all

    # Some schemas store `skill`, some `skills`; some `distance_km`, some `distance`
    has_skill_col = False
    has_skills_col = False
    has_distance_km = False
    has_distance = False

    cur.execute(f"PRAGMA table_info({match_table})")
    cols = {row["name"].lower() for row in cur.fetchall()}
    has_skill_col = "skill" in cols
    has_skills_col = "skills" in cols
    has_distance_km = "distance_km" in cols
    has_distance = "distance" in cols

    match_skill_expr = "m.skill" if has_skill_col else ("m.skills" if has_skills_col else "''")
    distance_expr = "m.distance_km" if has_distance_km else ("m.distance" if has_distance else "NULL")

    # Build joins to users table (case-insensitive)
    query = f"""
        SELECT 
            m.id,
            m.request_name,
            m.request_email,
            req.role AS request_role,
            COALESCE(req.skills, '') AS request_skills,
            COALESCE(req.location, '') AS request_location,
            COALESCE(req.availability, '') AS request_availability,

            m.volunteer_name,
            m.volunteer_email,
            vol.role AS volunteer_role,
            COALESCE(vol.skills, '') AS volunteer_skills,
            COALESCE(vol.location, '') AS volunteer_location,
            COALESCE(vol.availability, '') AS volunteer_availability,

            {match_skill_expr} AS match_skill,
            {distance_expr} AS distance_km,
            m.created_at
        FROM {match_table} m
        LEFT JOIN users req ON LOWER(req.email) = LOWER(m.request_email)
        LEFT JOIN users vol ON LOWER(vol.email) = LOWER(m.volunteer_email)
        ORDER BY m.created_at DESC
    """
    cur.execute(query)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def delete_user(user_id: int, page: ft.Page) -> bool:
    """Delete user safely from DB, removing related data if those tables/columns exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Get user's email first for cascading deletes by email
        cur.execute("SELECT email FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            _show_snack(page, "User not found.", ok=False)
            return False
        email = row["email"]

        # Delete from optional related tables safely
        if _table_exists(cur, "volunteers"):
            _safe_exec(cur, "DELETE FROM volunteers WHERE user_id=?", (user_id,))
            _safe_exec(cur, "DELETE FROM volunteers WHERE LOWER(email)=LOWER(?)", (email,))
        if _table_exists(cur, "help_requests"):
            _safe_exec(cur, "DELETE FROM help_requests WHERE user_id=?", (user_id,))
            _safe_exec(cur, "DELETE FROM help_requests WHERE LOWER(email)=LOWER(?)", (email,))
        if _table_exists(cur, "requests"):
            _safe_exec(cur, "DELETE FROM requests WHERE user_id=?", (user_id,))
            _safe_exec(cur, "DELETE FROM requests WHERE LOWER(email)=LOWER(?)", (email,))

        # Delete from whichever match table exists
        if _table_exists(cur, "matches"):
            _safe_exec(cur, "DELETE FROM matches WHERE LOWER(request_email)=LOWER(?) OR LOWER(volunteer_email)=LOWER(?)", (email, email))
        if _table_exists(cur, "match_logs"):
            _safe_exec(cur, "DELETE FROM match_logs WHERE LOWER(request_email)=LOWER(?) OR LOWER(volunteer_email)=LOWER(?)", (email, email))

        # Finally delete the user
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        _show_snack(page, "User deleted.")
        return True
    except Exception as ex:
        _show_snack(page, f"Delete failed: {ex}", ok=False)
        return False

# ----------------------------- UI Builders -----------------------------

def _scrollable_data_table(columns: List[str], rows: List[List[ft.Control]], height: int = 320):
    """Wraps a DataTable with both vertical & horizontal scroll, fixed height."""
    dt = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(c)) for c in columns],
        rows=[ft.DataRow(cells=[ft.DataCell(ctrl) for ctrl in row]) for row in rows],
        column_spacing=12,
        data_row_max_height=48,
        heading_row_height=44,
        divider_thickness=0.5,
    )
    # Horizontal + vertical scrolling
    return ft.Container(
        height=height,
        content=ft.Column(
            controls=[
                ft.Row(controls=[dt], scroll=ft.ScrollMode.AUTO)  # horizontal
            ],
            scroll=ft.ScrollMode.AUTO  # vertical
        ),
        border=ft.border.all(1, "#000000"),
        bgcolor="#000000",
        padding=8,
    )

def make_user_section(title: str, users: List[Dict], page: ft.Page, refresh_cb):
    user_cols = ["ID", "Name", "Email", "Role", "Skills", "Location", "Availability", "Created at", "Actions"]
    user_rows: List[List[ft.Control]] = []

    for u in users:
        # capture id for handler
        uid = u.get("id")
        def make_handler(id_to_delete=uid):
            def _h(_):
                if delete_user(id_to_delete, page):
                    refresh_cb()
            return _h

        user_rows.append([
            ft.Text(str(u.get("id", ""))),
            ft.Text(str(u.get("name", ""))),
            ft.Text(str(u.get("email", ""))),
            ft.Text(str(u.get("role", ""))),
            ft.Text(str(u.get("skills", ""))),
            ft.Text(str(u.get("location", ""))),
            ft.Text(str(u.get("availability", ""))),
            ft.Text(str(u.get("created_at", ""))),
            ft.Row(
                [
                    ft.IconButton(icon=ft.icons.DELETE, icon_color="red", tooltip="Delete", on_click=make_handler())
                ]
            )
        ])

    return ft.Column(
        controls=[
            ft.Text(title, size=18, weight="bold"),
            _scrollable_data_table(user_cols, user_rows, height=260)
        ],
        spacing=8
    )

def make_matches_section(matches: List[Dict]):
    cols = [
        "ID",
        "Requester Name", "Requester Email", "Requester Role", "Requester Skills", "Requester Location", "Requester Availability",
        "Volunteer Name", "Volunteer Email", "Volunteer Role", "Volunteer Skills", "Volunteer Location", "Volunteer Availability",
        "Matched Skill", "Distance (km)", "Created at"
    ]

    rows: List[List[ft.Control]] = []
    for m in matches:
        rows.append([
            ft.Text(str(m.get("id", ""))),
            ft.Text(str(m.get("request_name", ""))),
            ft.Text(str(m.get("request_email", ""))),
            ft.Text(str(m.get("request_role", ""))),
            ft.Text(str(m.get("request_skills", ""))),
            ft.Text(str(m.get("request_location", ""))),
            ft.Text(str(m.get("request_availability", ""))),

            ft.Text(str(m.get("volunteer_name", ""))),
            ft.Text(str(m.get("volunteer_email", ""))),
            ft.Text(str(m.get("volunteer_role", ""))),
            ft.Text(str(m.get("volunteer_skills", ""))),
            ft.Text(str(m.get("volunteer_location", ""))),
            ft.Text(str(m.get("volunteer_availability", ""))),

            ft.Text(str(m.get("match_skill", ""))),
            ft.Text("" if m.get("distance_km") is None else str(m.get("distance_km"))),
            ft.Text(str(m.get("created_at", ""))),
        ])

    return ft.Column(
        controls=[
            ft.Text("All Matches", size=18, weight="bold"),
            _scrollable_data_table(cols, rows, height=320)
        ],
        spacing=8
    )

# ------------------------------- Main UI --------------------------------

def main(page: ft.Page):
    def refresh():
        main(page)

    page.controls.clear()
    page.title = "Admin Dashboard"
    page.scroll = ft.ScrollMode.AUTO

    # Top bar with title and true navigation to Home (new slide via router)
    top_bar = ft.Row(
        controls=[
            ft.Text("Admin — Overview", size=24, weight="bold"),
            ft.ElevatedButton(
                "🏠 Home",
                on_click=lambda _: page.go("/"),
                bgcolor="#007BFF",
                color="black",
                height=40
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Fetch data
    all_users = fetch_users_with_profiles()
    volunteers = [u for u in all_users if (u.get("role") or "").lower() == "volunteer"]
    requesters = [u for u in all_users if (u.get("role") or "").lower() == "requester"]
    matches = fetch_all_matches_full()

    # Sections
    volunteers_sec = make_user_section("Volunteers", volunteers, page, refresh)
    requesters_sec = make_user_section("Requesters", requesters, page, refresh)
    matches_sec = make_matches_section(matches)

    # Layout — all inside a scrollable column
    body = ft.Column(
        controls=[
            top_bar,
            volunteers_sec,
            requesters_sec,
            matches_sec
        ],
        spacing=18
    )

    page.add(ft.Container(content=body, expand=True, padding=20))
    page.update()
