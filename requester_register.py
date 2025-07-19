import flet as ft
from database import add_requester, verify_login
import requester_sign_in
import main_menu  # 👈 This lets us go back to the main menu

def main(page: ft.Page):
    page.title = "Sign Up"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    name = ft.TextField(label="Name", width=300)
    email = ft.TextField(label="Email", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

    message = ft.Text(color="red")

    def handle_sign_up(e):
        user_name = name.value.strip()
        user_email = email.value.strip()
        user_password = password.value.strip()

        if not all([user_name, user_email, user_password]):
            message.value = "All fields are required."
            page.update()
            return

        try:
            if verify_login(user_email, user_password, "requester"):
                message.value = "Account already exists. Redirecting to login..."
                page.update()
                requester_sign_in.main(page)
                return

            add_requester(user_name, user_email, user_password)
            message.value = "Sign up successful! Redirecting to login..."
            page.update()
            requester_sign_in.main(page)

        except Exception as err:
            message.value = f"Error: {err}"
            page.update()

    def go_back(e):
        main_menu.main(page)

    form = ft.Column(
        [
            ft.Text("Sign Up", size=24, weight="bold"),
            name,
            email,
            password,
            ft.Row(
                [
                    ft.ElevatedButton(text="Sign Up", on_click=handle_sign_up),
                    ft.OutlinedButton(text="Back", on_click=go_back),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            message,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    page.add(form)
