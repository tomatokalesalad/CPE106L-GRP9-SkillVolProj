import flet as ft
from main_menu import main
import database

def main_wrapper(page: ft.Page):
    database.init_db()
    main(page)

if __name__ == "__main__":
    ft.app(target=main_wrapper)
