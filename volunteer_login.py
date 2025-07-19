import flet as ft
from database import volunteer_exists
import volunteer_dashboard  # this should be your main dashboard after login
import main_menu

def main(page: ft.Page):
    page.title = "Volunteer Login"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email_field = ft.TextField(label="Enter your email", width=400)
    status_text = ft.Text("", color="red")

    def login(e):
        email = email_field.value.strip()
        if not email:
            status_text.value = "Please enter your email."
            page.update()
            return

        if not volunteer_exists(email):
            status_text.value = "Volunteer not found. Please sign up first."
            page.update()
            return

        page.session.set("user_email", email)
        volunteer_dashboard.volunteer_dashboard(page, email)

    def go_back(e):
        main_menu.main(page)

    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Volunteer Login", size=24, weight="bold"),
                email_field,
                ft.ElevatedButton("Login", on_click=login, width=200),
                ft.TextButton("Back", on_click=go_back),
                status_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )
    page.update()
