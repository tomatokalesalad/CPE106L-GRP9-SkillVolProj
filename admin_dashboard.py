import flet as ft
import sqlite3
import matplotlib
matplotlib.use("Agg")  # Prevent GUI backend error
import matplotlib.pyplot as plt
from uuid import uuid4
import base64
import pandas as pd
from io import BytesIO
from match_results import match_results_ui


def get_summary_data():
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_volunteers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM requests")
    total_requests = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM matches")
    total_matches = cursor.fetchone()[0]

    cursor.execute("SELECT skills, COUNT(*) FROM users GROUP BY skills")
    skill_data = cursor.fetchall()

    conn.close()
    return total_volunteers, total_requests, total_matches, skill_data


def generate_pie_chart_base64(skill_data):
    labels = [row[0] for row in skill_data]
    sizes = [row[1] for row in skill_data]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Skills Distribution")
    plt.axis("equal")

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    img_bytes = buffer.read()
    return base64.b64encode(img_bytes).decode("utf-8")


def export_data(skill_data):
    df = pd.DataFrame(skill_data, columns=["Skill", "Count"])
    csv_path = "skills_export.csv"
    pdf_path = "skills_export.pdf"

    df.to_csv(csv_path, index=False)

    plt.figure(figsize=(6, 4))
    plt.bar(df["Skill"], df["Count"])
    plt.title("Skill Summary")
    plt.tight_layout()
    plt.savefig(pdf_path)
    plt.close()

    return csv_path, pdf_path


def load_users():
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, skills, location, availability FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def delete_user(user_id, page):
    conn = sqlite3.connect("skillvolunteer.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    page.snack_bar = ft.SnackBar(ft.Text(f"✅ User {user_id} deleted!"))
    page.snack_bar.open = True
    page.update()
    main(page)  # refresh dashboard


def add_user_dialog(page):
    name = ft.TextField(label="Name")
    email = ft.TextField(label="Email")
    skills = ft.TextField(label="Skills")
    location = ft.TextField(label="Location")
    availability = ft.TextField(label="Availability")

    def submit_add_user(e):
        conn = sqlite3.connect("skillvolunteer.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, skills, location, availability)
            VALUES (?, ?, ?, ?, ?)
        """, (name.value, email.value, skills.value, location.value, availability.value))
        conn.commit()
        conn.close()
        dlg.open = False
        page.update()
        main(page)

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("➕ Add New User"),
        content=ft.Column([name, email, skills, location, availability], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dlg, "open", False)),
            ft.TextButton("Add", on_click=submit_add_user),
        ],
    )
    page.dialog = dlg
    dlg.open = True
    page.update()


def main(page: ft.Page):
    page.title = "Admin Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    total_volunteers, total_requests, total_matches, skill_data = get_summary_data()
    pie_base64 = generate_pie_chart_base64(skill_data)

    summary = ft.Column([
        ft.Text("📊 Admin Summary Dashboard", size=30, weight=ft.FontWeight.BOLD),
        ft.Text(f"✅ Total Volunteers: {total_volunteers}", size=18),
        ft.Text(f"📩 Total Requests: {total_requests}", size=18),
        ft.Text(f"🤝 Total Matches: {total_matches}", size=18),
        ft.Text("Skill Distribution", size=20, weight=ft.FontWeight.BOLD),
        ft.Image(src_base64=pie_base64, width=400),
        ft.ElevatedButton("📄 View Match History", on_click=lambda e: match_results_ui(page))
    ], spacing=10)

    users = load_users()
    user_controls = [
        ft.Text("👥 Manage Users", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(thickness=1, color="gray"),
    ]

    for user in users:
        user_id, name, email, skills, location, availability = user
        user_controls.append(
            ft.Row([
                ft.Text(f"{name} | {skills} | {location}", expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color="red",
                    on_click=lambda e, uid=user_id: delete_user(uid, page)
                )
            ])
        )

    user_controls.append(
        ft.ElevatedButton("➕ Add New User", on_click=lambda e: add_user_dialog(page))
    )

    def go_back(e):
        import main_menu
        main_menu.main(page)

    def export_files(e):
        csv_path, pdf_path = export_data(skill_data)
        page.dialog = ft.AlertDialog(
            title=ft.Text("📤 Exported Files"),
            content=ft.Text(f"Saved as:\nCSV: {csv_path}\nPDF: {pdf_path}"),
            open=True,
        )
        page.update()

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column([
                summary,
                ft.Divider(thickness=2),
                *user_controls,
                ft.Divider(thickness=2),
                ft.Row([
                    ft.ElevatedButton("⬅ Back to Main Menu", on_click=go_back),
                    ft.ElevatedButton("📤 Export as CSV/PDF", on_click=export_files)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=20),
            padding=30,
            alignment=ft.alignment.center,
            expand=True,
        )
    )
