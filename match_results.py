import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = "Match Results"
    page.scroll = ft.ScrollMode.ALWAYS

    def load_data():
        conn = sqlite3.connect("skillvolunteer.db")
        cur = conn.cursor()
        cur.execute("SELECT requester_name, volunteer_name, skill, location, score FROM match_logs")
        matches = cur.fetchall()
        conn.close()

        return [
            ft.Text(f"Request: {r} | Volunteer: {v} | Skill: {s} | Location: {l} | Score: {sc}",
                    color="white")
            for r, v, s, l, sc in matches
        ]

    back_button = ft.ElevatedButton("← Back", on_click=lambda _: page.go("/"))

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                [ft.Text("Match Results", size=30, color="white")] + load_data() + [back_button],
                scroll=ft.ScrollMode.ALWAYS
            ),
            expand=True,
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1e3c72", "#2a5298"]
            ),
            padding=20,
        )
    )
    page.update()
