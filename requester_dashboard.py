import flet as ft
import main_menu
import match_results
import request_form

def main(page: ft.Page, name=None):
    print("📲 Entered requester_dashboard with name:", name)

    page.title = "Requester Dashboard"
    page.controls.clear()

    welcome_msg = f"Welcome, {name}!" if name else "Welcome!"

    def go_back(e):
        main_menu.main(page)

    def view_match_results(e):
        print("🔁 Redirecting to match_results from requester_dashboard with name:", name)
        match_results.main(page, return_to="requester", email=name)  # Correct arguments

    def create_new_request(e):
        request_form.main(page, name=name)

    layout = ft.Column(
        controls=[
            ft.Text(welcome_msg, size=28, weight=ft.FontWeight.BOLD),
            ft.Text("What would you like to do today?", size=20),
            ft.ElevatedButton("➕ Create New Help Request", on_click=create_new_request),
            ft.ElevatedButton("📄 View Match Results", on_click=view_match_results),
            ft.TextButton("← Back to Main Menu", on_click=go_back),
        ],
        spacing=25,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(layout)
    page.update()
