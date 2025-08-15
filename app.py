import flet as ft
from database import init_db

import main_menu
import sign_in
import sign_up
import admin_login
import volunteer_profile
import request_form
import admin_dashboard

ROUTES = {
    "/": main_menu.main,
    "/login": sign_in.main,
    "/signup": sign_up.main,
    "/admin": admin_login.main,
    "/volunteer": volunteer_profile.main,
    "/request": request_form.main,
    "/admin-dashboard": admin_dashboard.main,
}

def app_main(page: ft.Page):
    page.title = "Skill-Based Volunteer Exchange"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"
    page.window_min_width = 900
    page.window_min_height = 640

    init_db()  # safe to call repeatedly; adds missing cols/tables if needed

    def route_change(e: ft.RouteChangeEvent):
        page.controls.clear()
        handler = ROUTES.get(page.route, main_menu.main)
        handler(page)
        page.update()

    page.on_route_change = route_change
    page.go("/")  # start at main menu

ft.app(target=app_main)
