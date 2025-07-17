import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = "Admin Dashboard"

    conn = sqlite3.connect("skillvolunteer.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    num_volunteers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM requests")
    num_requests = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM match_logs")
    num_matches = cur.fetchone()[0]

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
                    ft.ElevatedButton("← Back", on_click=lambda _: page.go("/"))
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
