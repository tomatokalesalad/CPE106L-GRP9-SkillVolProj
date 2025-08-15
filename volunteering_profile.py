import flet as ft
from database import get_user_by_email, upsert_volunteer_profile

# Skills and availability options
SKILLS = ["Tutoring", "IT Support", "Counseling", "Translation", "Healthcare", "Other"]
LOCATIONS = ["Manila", "Quezon", "Alabang", "Pasay", "Makati", "Taguig", "Pasig"]
AVAIL = ["Weekdays", "Weekends", "Evening", "Full-time", "Flexible"]

def main(page: ft.Page):
    page.title = "Volunteer Profile"
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Load logged-in user
    em = page.session.get("user_email") or ""
    user = get_user_by_email(em) or {}

    # Pre-fill dropdowns with stored values
    current_skills = user.get("skills", "")
    current_avail = user.get("availability", "")
    current_location = user.get("location", "")

    name = ft.TextField(label="Full Name", width=320, value=user.get("name", ""), read_only=True)
    email = ft.TextField(label="Email", width=320, value=em, read_only=True)

    skills = ft.Dropdown(
        label="Skills",
        width=320,
        value=current_skills if current_skills in SKILLS else None,
        options=[ft.dropdown.Option(s) for s in SKILLS]
    )

    location = ft.Dropdown(
        label="Location",
        width=320,
        value=current_location if current_location in LOCATIONS else None,
        options=[ft.dropdown.Option(l) for l in LOCATIONS]
    )

    availability = ft.Dropdown(
        label="Availability",
        width=320,
        value=current_avail if current_avail in AVAIL else None,
        options=[ft.dropdown.Option(a) for a in AVAIL]
    )

    status = ft.Text("", color="green")

    # Save/Update profile
    def save_profile(e):
        if not (skills.value and availability.value and location.value):
            status.value = "Please select skills, location, and availability."
            status.color = "red"
            page.update()
            return

        upsert_volunteer_profile(
            email=email.value,
            name=name.value,
            skills=skills.value,
            location=location.value,
            availability=availability.value
        )
        status.value = f"✅ Profile saved! (Skills: {skills.value}, Location: {location.value}, Availability: {availability.value})"
        status.color = "green"
        page.update()

    content = ft.Column(
        [
            ft.Text("Volunteer Profile", size=26, weight="bold", color="white"),
            name,
            email,
            skills,
            location,
            availability,
            ft.Row([ft.ElevatedButton("Save Profile", on_click=save_profile)], alignment="center"),
            ft.Row([ft.TextButton("Back to Home", on_click=lambda e: page.go("/"))], alignment="center"),
            status
        ],
        spacing=12,
        horizontal_alignment="center"
    )

    page.controls.clear()
    page.add(
        ft.Container(
            content=content,
            expand=True,
            alignment=ft.alignment.center
        )
    )
    page.update()
