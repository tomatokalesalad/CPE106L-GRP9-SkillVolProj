import flet as ft
import sqlite3

def fetch_match_logs():
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()
    cursor.execute("SELECT requester_name, volunteer_name, skill, distance_km, timestamp FROM match_logs")
    logs = cursor.fetchall()
    conn.close()
    return logs

def main(page: ft.Page):
    page.title = "Match History"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    def go_back(e):
        __import__("admin_dashboard").main(page)

    logs = fetch_match_logs()

    # Table header
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Requester")),
            ft.DataColumn(ft.Text("Volunteer")),
            ft.DataColumn(ft.Text("Skill")),
            ft.DataColumn(ft.Text("Distance (km)")),
            ft.DataColumn(ft.Text("Timestamp")),
        ],
        rows=[]
    )

    # Populate rows
    for log in logs:
        table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(log[0])),
                    ft.DataCell(ft.Text(log[1])),
                    ft.DataCell(ft.Text(log[2])),
                    ft.DataCell(ft.Text(str(log[3]))),
                    ft.DataCell(ft.Text(log[4])),
                ]
            )
        )

    page.controls.clear()
    page.add(
        ft.Column([
            ft.Text("Match History", size=28, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            table,
            ft.Container(height=30),
            ft.ElevatedButton("Back to Dashboard", on_click=go_back)
        ])
    )
    page.update()
