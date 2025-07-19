import flet as ft
from database import verify_login
import requester_dashboard

def main(page: ft.Page):
    page.title = "Sign In"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email = ft.TextField(label="Email", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

    message = ft.Text(color="red")

    def handle_sign_in(e):
        user_email = email.value.strip()
        user_password = password.value.strip()

        if not all([user_email, user_password]):
            message.value = "Email and password are required."
            page.update()
            return

        try:
            if verify_login(user_email, user_password, "requester"):
                message.value = "Login successful!"
                page.session.set("user_email", user_email)
                page.update()
                requester_dashboard.main(page)
            else:
                message.value = "Invalid credentials. Try again."
                page.update()

        except Exception as err:
            message.value = f"Error: {err}"
            page.update()

    form = ft.Column(
        [
            ft.Text("Sign In", size=24, weight="bold"),
            email,
            password,
            ft.ElevatedButton(text="Sign In", on_click=handle_sign_in),
            message,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(form)
