import flet as ft

def main(page: ft.Page):
    page.title = "Skill-Based Volunteer Exchange"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def go_to_volunteer_register(e):
        if page.session.get("user_email"):
            import register_form
            page.controls.clear()
            register_form.main(page)
            page.update()
        else:
            import requester_login
            page.controls.clear()
            requester_login.main(page)
            page.update()

    def go_to_request_form(e):
        if page.session.get("user_email"):
            import request_form
            page.controls.clear()
            request_form.main(page)
            page.update()
        else:
            import requester_login
            page.controls.clear()
            requester_login.main(page)
            page.update()

    def go_to_requester_login(e):
        import requester_login
        page.controls.clear()
        requester_login.main(page)
        page.update()

    def go_to_requester_register(e):
        import requester_register
        page.controls.clear()
        requester_register.main(page)
        page.update()

    def go_to_matches(e):
        import match_results
        page.controls.clear()
        match_results.main(page, return_to="main")
        page.update()

    def go_to_admin_login(e):
        import admin_login
        page.controls.clear()
        admin_login.main(page)
        page.update()

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
            ft.Container(height=30),
            ft.ElevatedButton(
                text="Request Help",
                width=220,
                height=50,
                bgcolor="#e66767",
                color="white",
                on_click=go_to_request_form,
            ),
            ft.ElevatedButton(
                text="Become a Volunteer",
                width=220,
                height=50,
                bgcolor="#546de5",
                color="white",
                on_click=go_to_volunteer_register,
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
            ft.Container(height=20),
            ft.Text("Already a requester?", color="white70"),
            ft.Row(
                [
                    ft.ElevatedButton(
                        text="Login",
                        width=120,
                        bgcolor="#009688",
                        color="white",
                        on_click=go_to_requester_login,
                    ),
                    ft.ElevatedButton(
                        text="Sign Up",
                        width=120,
                        bgcolor="#00b894",
                        color="white",
                        on_click=go_to_requester_register,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
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
