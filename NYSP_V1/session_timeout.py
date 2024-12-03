import tkinter as tk
from tkinter import messagebox
import time  # Add this import statement

def timeout_warning(root):
    TIMEOUT_SECONDS = 600  # Adjust timeout duration as needed (600 seconds = 10 minutes)

    def reset_timer():
        nonlocal last_activity_time
        last_activity_time = time.time()

    def check_activity():
        nonlocal last_activity_time
        current_time = time.time()
        if current_time - last_activity_time > TIMEOUT_SECONDS:
            messagebox.showwarning("Session Timeout", "Your session has timed out due to inactivity.")
            root.quit()
        else:
            root.after(1000, check_activity)

    last_activity_time = time.time()

    root.bind("<Any-KeyPress>", lambda event: reset_timer())
    root.bind("<Any-ButtonPress>", lambda event: reset_timer())

    check_activity()

if __name__ == "__main__":
    root = tk.Tk()
    timeout_warning(root)
    root.mainloop()
