import sqlite3

# Connect to the database
conn = sqlite3.connect('driving_simulator.db')

# Create a cursor object
c = conn.cursor()

# Define the SQL statement to create the users table
create_users_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    badge_number INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    total_time REAL DEFAULT 0
);
"""

# Define the SQL statement to create the sessions table
create_sessions_table_sql = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    badge_number INTEGER NOT NULL,
    session_date TEXT NOT NULL,
    session_time REAL NOT NULL,
    FOREIGN KEY (badge_number) REFERENCES users(badge_number)
);
"""

# Execute the SQL statements to create the tables
c.execute(create_users_table_sql)
c.execute(create_sessions_table_sql)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Database and tables created successfully.")
