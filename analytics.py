import flet as ft

# Dummy credentials (you can store securely later)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Admin Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    error_text = ft.Text("", color="red")

    def login(e):
        if username.value == ADMIN_USERNAME and password.value == ADMIN_PASSWORD:
            import admin_dashboard
            admin_dashboard.main(page)
        else:
            error_text.value = "Invalid credentials"
            page.update()

    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Admin Login", size=30, weight=ft.FontWeight.BOLD),
                username,
                password,
                error_text,
                ft.ElevatedButton("Login", on_click=login),
                ft.ElevatedButton(
                    text="← Back to Main Menu",
                    width=180,
                    height=40,
                    bgcolor="#636e72",
                    color="white",
                    on_click=lambda e: __import__('main_menu').main(page),
                ),
            ],
            spacing=20,
            width=400,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    page.update()
