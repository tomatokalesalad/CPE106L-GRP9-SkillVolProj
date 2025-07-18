import flet as ft

def main(page: ft.Page):
    page.title = "Skill-Based Volunteer Exchange"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def go_to_register(e):
        import register_form
        register_form.main(page)

    def go_to_request(e):
        import request_help
        request_help.main(page)

    def go_to_matches(e):
        import match_results
        match_results.main(page)

    def go_to_admin_login(e):
        import admin_login
        admin_login.main(page)

    layout = ft.Column(
        controls=[
            ft.Text(
                "Skill-Based Volunteer Exchange",
                size=36,
                weight=ft.FontWeight.BOLD,
                color="white",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Empowering communities, one skill at a time",
                size=18,
                italic=True,
                color="white70",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=40),
            ft.ElevatedButton(
                text="Become a Volunteer",
                width=220,
                height=50,
                bgcolor="#546de5",
                color="white",
                on_click=go_to_register,
            ),
            ft.ElevatedButton(
                text="Request Help",
                width=220,
                height=50,
                bgcolor="#e66767",
                color="white",
                on_click=go_to_request,
            ),
            ft.ElevatedButton(
                text="View Match Results",
                width=220,
                height=50,
                bgcolor="#6A1B9A",
                color="white",
                on_click=go_to_matches,
            ),
            ft.ElevatedButton(
                text="🛠 Admin Dashboard",
                width=220,
                height=50,
                bgcolor="#303952",
                color="white",
                on_click=go_to_admin_login,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=25,
    )

    bg = ft.Container(
        content=layout,
        expand=True,
        padding=50,
        alignment=ft.alignment.center,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#574b90", "#f5cd79"], 
        ),
    )

    page.controls.clear()
    page.add(bg)
    page.update()
