import sqlite3

def setup_database():
    conn = sqlite3.connect('../driving_simulator.db')
    c = conn.cursor()

    # Create users table with an auto-incrementing ID maybe not so much w the ID
    # using their badge ID will really make a difference and create a more well
    # structured code
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            badge_number TEXT,
            name TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database schema updated successfully.")

