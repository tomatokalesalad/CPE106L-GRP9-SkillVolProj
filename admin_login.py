import flet as ft

# Fallback static credentials
ADMIN_FALLBACK_USER = "admin"
ADMIN_FALLBACK_PASS = "1234"

# Try to import database login function if available
try:
    from database import verify_login as _verify_login
except ImportError:
    _verify_login = None

def _is_valid_admin(username: str, password: str) -> bool:
    # 1. Fallback direct check
    if username.strip() == ADMIN_FALLBACK_USER and password.strip() == ADMIN_FALLBACK_PASS:
        return True

    # 2. If DB login is available, check it
    if _verify_login:
        try:
            user = _verify_login(username.strip(), password.strip())
            if user and (user.get("role") or "").lower() == "admin":
                return True
        except Exception:
            pass

    return False

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.title = "Admin Login"

    username = ft.TextField(label="Admin Username", width=320)
    password = ft.TextField(label="Admin Password", width=320, password=True, can_reveal_password=True)
    status = ft.Text("", color="red")

    def submit(e):
        if _is_valid_admin(username.value, password.value):
            import admin_dashboard
            admin_dashboard.main(page)
        else:
            status.value = "Invalid admin credentials."
            page.update()

    content = ft.Column(
        [
            ft.Text("Admin Login", size=24, weight="bold"),
            username,
            password,
            ft.Row([ft.ElevatedButton("Login", on_click=submit)], alignment="center"),
            ft.Row([ft.TextButton("Back to Home", on_click=lambda e: page.go("/"))], alignment="center"),
            status
        ],
        spacing=12, horizontal_alignment="center", alignment="center"
    )
    page.controls.clear()
    page.add(ft.Container(content=content, expand=True, alignment=ft.alignment.center))
    page.update()
