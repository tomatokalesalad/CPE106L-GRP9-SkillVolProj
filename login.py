# login.py
import flet as ft
import sqlite3
import volunteer_dashboard
import requester_dashboard
import main_menu

DB_NAME = "skillvolunteer.db"

def check_email_exists(email, role):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    table = "users" if role == "Volunteer" else "requests"
    c.execute(f"SELECT * FROM {table} WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    return result is not None

def main(page: ft.Page):
    page.title = "Login"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT

    email_field = ft.TextField(label="Email", width=300)
    role_dropdown = ft.Dropdown(
        label="Login As",
        width=300,
        options=[
            ft.dropdown.Option("Volunteer"),
            ft.dropdown.Option("Requester")
        ]
    )

    def try_login(e):
        email = email_field.value.strip()
        role = role_dropdown.value

        if not email or not role:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter email and select role."))
            page.snack_bar.open = True
            page.update()
            return

        if not check_email_exists(email, role):
            page.snack_bar = ft.SnackBar(ft.Text("Account not found. Please register first."))
            page.snack_bar.open = True
            page.update()
            return

        # ✅ Redirect
        if role == "Volunteer":
            volunteer_dashboard.main(page, email)
        else:
            requester_dashboard.main(page, email)

    def go_back(e):
        main_menu.main(page)

    page.controls = [
        ft.Text("Login to Dashboard", size=20, weight="bold"),
        email_field,
        role_dropdown,
        ft.ElevatedButton("Login", on_click=try_login),
        ft.TextButton("Back to Menu", on_click=go_back),
    ]
    page.update()
