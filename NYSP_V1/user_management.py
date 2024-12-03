import tkinter as tk
from tkinter import messagebox
import sqlite3

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management")

        # This frame should help to create a new user
        add_user_frame = tk.LabelFrame(root, text="Add New User")
        add_user_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(add_user_frame, text="Badge Number:").grid(row=0, column=0, padx=5, pady=5)
        self.badge_entry = tk.Entry(add_user_frame)
        self.badge_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_user_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(add_user_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = tk.Button(add_user_frame, text="Add User", command=self.add_user)
        add_button.grid(row=2, columnspan=2, padx=5, pady=5)

        # with this functions i should be able to create a edit and delete button
        edit_user_frame = tk.LabelFrame(root, text="Edit/Delete User")
        edit_user_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(edit_user_frame, text="Badge Number (for editing/deleting):").grid(row=0, column=0, padx=5, pady=5)
        self.edit_badge_entry = tk.Entry(edit_user_frame)
        self.edit_badge_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(edit_user_frame, text="New Name:").grid(row=1, column=0, padx=5, pady=5)
        self.edit_name_entry = tk.Entry(edit_user_frame)
        self.edit_name_entry.grid(row=1, column=1, padx=5, pady=5)

        edit_button = tk.Button(edit_user_frame, text="Edit User", command=self.edit_user)
        edit_button.grid(row=2, column=0, padx=5, pady=5)

        delete_button = tk.Button(edit_user_frame, text="Delete User", command=self.delete_user)
        delete_button.grid(row=2, column=1, padx=5, pady=5)

        # not only will this create a list but i can also organize different
        user_list_frame = tk.LabelFrame(root, text="User List")
        user_list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.user_listbox = tk.Listbox(user_list_frame)
        self.user_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        self.user_listbox.bind("<Double-1>", self.populate_edit_fields)

        self.populate_user_list()

    def add_user(self):
        # This will retrieve user input
        badge_number = self.badge_entry.get()
        name = self.name_entry.get()

        # Can this be enough t validate input
        if not badge_number or not name:
            messagebox.showerror("Error", "Please enter both badge number and name.")
            return

        # Add user to the database
        try:
            conn = sqlite3.connect('driving_simulator.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (badge_number, name) VALUES (?, ?)", (badge_number, name))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User added successfully.")
            self.populate_user_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")

    def edit_user(self):
        # Retrieve user input
        badge_number = self.edit_badge_entry.get()
        new_name = self.edit_name_entry.get()

        # Validate input
        if not badge_number or not new_name:
            messagebox.showerror("Error", "Please enter both badge number and new name.")
            return

        # Update user in the database
        try:
            conn = sqlite3.connect('driving_simulator.db')
            c = conn.cursor()
            c.execute("UPDATE users SET name=? WHERE badge_number=?", (new_name, badge_number))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User updated successfully.")
            self.populate_user_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {e}")

    def delete_user(self):
        # Retrieve user badge number
        badge_number = self.edit_badge_entry.get()

        # Validate input
        if not badge_number:
            messagebox.showerror("Error", "Please enter badge number.")
            return

        # Delete user from the database
        try:
            conn = sqlite3.connect('driving_simulator.db')
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE badge_number=?", (badge_number,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User deleted successfully.")
            self.populate_user_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")

    def populate_user_list(self):
        try:
            self.user_listbox.delete(0, tk.END)  # Clear the listbox
            conn = sqlite3.connect('driving_simulator.db')
            c = conn.cursor()
            c.execute("SELECT badge_number, name FROM users")
            users = c.fetchall()
            conn.close()

            for user in users:
                self.user_listbox.insert(tk.END, f"{user[0]} - {user[1]}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve user list: {e}")

    def populate_edit_fields(self, event):
        selected_user = self.user_listbox.get(self.user_listbox.curselection())
        badge_number = selected_user.split(' - ')[0]
        self.edit_badge_entry.delete(0, tk.END)
        self.edit_badge_entry.insert(0, badge_number)
