import flet as ft
from matcher import match_request_to_volunteer
from database import add_request
import requester_dashboard

def main(page: ft.Page):
    def go_back(e):
        import main_menu
        page.controls.clear()
        main_menu.main(page)
        page.update()

    def submit_request(e):
        name = name_field.value.strip()
        email = email_field.value.strip()
        location = location_field.value.strip()
        skill = skill_field.value.strip()
        availability = availability_field.value.strip()

        if not all([name, email, location, skill, availability]):
            page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields"))
            page.snack_bar.open = True
            page.update()
            return

        add_request(name, skill, location, availability, email)
        match_request_to_volunteer(name, skill, location, availability, email)
        requester_dashboard.main(page, email)  # ✅ navigate to dashboard

    name_field = ft.TextField(label="Name")
    email_field = ft.TextField(label="Email")
    location_field = ft.TextField(label="Location")
    skill_field = ft.TextField(label="Skill Needed")
    availability_field = ft.TextField(label="Availability")

    page.controls.clear()
    page.controls.extend([
        ft.Text("Help Request Form", size=20, weight="bold"),
        name_field,
        email_field,
        location_field,
        skill_field,
        availability_field,
        ft.Row([
            ft.ElevatedButton("Submit", on_click=submit_request),
            ft.TextButton("Back to Menu", on_click=go_back)
        ])
    ])
    page.update()
