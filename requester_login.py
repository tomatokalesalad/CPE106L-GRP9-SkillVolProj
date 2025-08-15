import flet as ft
from database import requester_exists, get_user_by_email
import requester_dashboard
import main_menu

SKILLS = ["Tutoring", "IT Support", "Counseling", "Translation", "Healthcare", "Other"]

def main(page: ft.Page):
    page.title = "Requester Login"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email_field = ft.TextField(label="Enter your email", width=400)
    status_text = ft.Text("", color="red", size=16)

    def login(e):
        email = email_field.value.strip()
        if not email:
            status_text.value = "Please enter your email."
            page.update()
            return

        if not requester_exists(email):
            status_text.value = "Requester not found. Please sign up first."
            page.update()
            return

        user = get_user_by_email(email)
        page.session.set("user_email", email)

        # Show role message
        role_msg = ft.SnackBar(ft.Text(f"✅ Welcome! You are logged in as Requester (Needing Help).", size=16))
        page.snack_bar = role_msg
        page.snack_bar.open = True
        page.update()

        requester_dashboard.main(page)

    def go_back(e):
        main_menu.main(page)

    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Requester Login", size=26, weight="bold", color="white"),
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
