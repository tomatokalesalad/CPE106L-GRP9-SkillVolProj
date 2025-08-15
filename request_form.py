import flet as ft
from database import add_help_request, get_user_by_email
from matcher import match_request_to_volunteer

SKILLS = ["Tutoring", "IT Support", "Counseling", "Translation", "Healthcare", "Other"]
LOCATIONS = ["Manila", "Quezon", "Alabang", "Pasay", "Makati", "Taguig", "Pasig"]
AVAIL = ["Weekdays", "Weekends", "Evening", "Full-time", "Flexible"]

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    em = page.session.get("user_email") or ""
    user = get_user_by_email(em) or {}

    name = ft.TextField(label="Full Name", width=320, value=user.get("name",""))
    email = ft.TextField(label="Email", width=320, value=em, read_only=True)

    skills = ft.Dropdown(label="Skill Needed", width=320, options=[ft.dropdown.Option(s) for s in SKILLS])
    location = ft.Dropdown(label="Location", width=320, options=[ft.dropdown.Option(c) for c in LOCATIONS])
    availability = ft.Dropdown(label="Availability", width=320, options=[ft.dropdown.Option(a) for a in AVAIL])

    status = ft.Text("", color="green")

    def submit(e):
        if not all([name.value.strip(), email.value.strip(), skills.value, location.value, availability.value]):
            status.value = "Please complete all fields."
            status.color = "red"
            page.update(); return

        add_help_request(name.value.strip(), email.value.strip(), skills.value, location.value, availability.value)
        # try to match instantly
        match_request_to_volunteer(email.value.strip())
        status.value = "✅ Help request submitted. Matching attempted."
        status.color = "green"
        page.update()

    content = ft.Column(
        [
            ft.Text(f"Welcome, {user.get('name') or 'Requester'}!", size=22, weight="bold"),
            name, email, skills, location, availability,
            ft.Row([ft.ElevatedButton("Submit", on_click=submit)], alignment="center"),
            ft.Row([ft.TextButton("Back to Home", on_click=lambda e: page.go("/"))], alignment="center"),
            status
        ],
        spacing=12, horizontal_alignment="center", alignment="center"
    )
    page.add(ft.Container(content=content, expand=True, alignment=ft.alignment.center))
