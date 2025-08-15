import flet as ft
from database import verify_login, record_sign_in

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    email = ft.TextField(label="Email", width=320)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=320)
    status = ft.Text("", color="red")

    def submit(e):
        em = email.value.strip()
        pw = password.value.strip()
        if not em or not pw:
            status.value = "Please fill in all fields."
            page.update(); return

        user = verify_login(em, pw)
        if not user:
            status.value = "Invalid email or password."
            page.update(); return

        # Store session for greetings/navigation
        page.session.set("user_email", user["email"])
        page.session.set("user_name", user.get("name") or "")
        page.session.set("user_role", user.get("role") or "")
        record_sign_in(user["email"])

        role = (user.get("role") or "").lower()
        if role == "volunteer":
            page.go("/volunteer")
        elif role == "requester":
            page.go("/request")
        elif role == "admin":
            page.go("/admin-dashboard")
        else:
            status.value = "Role not recognized."
            page.update()

    content = ft.Column(
        [
            ft.Text("Login", size=24, weight="bold"),
            email,
            password,
            ft.Row([ft.ElevatedButton("Sign In", on_click=submit)], alignment="center"),
            ft.Row([ft.TextButton("Back to Home", on_click=lambda e: page.go("/"))],
                   alignment="center"),
            status
        ],
        spacing=14, horizontal_alignment="center", alignment="center"
    )
    page.add(ft.Container(content=content, expand=True, alignment=ft.alignment.center))
