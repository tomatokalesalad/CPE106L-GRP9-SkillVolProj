import flet as ft

def main(page: ft.Page):
    page.title = "Test Page"
    page.add(
        ft.Text("If you see this, Flet works!", size=30, color="blue")
    )

if __name__ == "__main__":
    ft.app(target=main)
