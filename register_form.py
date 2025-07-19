import flet as ft
from database import add_volunteer

def main(page: ft.Page, email=None):  # 💡 Accept logged-in email
    def go_back(e):
        import main_menu
        main_menu.main(page)

    def submit_registration(e):
        name = name_field.value.strip()
        location = location_field.value.strip()
        skills = skills_dropdown.value
        availability = availability_dropdown.value

        if not all([name, location, skills, availability]):
            result_text.value = "❗ Please fill in all fields."
            page.update()
            return

        add_volunteer(name, skills, location, availability, email=email)
        result_text.value = "✅ Registered successfully!"
        page.update()

    # Clear page
    page.controls.clear()

    name_field = ft.TextField(label="Full Name", width=400)
    location_field = ft.TextField(label="Location", width=400)

    # ✅ Skills Dropdown
    skills_dropdown = ft.Dropdown(
        label="Skills / Services You Offer",
        width=400,
        options=[
            ft.dropdown.Option("Tutoring"),
            ft.dropdown.Option("IT Support"),
            ft.dropdown.Option("Counseling"),
            ft.dropdown.Option("Translation"),
            ft.dropdown.Option("Healthcare"),
            ft.dropdown.Option("Construction"),
            ft.dropdown.Option("Other"),
        ],
    )

    # ✅ Availability Dropdown
    availability_dropdown = ft.Dropdown(
        label="Availability",
        width=400,
        options=[
            ft.dropdown.Option("Weekdays"),
            ft.dropdown.Option("Weekends"),
            ft.dropdown.Option("Evenings"),
            ft.dropdown.Option("Full-Time"),
            ft.dropdown.Option("Flexible"),
        ],
    )

    result_text = ft.Text("", color="white", size=16)

    email_field = ft.TextField(label="Email Address", width=400, value=email or "", read_only=True)

    layout = ft.Column(
        [
            ft.Text("Volunteer Registration", size=24, weight=ft.FontWeight.BOLD, color="white"),
            name_field,
            email_field,
            location_field,
            skills_dropdown,
            availability_dropdown,
            ft.ElevatedButton(text="Submit", width=150, on_click=submit_registration),
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
            colors=["#7153CA", "#5A0377"]  # Forest green gradient
        ),
    )

    page.add(container)
    page.update()
