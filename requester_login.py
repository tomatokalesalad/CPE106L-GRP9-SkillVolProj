import flet as ft
from database import requester_exists
import requester_dashboard  # 👈 Make sure this file defines main(page, email)
import main_menu

def main(page: ft.Page):
    page.title = "Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email_field = ft.TextField(label="Enter your email", width=300)
    status_text = ft.Text("", color="red")

    def login_click(e):
        email = email_field.value.strip()
        if not email:
            status_text.value = "Please enter your email."
            page.update()
            return

        if requester_exists(email):
            page.session.set("user_email", email)
            requester_dashboard.main(page, email)  
        else:
            status_text.value = "Requester not found. Please sign up first."
            page.update()

    def go_back(e):
        main_menu.main(page)

    # UI layout
    page.controls.clear()
    page.add(
        ft.Column(
            controls=[
                ft.Text("Login", size=24, weight="bold"),
                email_field,
                ft.ElevatedButton("Login", on_click=login_click, width=200),
                ft.TextButton("Back", on_click=go_back),
                status_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )
    page.update()
