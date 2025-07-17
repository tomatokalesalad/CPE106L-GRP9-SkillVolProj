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

    # ORIGINAL layout restored
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
                width=200,
                height=50,
                bgcolor="#4CAF50",
                color="white",
                on_click=go_to_register,
            ),
            ft.ElevatedButton(
                text="Request Help",  # ✅ This is the ONLY addition
                width=200,
                height=50,
                bgcolor="#2196F3",
                color="white",
                on_click=go_to_request,
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
            colors=["#00BFFF", "#228B22"],  # ✅ Sky blue to forest green, as you asked before
        ),
    )

    page.controls.clear()
    page.add(bg)
    page.update()
