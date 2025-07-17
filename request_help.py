import flet as ft
from matcher import match_request_to_volunteer
from database import add_request

def main(page: ft.Page):
    def go_back(e):
        import main_menu
        main_menu.main(page)

    def submit_request(e):
        name = name_field.value.strip()
        email = email_field.value.strip()
        location = location_field.value.strip()
        skill = skill_field.value.strip()
        availability = availability_field.value.strip()

        if not all([name, email, location, skill, availability]):
            result_text.value = "❗ Please fill in all fields."
            page.update()
            return

        # Add to DB with email
        add_request(name, skill, location, availability, email=email)

        # Try to match with a volunteer
        match = match_request_to_volunteer(name, skill, location, availability)

        if match:
            volunteer_name, distance = match
            result_text.value = f"✅ Matched with {volunteer_name} ({distance:.1f} km away)"
        else:
            result_text.value = "❌ No matching volunteer found at the moment."

        page.update()

    # Clear page
    page.controls.clear()

    page.appbar = ft.AppBar(
        title=ft.Text("Request Help"),
        bgcolor="#2E7D32"
    )

    # Input fields
    name_field = ft.TextField(label="Full Name", width=400)
    email_field = ft.TextField(label="Email Address", width=400)
    location_field = ft.TextField(label="Location", width=400)
    skill_field = ft.TextField(label="Describe the Help You Need", multiline=True, min_lines=2, max_lines=4, width=400)
    availability_field = ft.TextField(label="Preferred Schedule", width=400)
    result_text = ft.Text("", color="white", size=16)

    layout = ft.Column(
        [
            ft.Text("Request Help", size=24, weight=ft.FontWeight.BOLD, color="white"),
            name_field,
            email_field,
            location_field,
            skill_field,
            availability_field,
            ft.ElevatedButton(text="Submit", width=150, on_click=submit_request),
            result_text,
            ft.TextButton(text="Back", on_click=go_back),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    container = ft.Container(
        expand=True,
        content=layout,
        padding=30,
        alignment=ft.alignment.center,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#044BA7", "#89ABC7"]  # Cool blue gradient
        ),
    )

    page.add(container)
    page.update()
