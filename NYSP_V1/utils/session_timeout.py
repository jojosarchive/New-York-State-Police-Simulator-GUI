import tkinter as tk
from tkinter import messagebox
import sqlite3
import time

class SessionTimeoutHandler:
    def __init__(self, root, timeout_seconds=600):
        self.root = root
        self.timeout_seconds = timeout_seconds
        self.session_start_time = None
        self.monitor_session_timeout()

    def monitor_session_timeout(self):
        self.session_start_time = time.time()
        self.check_session_timeout()

    def check_session_timeout(self):
        current_time = time.time()
        elapsed_time = current_time - self.session_start_time
        if elapsed_time >= self.timeout_seconds:
            self.handle_session_timeout()
        else:
            self.root.after(1000, self.check_session_timeout)

    def handle_session_timeout(self):
        messagebox.showwarning("Session Timeout", "Your session has timed out. Please log in again.")
        self.session_start_time = None
        # You may want to perform additional actions here, such as logging out the user or resetting the session.

if __name__ == "__main__":
    root = tk.Tk()
    session_handler = SessionTimeoutHandler(root)
    root.mainloop()
