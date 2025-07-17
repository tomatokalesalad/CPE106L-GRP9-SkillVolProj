import flet as ft

def main(page: ft.Page):
    page.title = "TEST APP"
    page.bgcolor = "#222222"
    page.add(ft.Text("HELLO FLET", size=30, color="white"))

ft.app(target=main)
