import flet as ft
from database import get_user_by_email, find_matches_for_user

def main(page: ft.Page):
    page.controls.clear()
    em = page.session.get("user_email")
    user = get_user_by_email(em) if em else None
    name = user["name"] if user else "Requester"

    title = ft.Text(f"Requester Dashboard — Hi, {name}!", size=22, weight="bold")

    # Show matches
    matches = find_matches_for_user(em)
    if matches:
        match_list = ft.Column([
            ft.Text("📌 Matching Volunteers:", size=18, weight="bold")
        ] + [
            ft.Text(f"{m['name']} — {m['email']} — {m['skills']} — {m['availability']} — {m['location']}")
            for m in matches
        ])
    else:
        match_list = ft.Text("No matching volunteers found at the moment.", color="red")

    layout = ft.Column(
        [
            title,
            match_list
        ],
        spacing=18, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.add(ft.Container(content=layout, expand=True, alignment=ft.alignment.center))
    page.update()
