import flet as ft
from database import init_db           # ✅ correct import

def main_wrapper(page: ft.Page):
    # launch the main menu (or whatever your entry screen is)
    import main_menu
    main_menu.main(page)

if __name__ == "__main__":
    init_db()                          # ✅ creates all tables if missing
    ft.app(target=main_wrapper)
