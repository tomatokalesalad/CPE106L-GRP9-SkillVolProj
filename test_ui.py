import flet as ft

def main(page: ft.Page):
    page.title = "Flet Test App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def say_hello(e):
        name = name_field.value
        page.controls.append(ft.Text(f"Hello, {name}!"))
        page.update()

    name_field = ft.TextField(label="Your name", width=300)
    greet_button = ft.ElevatedButton(text="Say Hello", on_click=say_hello)

    page.add(
        ft.Column([
            ft.Text("Test App", size=32, weight=ft.FontWeight.BOLD),
            name_field,
            greet_button
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
