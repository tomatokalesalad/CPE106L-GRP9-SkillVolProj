import sqlite3
import csv

def export_all_data():
    conn = sqlite3.connect("skillvolunteer.db")
    cur = conn.cursor()

    with open("volunteers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        cur.execute("SELECT * FROM users")
        writer.writerow([desc[0] for desc in cur.description])
        writer.writerows(cur.fetchall())

    with open("requests.csv", "w", newline="") as f:
        writer = csv.writer(f)
        cur.execute("SELECT * FROM requests")
        writer.writerow([desc[0] for desc in cur.description])
        writer.writerows(cur.fetchall())

    with open("match_logs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        cur.execute("SELECT * FROM match_logs")
        writer.writerow([desc[0] for desc in cur.description])
        writer.writerows(cur.fetchall())

    conn.close()
    print("Data exported successfully to CSV.")
