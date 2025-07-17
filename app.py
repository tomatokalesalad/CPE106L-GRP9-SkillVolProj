import flet as ft
from main_menu import main

def main_wrapper(page: ft.Page):
    print(">>> Loading app...")
    main(page)  # This should load the UI

if __name__ == "__main__":
    ft.app(target=main_wrapper)
