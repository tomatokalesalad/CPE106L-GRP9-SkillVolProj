# main.py

import flet as ft
from main_menu import main as main_menu_main

def main(page: ft.Page):
    main_menu_main(page)

ft.app(target=main)
