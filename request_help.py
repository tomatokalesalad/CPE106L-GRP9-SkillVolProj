import flet as ft
import database
from main_menu import main as main_menu_main

def main(page: ft.Page):
    page.title = "Request Help"
    page.theme = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#4682b4",
        secondary="#006994",
    )
)

    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    name_field = ft.TextField(label="Your Name", width=250, filled=True, fill_color="#4682b4", text_align=ft.TextAlign.CENTER)

    skill_dropdown = ft.Dropdown(
        label="Skill Needed",
        width=250,
        options=[
            ft.dropdown.Option("Tutoring"),
            ft.dropdown.Option("Repairs"),
            ft.dropdown.Option("Cooking"),
            ft.dropdown.Option("Tech Support"),
            ft.dropdown.Option("Others: Specify below"),
        ]
    )

    other_skill_field = ft.TextField(label="Specify Skill", width=250, filled=True, visible=False)

    availability_dropdown = ft.Dropdown(
        label="When do you need help?",
        width=250,
        options=[
            ft.dropdown.Option("Morning"),
            ft.dropdown.Option("Afternoon"),
            ft.dropdown.Option("Evening"),
            ft.dropdown.Option("Weekends"),
        ]
    )

    location_field = ft.TextField(label="Your Location", width=250, filled=True, fill_color="#FFF", text_align=ft.TextAlign.CENTER)

    def skill_changed(e):
        other_skill_field.visible = (skill_dropdown.value == "Others: Specify below")
        page.update()

    skill_dropdown.on_change = skill_changed

    def submit_handler(e):
        name = name_field.value.strip()
        skill = other_skill_field.value.strip() if skill_dropdown.value == "Others: Specify below" else skill_dropdown.value
        availability = availability_dropdown.value
        location = location_field.value.strip()

        if not name or not skill or not availability or not location:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please fill out all fields!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        database.add_request(name, skill, location, availability)

        def on_done(_):
            page.dialog.open = False
            page.controls.clear()
            main_menu_main(page)

        page.dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text("Help request submitted!"),
            actions=[ft.TextButton("OK", on_click=on_done)],
        )
        page.dialog.open = True
        page.update()

    def go_back(e):
        page.controls.clear()
        main_menu_main(page)

    form = ft.Column(
        [
            ft.Row([ft.ElevatedButton("← Back", on_click=go_back)], alignment=ft.MainAxisAlignment.START),
            ft.Text("Request Help", size=28, weight=ft.FontWeight.BOLD, color="white"),
            name_field,
            skill_dropdown,
            other_skill_field,
            availability_dropdown,
            location_field,
            ft.ElevatedButton("Submit Request", on_click=submit_handler),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    bg = ft.Container(
        content=form,
        expand=True,
        alignment=ft.alignment.center,
        padding=30,
        bgcolor=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#87CEEB", "#228B22"]
        )
    )

    page.controls.clear()
    page.add(bg)
    page.update()
