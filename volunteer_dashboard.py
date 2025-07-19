import flet as ft

def volunteer_dashboard(page, name):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Volunteer Dashboard"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def view_matches(e):
        import match_results
        match_results.main(page)

    def logout(e):
        import main_menu
        main_menu.main(page)

    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text(f"Welcome, {name}!", size=28, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("View Match Results", on_click=view_matches, width=200),
                ft.ElevatedButton("Logout", on_click=logout, width=200, bgcolor="#d63031", color="white")
            ],
            spacing=25,
            alignment=ft.MainAxisAlignment.CENTER,
            width=300
        )
    )

    page.update()
