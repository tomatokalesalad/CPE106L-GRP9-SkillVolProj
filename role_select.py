import flet as ft
from database import get_user_by_email
import requester_dashboard
import volunteer_dashboard
import main_menu

def main(page: ft.Page):
    page.controls.clear()
    em = page.session.get("user_email")
    user = get_user_by_email(em) if em else None
    name = user["name"] if user else "there"

    title = ft.Text(f"Welcome, {name}!", size=26, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("What would you like to do today?", size=16)

    def to_requester(e): requester_dashboard.main(page)
    def to_volunteer(e): volunteer_dashboard.main(page)
    def back(e): main_menu.main(page)

    btns = ft.Row(
        [
            ft.ElevatedButton("I need help", on_click=to_requester),
            ft.ElevatedButton("I want to volunteer", on_click=to_volunteer),
            ft.TextButton("Back to menu", on_click=back),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    layout = ft.Column([title, subtitle, btns],
        spacing=20, alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(ft.Container(content=layout, expand=True, alignment=ft.alignment.center))
    page.update()
