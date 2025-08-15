import flet as ft
import sqlite3

DB_PATH = "skillvolunteer.db"

def _count(cur, sql, default=0):
    try:
        cur.execute(sql)
        row = cur.fetchone()
        return int(row[0] if row and row[0] is not None else default)
    except Exception:
        return default

def main(page: ft.Page):
    page.title = "Admin Summary"
    page.scroll = ft.ScrollMode.AUTO

    # Pull counts
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
    except Exception:
        conn = None
        cur = None

    num_volunteers = 0
    num_requests   = 0
    num_matches    = 0

    if cur:
        # Adjust these table/column names if yours differ
        num_volunteers = _count(cur, "SELECT COUNT(*) FROM users WHERE lower(role)='volunteer'")
        num_requests   = _count(cur, "SELECT COUNT(*) FROM requests")
        num_matches    = _count(cur, "SELECT COUNT(*) FROM match_logs")
        conn.close()

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("📊 Admin Summary", size=32, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text(f"✅ Volunteers: {num_volunteers}", color="white"),
                    ft.Text(f"📩 Requests: {num_requests}", color="white"),
                    ft.Text(f"🔁 Matches: {num_matches}", color="white"),
                    ft.Row(
                        [
                            ft.ElevatedButton("← Back to Home", on_click=lambda _: page.go("/")),
                            ft.ElevatedButton("Go to Dashboard", on_click=lambda _: __import__("admin_dashboard").main(page)),
                        ],
                        alignment="center",
                        spacing=12
                    )
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            expand=True,
            padding=40,
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#6dd5ed", "#2193b0"]
            )
        )
    )
    page.update()
