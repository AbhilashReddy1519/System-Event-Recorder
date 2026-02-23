import tkinter as tk
from tkinter import ttk
import sqlite3
from modules.capture import DB_PATH, create_file, create_folder, delete_file, delete_folder

class SecurityUI:
    def _init_(self, root):
        self.root = root
        self.root.title("Security Event Recorder")
        self.root.geometry("800x600")

        # Frame for buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(fill=tk.X, pady=5)

        # Buttons for creating/deleting files and folders
        ttk.Button(button_frame, text="Create File", command=self.create_test_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create Folder", command=self.create_test_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete File", command=self.delete_test_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Folder", command=self.delete_test_folder).pack(side=tk.LEFT, padx=5)

        # Treeview for logs
        self.tree = ttk.Treeview(root, columns=("ID", "Timestamp", "Event Type", "Details"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Event Type", text="Event Type")
        self.tree.heading("Details", text="Details")
        self.tree.column("ID", width=50)
        self.tree.column("Timestamp", width=150)
        self.tree.column("Event Type", width=150)
        self.tree.column("Details", width=450)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Start periodic update
        self.update_logs()

    def create_test_file(self):
        create_file("testfile.txt")

    def create_test_folder(self):
        create_folder("testfolder")

    def delete_test_file(self):
        delete_file("testfile.txt")

    def delete_test_folder(self):
        delete_folder("testfolder")

    def update_logs(self):
        """Fetch and display logs from the database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, event_type, details FROM logs ORDER BY id DESC LIMIT 100")
        rows = cursor.fetchall()
        conn.close()

        # Clear current entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new entries
        for row in rows:
            self.tree.insert("", tk.END, values=row)

        # Schedule next update
        self.root.after(1000, self.update_logs)