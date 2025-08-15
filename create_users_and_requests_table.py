import flet as ft
import database  # Must have add_request() defined there
from main_menu import main as main_menu_main

def main(page: ft.Page):
    page.title = "Request Help"
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Fields
    name_field = ft.TextField(label="Your Name", width=250, filled=True, fill_color="#FFF8DC", text_align=ft.TextAlign.CENTER)
    skill_field = ft.TextField(label="Skill Needed", width=250, filled=True, fill_color="#FFF8DC", text_align=ft.TextAlign.CENTER)
    desc_field = ft.TextField(label="Short Description", width=250, multiline=True, min_lines=3, filled=True, fill_color="#FFF8DC")
    location_field = ft.TextField(label="Location", width=250, filled=True, fill_color="#FFF8DC", text_align=ft.TextAlign.CENTER)
    availability_field = ft.Dropdown(
        label="Preferred Time",
        width=250,
        options=[
            ft.dropdown.Option("Weekdays"),
            ft.dropdown.Option("Weekends"),
            ft.dropdown.Option("Evening"),
            ft.dropdown.Option("Full-time"),
            ft.dropdown.Option("Flexible"),
        ],
    )

    def submit_handler(e):
        name = name_field.value.strip()
        skill = skill_field.value.strip()
        desc = desc_field.value.strip()
        location = location_field.value.strip()
        availability = availability_field.value

        if not name or not skill or not desc or not location or not availability:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Please complete all fields.", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        # Save to database
        database.add_request(name, skill, desc, location, availability)

        def on_ok(_):
            page.dialog.open = False
            page.controls.clear()
            main_menu_main(page)

        page.dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text("Your help request has been submitted!"),
            actions=[ft.TextButton("OK", on_click=on_ok)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()

    def go_back(e):
        page.controls.clear()
        main_menu_main(page)

    form = ft.Column(
        controls=[
            ft.Row([ft.ElevatedButton("← Back", on_click=go_back)], alignment=ft.MainAxisAlignment.START),
            ft.Text("Submit Help Request", size=26, weight=ft.FontWeight.BOLD, color="white"),
            name_field,
            skill_field,
            desc_field,
            location_field,
            availability_field,
            ft.ElevatedButton("Submit Request", on_click=submit_handler)
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    background = ft.Container(
        content=form,
        expand=True,
        bgcolor=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#E0FFFF", "#90EE90"]
        ),
        padding=30,
        alignment=ft.alignment.center,
    )

    page.controls.clear()
    page.add(background)
    page.update()
