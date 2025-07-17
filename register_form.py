import flet as ft
import database
from main_menu import main as main_menu_main

def main(page: ft.Page):
    page.title = "Volunteer Registration"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Input Fields
    full_name_field = ft.TextField(label="Full Name", width=250, filled=True, fill_color="#B0E0E6", text_align=ft.TextAlign.CENTER)

    skills_dropdown = ft.Dropdown(
        label="Skills",
        width=250,
        options=[
            ft.dropdown.Option("Tutoring"),
            ft.dropdown.Option("Repairs"),
            ft.dropdown.Option("Cooking"),
            ft.dropdown.Option("Tech Support"),
            ft.dropdown.Option("Others: Specify below"),
        ],
    )

    other_skills_field = ft.TextField(label="If Others, specify skill", width=250, filled=True, fill_color="#B0E0E6", text_align=ft.TextAlign.CENTER, visible=False)

    availability_dropdown = ft.Dropdown(
        label="Availability",
        width=250,
        options=[
            ft.dropdown.Option("Morning"),
            ft.dropdown.Option("Afternoon"),
            ft.dropdown.Option("Evening"),
            ft.dropdown.Option("Weekends"),
        ],
    )

    location_field = ft.TextField(label="Location", width=250, filled=True, fill_color="#B0E0E6", text_align=ft.TextAlign.CENTER)

    # Dropdown logic
    def skills_changed(e):
        other_skills_field.visible = (skills_dropdown.value == "Others: Specify below")
        page.update()

    skills_dropdown.on_change = skills_changed

    def go_back(e):
        page.controls.clear()
        main_menu_main(page)

    # ✅ Submit Handler must be inside `main()`
    def submit_handler(e):
        full_name = full_name_field.value.strip()
        skills = other_skills_field.value.strip() if skills_dropdown.value == "Others: Specify below" else skills_dropdown.value
        availability = availability_dropdown.value
        location = location_field.value.strip()

        if not full_name or not skills or not availability or not location:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Please fill all fields", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            database.add_user(full_name, skills, location, availability)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Database error: {ex}", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        def on_continue(_):
            page.dialog.open = False
            page.controls.clear()
            main_menu_main(page)

        page.dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text("You are registered successfully!"),
            actions=[ft.TextButton("Continue", on_click=on_continue)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    # Layout
    form_content = ft.Column(
        [
            ft.Row([ft.ElevatedButton("← Back", width=90, on_click=go_back)], alignment=ft.MainAxisAlignment.START),
            ft.Text("Register as Volunteer", size=28, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
            full_name_field,
            skills_dropdown,
            other_skills_field,
            availability_dropdown,
            location_field,
            ft.ElevatedButton("Submit", width=120, on_click=submit_handler),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Background
    background = ft.Container(
        content=form_content,
        expand=True,
        bgcolor=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#87CEEB", "#228B22"]
        ),
        alignment=ft.alignment.center,
        padding=30,
    )

    page.controls.clear()
    page.add(background)
    page.update()
