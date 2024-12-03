import sqlite3
import csv

def backup_data():
    conn = sqlite3.connect('../driving_simulator.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    with open('../users_backup.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'badge_number', 'name'])
        writer.writerows(users)

if __name__ == "__main__":
    backup_data()
    print("Data backup completed.")
