import flet as ft
from database import get_matches_for_requester

def main(page: ft.Page, email=None):
    page.controls.clear()
    em = email or page.session.get("user_email")

    rows = get_matches_for_requester(em)

    table_rows = [
        ft.DataRow(cells=[
            ft.DataCell(ft.Text(str(r["id"]))),
            ft.DataCell(ft.Text(r["request_name"])),
            ft.DataCell(ft.Text(r["volunteer_name"])),
            ft.DataCell(ft.Text(r["skill"])),
            ft.DataCell(ft.Text(f'{r["distance_km"]:.2f}' if r["distance_km"] is not None else "N/A")),
            ft.DataCell(ft.Text(r["created_at"])),
        ]) for r in rows
    ]

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Requester")),
            ft.DataColumn(ft.Text("Volunteer")),
            ft.DataColumn(ft.Text("Skill")),
            ft.DataColumn(ft.Text("Distance (km)")),
            ft.DataColumn(ft.Text("When")),
        ],
        rows=table_rows,
        column_spacing=18,
    )

    def back(e):
        import requester_dashboard
        requester_dashboard.main(page)

    layout = ft.Column(
        [ft.Text("Your Match Results", size=22, weight="bold"), table, ft.TextButton("← Back", on_click=back)],
        spacing=16, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(ft.Container(content=layout, expand=True, alignment=ft.alignment.center))
    page.update()
