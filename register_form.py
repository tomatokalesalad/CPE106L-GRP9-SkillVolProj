import flet as ft
from database import add_volunteer

def main(page: ft.Page):
    def go_back(e):
        import main_menu
        main_menu.main(page)

    def submit_registration(e):
        name = name_field.value.strip()
        email = email_field.value.strip()
        location = location_field.value.strip()
        skills = skills_field.value.strip()
        availability = availability_field.value.strip()

        if not all([name, email, location, skills, availability]):
            result_text.value = "❗ Please fill in all fields."
            page.update()
            return

        add_volunteer(name, skills, location, availability, email=email)
        result_text.value = "✅ Registered successfully!"
        page.update()

    # Clear page
    page.controls.clear()

    page.appbar = ft.AppBar(
        title=ft.Text("Volunteer Registration"),
        bgcolor="#2E7D32"
    )

    name_field = ft.TextField(label="Full Name", width=400)
    email_field = ft.TextField(label="Email Address", width=400)
    location_field = ft.TextField(label="Location", width=400)
    skills_field = ft.TextField(label="Skills / Services You Offer", multiline=True, min_lines=2, max_lines=4, width=400)
    availability_field = ft.TextField(label="Availability", width=400)
    result_text = ft.Text("", color="white", size=16)

    layout = ft.Column(
        [
            ft.Text("Volunteer Registration", size=24, weight=ft.FontWeight.BOLD, color="white"),
            name_field,
            email_field,
            location_field,
            skills_field,
            availability_field,
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
            colors=["#044b04", "#59A059"]  # Forest green gradient
        ),
    )

    page.add(container)
    page.update()
