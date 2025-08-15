import flet as ft
from database import add_user, get_user_by_email, upsert_volunteer_profile, add_help_request, get_all_volunteers

# Updated skill list
SKILLS = ["Tutoring", "IT Support", "Counseling", "Translation", "Healthcare", "Other"]
LOCATIONS = ["Manila", "Quezon", "Alabang", "Pasay", "Makati", "Taguig", "Pasig"]
AVAIL = ["Weekdays", "Weekends", "Evenings", "Full-time", "Flexible"]
ROLES = ["Volunteer", "Requester"]

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Form fields
    name = ft.TextField(label="Full Name", width=320)
    email = ft.TextField(label="Email", width=320)
    password = ft.TextField(label="Password", width=320, password=True, can_reveal_password=True)
    role = ft.Dropdown(label="I am a…", width=320, options=[ft.dropdown.Option(r) for r in ROLES])

    # Skills dropdown with "Other" text field
    other_skill_field = ft.TextField(label="Please specify", width=320, visible=False)

    def skill_change(e):
        other_skill_field.visible = (skills.value == "Other")
        page.update()

    skills = ft.Dropdown(
        label="Skill",
        width=320,
        options=[ft.dropdown.Option(s) for s in SKILLS],
        on_change=skill_change
    )

    location = ft.Dropdown(label="Location", width=320, options=[ft.dropdown.Option(c) for c in LOCATIONS])
    availability = ft.Dropdown(label="Availability", width=320, options=[ft.dropdown.Option(a) for a in AVAIL])

    status = ft.Text("", color="red")

    def submit(e):
        n, em, pw, ro = name.value.strip(), email.value.strip(), password.value.strip(), role.value
        sk = other_skill_field.value.strip() if skills.value == "Other" else skills.value
        loc, av = location.value, availability.value

        # Validation
        if not all([n, em, pw, ro, sk, loc, av]):
            status.value = "Please complete all fields."
            page.update()
            return

        if get_user_by_email(em):
            status.value = "Email already exists. Please login."
            page.update()
            return

        # Create account
        add_user(n, em, pw, ro)
        page.session.set("user_email", em)
        page.session.set("user_name", n)
        page.session.set("user_role", ro)

        # Save profile based on role
        if ro == "Volunteer":
            upsert_volunteer_profile(em, n, sk, loc, av)
        else:
            add_help_request(n, em, sk, loc, av)

        # Check available matches (very simple: same skill)
        available_people = [v for v in get_all_volunteers() if v["skills"].lower() == sk.lower()]
        msg = f"Available person: {available_people[0]['name']}" if available_people else "No available match."

        def on_ok(_):
            page.dialog.open = False
            page.go("/")  # back to home

        page.dialog = ft.AlertDialog(
            title=ft.Text("Result"),
            content=ft.Text(msg),
            actions=[ft.TextButton("OK", on_click=on_ok)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()

    content = ft.Column(
        [
            ft.Text("Create Account", size=24, weight="bold"),
            name, email, password, role,
            skills, other_skill_field,
            location, availability,
            ft.Row(
                [
                    ft.ElevatedButton("Submit", on_click=submit),
                    ft.TextButton("Back to Home", on_click=lambda e: page.go("/")),
                ],
                alignment="center"
            ),
            status
        ],
        spacing=12, horizontal_alignment="center", alignment="center"
    )

    page.add(ft.Container(content=content, expand=True, alignment=ft.alignment.center))
