import flet as ft
import sqlite3

def match_results_ui(page: ft.Page):
    page.title = "Match History"
    page.theme_mode = ft.ThemeMode.DARK

    def fetch_match_data():
        conn = sqlite3.connect("skillvolunteer.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT volunteer_name, volunteer_email, requester_name, requester_need, matched_skill, timestamp
            FROM match_history
            ORDER BY timestamp DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    matches = fetch_match_data()

    match_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Volunteer")),
            ft.DataColumn(label=ft.Text("Email")),
            ft.DataColumn(label=ft.Text("Requester")),
            ft.DataColumn(label=ft.Text("Need")),
            ft.DataColumn(label=ft.Text("Matched Skill")),
            ft.DataColumn(label=ft.Text("Timestamp")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row[0])),
                    ft.DataCell(ft.Text(row[1])),
                    ft.DataCell(ft.Text(row[2])),
                    ft.DataCell(ft.Text(row[3])),
                    ft.DataCell(ft.Text(row[4])),
                    ft.DataCell(ft.Text(row[5])),
                ]
            ) for row in matches
        ]
    )

    def go_back(e):
        import admin_dashboard  # or wherever your main admin panel is
        admin_dashboard.main(page)

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("📜 Match History Log", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                match_table,
                ft.ElevatedButton("⬅ Back to Dashboard", on_click=go_back)
            ], scroll=ft.ScrollMode.ALWAYS),
            padding=20
        )
    )
    page.update()
