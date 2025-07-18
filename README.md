Skill-Based Volunteer Exchange System
--------------------------------------

DESCRIPTION:
This project is a desktop application that matches volunteers with people requesting help based on skill, location, and availability. It includes user registration, request submission, automatic matching, and an admin dashboard with data export and visualizations.

🛠 BUILT WITH:
- Python 3.13+
- Flet (UI framework)
- SQLite (local database)
- Matplotlib (for pie charts)
- Pandas (for CSV/PDF exports)
- Google Maps API (optional future feature)

FILE STRUCTURE:
- main_menu.py ............ Entry point with role selection (Volunteer, Requester, Admin)
- register_form.py ........ Volunteer registration UI
- request_form.py ......... Help requester form UI
- match_results.py ........ UI for displaying match history
- admin_login.py .......... Admin login interface
- admin_dashboard.py ...... Admin panel with charts, user management, and export
- location_utils.py ....... Location-based sorting (future Maps integration)
- skillvolunteer.db ....... SQLite database file
- skills_export.csv/pdf ... Generated exports (on demand)
- README.txt .............. This guide

HOW TO RUN:
1. Open terminal / command prompt.
2. Navigate to the project folder:
   cd SkillVolunteer

3. Run the app:
   python main_menu.py

DEPENDENCIES:
Make sure you have installed the following Python packages:
- flet
- pandas
- matplotlib
- sqlite3 (built-in)

To install dependencies, run:
pip install flet pandas matplotlib

ADMIN LOGIN (default credentials):
Username: admin
Password: admin123

NOTES:
- The UI uses a dark theme.
- Volunteers and requesters are automatically matched after registering.
- The admin can view all users, match stats, and export data in CSV or PDF format.
- Future upgrades: map visualization, real-time matching, and user management via UI.

FOR PROFESSORS:
This project is designed to be runnable in Windows (Oracle VM or bare metal). If running on Linux/Ubuntu:
- Ensure Python 3.10+ is installed.
- Run `pip3 install flet pandas matplotlib`
- Launch using `python3 main_menu.py` or if in windows `python app.py`

---

Thank you!
- Alec ✨
