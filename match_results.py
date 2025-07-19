import flet as ft
import sqlite3

def match_results_ui(page: ft.Page, return_to="admin", email=None):
    page.title = "Match History"
    page.theme_mode = ft.ThemeMode.DARK

    def fetch_match_data():
        try:
            conn = sqlite3.connect("skillvolunteer.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT volunteer_name, volunteer_email, request_name, request_email, skill, timestamp
                FROM matches
                ORDER BY timestamp DESC
            """)
            rows = cursor.fetchall()
            conn.close()
            print(f"✅ Retrieved {len(rows)} match entries.")
            return rows
        except Exception as e:
            print("❌ Error fetching match data:", e)
            return []

    matches = fetch_match_data()

    # Build table rows safely even if values are None
    match_rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(row[0] or "—"))),
                ft.DataCell(ft.Text(str(row[1] or "—"))),
                ft.DataCell(ft.Text(str(row[2] or "—"))),
                ft.DataCell(ft.Text(str(row[3] or "—"))),
                ft.DataCell(ft.Text(str(row[4] or "—"))),
                ft.DataCell(ft.Text(str(row[5] or "—"))),
            ]
        )
        for row in matches
    ] if matches else [
        ft.DataRow(cells=[ft.DataCell(ft.Text("No data")) for _ in range(6)])
    ]

    match_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Volunteer")),
            ft.DataColumn(label=ft.Text("Email")),
            ft.DataColumn(label=ft.Text("Requester")),
            ft.DataColumn(label=ft.Text("Need")),
            ft.DataColumn(label=ft.Text("Matched Skill")),
            ft.DataColumn(label=ft.Text("Timestamp")),
        ],
        rows=match_rows
    )

    def go_back(e):
        if return_to == "requester":
            import requester_dashboard
            requester_dashboard.main(page, name=email)
        elif return_to == "volunteer":
            import volunteer_dashboard
            volunteer_dashboard.main(page, name=email)
        else:
            import admin_dashboard
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
            padding=20,
            expand=True,
        )
    )
    page.update()


def main(page: ft.Page, return_to="admin", email=None):
    print("🔁 match_results.main() called with:", return_to, email)
    if email is None and return_to != "admin":
        if return_to == "requester":
            import requester_login
            requester_login.main(page)
        elif return_to == "volunteer":
            import volunteer_login
            volunteer_login.main(page)
        return

    match_results_ui(page, return_to=return_to, email=email)
