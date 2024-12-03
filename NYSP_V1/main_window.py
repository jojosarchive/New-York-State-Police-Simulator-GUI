import tkinter as tk
from tkinter import messagebox
import sqlite3
import psutil
import time
from user_management import UserManagementApp
from session_timeout import timeout_warning

def login(root, badge_entry, name_entry):
    # Retrieve badge number and name from the entry fields
    badge_number = badge_entry.get()
    name = name_entry.get()

    # Connect to the SQLite database
    conn = sqlite3.connect('driving_simulator.db')
    c = conn.cursor()
    # Check if the provided badge number and name exist in the database
    c.execute("SELECT * FROM users WHERE badge_number=? AND name=?", (badge_number, name))
    user = c.fetchone()
    conn.close()

    # If user exists, show login success message and proceed to the main menu
    if user:
        messagebox.showinfo("Login Success", f"Welcome {name}!")
        root.after_cancel(timeout_warning)  # Cancel any existing timeout warning
        main_menu(root, name, badge_number)
    else:
        messagebox.showerror("Login Failed", "Invalid badge number or name.")

def start_app():
    root = tk.Tk()
    root.title("Driving Simulator Tracker")

    # Set initial window size and position
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 3
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Update label and entry widget fonts and button style
    label_font = ("Helvetica", 12)
    entry_font = ("Helvetica", 12)
    button_font = ("Helvetica", 12)

    badge_label = tk.Label(root, text="Badge Number:", font=label_font)
    badge_label.place(relx=0.5, rely=0.3, anchor="center")
    badge_entry = tk.Entry(root, font=entry_font, bd=2, relief="solid")
    badge_entry.place(relx=0.5, rely=0.4, anchor="center")

    name_label = tk.Label(root, text="Name:", font=label_font)
    name_label.place(relx=0.5, rely=0.5, anchor="center")
    name_entry = tk.Entry(root, font=entry_font, bd=2, relief="solid")
    name_entry.place(relx=0.5, rely=0.6, anchor="center")

    login_button = tk.Button(root, text="Login", font=button_font, command=lambda: login(root, badge_entry, name_entry), padx=10, pady=5)
    login_button.place(relx=0.5, rely=0.7, anchor="center")

    # Create a label to display the signature
    signature_label = tk.Label(root, text="K", font=("Arial", 10), fg="gray")
    signature_label.place(relx=1, rely=1, anchor="se")  # Place the label in the bottom right corner

    root.mainloop()

def main_menu(root, name, badge_number):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Set window title and size
    root.title("Main Menu")
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 3
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(root, text=f"Welcome {name}!", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

    back_button = tk.Button(root, text="Back", font=("Helvetica", 12), command=lambda: start_app(), padx=10, pady=5,
                            bg="#6c757d", fg="white")
    back_button.place(x=10, y=10)

    start_session_button = tk.Button(root, text="Start New Session", font=("Helvetica", 12),
                                     command=lambda: start_new_session(root, name, badge_number), padx=10, pady=5,
                                     bg="#007bff", fg="white")
    start_session_button.place(relx=0.5, rely=0.3, anchor="center")

    view_progress_button = tk.Button(root, text="View Progress", font=("Helvetica", 12),
                                     command=lambda: view_progress(root, badge_number), padx=10, pady=5,
                                     bg="#28a745", fg="white")
    view_progress_button.place(relx=0.5, rely=0.4, anchor="center")

    leaderboard_button = tk.Button(root, text="Leaderboard", font=("Helvetica", 12),
                                   command=lambda: view_leaderboard(root), padx=10, pady=5, bg="#17a2b8",
                                   fg="white")
    leaderboard_button.place(relx=0.5, rely=0.5, anchor="center")

    manage_users_button = tk.Button(root, text="Manage Users", font=("Helvetica", 12),
                                    command=lambda: UserManagementApp(tk.Toplevel(root)), padx=10, pady=5,
                                    bg="#ffc107", fg="black")
    manage_users_button.place(relx=0.5, rely=0.6, anchor="center")

    exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), command=root.quit, padx=10, pady=5,
                            bg="#dc3545", fg="white")
    exit_button.place(relx=0.5, rely=0.7, anchor="center")

    timeout_warning(root)

def start_new_session(root, name, badge_number):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("New Session")

    tk.Label(root, text=f"Session for {name}").pack(pady=20)

    game_found = False
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'acs':
            game_found = True
            break

    if not game_found:
        messagebox.showerror("Game Not Found", "The game was not found. Please start the game and try again.")
        main_menu(root, name, badge_number)
        return

    tk.Label(root, text="Waiting for game to start...").pack(pady=20)

    root.update()

    def check_game():
        game_running = False
        while not game_running:
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == 'acs':
                    game_running = True
                    break
            time.sleep(5)

        start_time = time.time()
        tk.Label(root, text="Game started. Tracking time...").pack(pady=20)
        root.update()

        time.sleep(30)
        end_session(root, badge_number, start_time)

    root.after(1000, check_game)

def end_session(root, badge_number, start_time):
    end_time = time.time()
    session_time = end_time - start_time

    conn = sqlite3.connect('driving_simulator.db')
    c = conn.cursor()
    c.execute("INSERT INTO sessions (badge_number, session_date, session_time) VALUES (?, datetime('now'), ?)",
              (badge_number, session_time))
    c.execute("UPDATE users SET total_time = total_time + ? WHERE badge_number = ?",
              (session_time, badge_number))
    conn.commit()
    conn.close()

    messagebox.showinfo("Session Ended", f"Session duration: {session_time / 60:.2f} minutes")
    main_menu(root, "", badge_number)

def view_progress(root, badge_number):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Progress")

    conn = sqlite3.connect('driving_simulator.db')
    c = conn.cursor()
    c.execute("SELECT total_time FROM users WHERE badge_number=?", (badge_number,))
    total_time_row = c.fetchone()
    if total_time_row:
        total_time = total_time_row[0]
        c.execute("SELECT session_date, session_time FROM sessions WHERE badge_number=?", (badge_number,))
        sessions = c.fetchall()
        conn.close()

        tk.Label(root, text=f"Total driving time: {total_time / 60:.2f} minutes").pack(pady=20)
        for session in sessions:
            tk.Label(root, text=f"Date: {session[0]}, Duration: {session[1] / 60:.2f} minutes").pack(pady=5)
    else:
        tk.Label(root, text="No progress available.").pack(pady=20)

    back_button = tk.Button(root, text="Back", command=lambda: main_menu(root, "", badge_number))
    back_button.pack(pady=20)

def view_leaderboard(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Leaderboard")

    conn = sqlite3.connect('driving_simulator.db')
    c = conn.cursor()
    c.execute("SELECT name, total_time FROM users ORDER BY total_time DESC")
    leaderboard = c.fetchall()
    conn.close()

    tk.Label(root, text="Leaderboard").pack(pady=20)
    for idx, user in enumerate(leaderboard):
        tk.Label(root, text=f"{idx + 1}. {user[0]} - {user[1] / 60:.2f} minutes").pack(pady=5)

    back_button = tk.Button(root, text="Back", command=lambda: main_menu(root, "", ""))
    back_button.pack(pady=20)

if __name__ == "__main__":
    start_app()
