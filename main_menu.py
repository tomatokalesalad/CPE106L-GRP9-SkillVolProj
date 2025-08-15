import flet as ft

def main(page: ft.Page):
    greeting = ft.Text("Skill-Based Volunteer Exchange", size=28, weight="bold")
    subtitle = ft.Text("Empowering communities, one skill at a time", size=16, italic=True)

    btn_signin = ft.ElevatedButton("Sign In", width=220, on_click=lambda e: page.go("/login"))
    btn_signup = ft.ElevatedButton("Sign Up", width=220, on_click=lambda e: page.go("/signup"))
    btn_admin = ft.OutlinedButton("Admin Login", width=220, on_click=lambda e: page.go("/admin"))

    content = ft.Column(
        [greeting, subtitle, ft.Divider(opacity=0.3),
         btn_signin, btn_signup, ft.Container(height=20), btn_admin],
        spacing=15, alignment="center", horizontal_alignment="center"
    )

    page.add(ft.Container(content=content, expand=True, alignment=ft.alignment.center))
