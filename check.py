import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from plyer import notification
import json
import os
import csv
import datetime
from PIL import Image, ImageTk
import threading

# Constants
DATA_DIR = "user_data"
THEME_COLOR = "#3498db"
BUTTON_COLOR = "#2980b9"
ACCENT_COLOR = "#e74c3c"
BG_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"

os.makedirs(DATA_DIR, exist_ok=True)

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Life Tools - Login")
        self.root.geometry("400x500")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window(400, 500)
        
        # Create a frame for the login form
        self.frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
        self.frame.pack(expand=True)
        
        # App title
        title_label = tk.Label(
            self.frame, 
            text="Campus Life Tools", 
            font=("Helvetica", 24, "bold"),
            bg=BG_COLOR,
            fg=THEME_COLOR
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Username field
        tk.Label(
            self.frame, 
            text="Username:", 
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        self.username_entry = tk.Entry(
            self.frame, 
            font=("Helvetica", 12),
            width=25,
            bd=2,
            relief=tk.GROOVE
        )
        self.username_entry.grid(row=2, column=0, columnspan=2, pady=(0, 20), ipady=8)
        
        # Password field
        tk.Label(
            self.frame, 
            text="Password:", 
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).grid(row=3, column=0, sticky="w", pady=(0, 10))
        
        self.password_entry = tk.Entry(
            self.frame, 
            show="•", 
            font=("Helvetica", 12),
            width=25,
            bd=2,
            relief=tk.GROOVE
        )
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=(0, 30), ipady=8)
        
        # Buttons
        login_button = tk.Button(
            self.frame, 
            text="Login", 
            command=self.login,
            bg=THEME_COLOR,
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=10,
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2"
        )
        login_button.grid(row=5, column=0, padx=(0, 10), pady=(0, 10))
        
        register_button = tk.Button(
            self.frame, 
            text="Register", 
            command=self.register,
            bg=BUTTON_COLOR,
            fg="white",
            font=("Helvetica", 12),
            width=10,
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2"
        )
        register_button.grid(row=5, column=1, padx=(10, 0), pady=(0, 10))
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Status message
        self.status_label = tk.Label(
            self.frame, 
            text="", 
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg=ACCENT_COLOR
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.status_label.config(text="Please enter both username and password")
            return
        
        filepath = os.path.join(DATA_DIR, f"{username}.json")
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    user_data = json.load(f)
                    if user_data.get("password") == password:
                        self.status_label.config(text="Login successful! Redirecting...")
                        self.root.after(1000, self.launch_main_app)
                    else:
                        self.status_label.config(text="Incorrect password")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
        else:
            self.status_label.config(text="User not found")
    
    def launch_main_app(self):
        username = self.username_entry.get().strip()
        self.root.destroy()
        root = tk.Tk()
        CampusLifeApp(root, username)
    
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.status_label.config(text="Please enter both username and password")
            return
        
        filepath = os.path.join(DATA_DIR, f"{username}.json")
        
        if os.path.exists(filepath):
            self.status_label.config(text="User already exists")
        else:
            data = {"password": password, "attendance": {}, "study": [], "exams": [], "timetable": []}
            try:
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=4)
                self.status_label.config(text="Registration successful! You can now log in.")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")

class CampusLifeApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Campus Life Tools - {username}")
        self.root.geometry("800x600")
        self.root.configure(bg=BG_COLOR)
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"800x600+{x}+{y}")
        
        self.filepath = os.path.join(DATA_DIR, f"{username}.json")
        self.load_data()
        
        # Create a header frame
        header_frame = tk.Frame(root, bg=THEME_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        
        # Welcome message
        welcome_label = tk.Label(
            header_frame, 
            text=f"Welcome, {username}!", 
            font=("Helvetica", 16, "bold"),
            bg=THEME_COLOR,
            fg="white",
            pady=10
        )
        welcome_label.pack(side=tk.LEFT, padx=20)
        
        # Logout button
        logout_btn = tk.Button(
            header_frame, 
            text="Logout", 
            command=self.logout,
            bg=ACCENT_COLOR,
            fg="white",
            font=("Helvetica", 10),
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        logout_btn.pack(side=tk.RIGHT, padx=20)
        
        # Create a style for the notebook
        style = ttk.Style()
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background="#dfe6e9", padding=[15, 5], font=('Helvetica', 11))
        style.map("TNotebook.Tab", background=[("selected", THEME_COLOR)], foreground=[("selected", "white")])
        style.configure("TFrame", background=BG_COLOR)
        
        # Create the notebook (tab control)
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=20)
        
        # Create tabs
        self.attendance_tab = ttk.Frame(self.tab_control)
        self.study_tab = ttk.Frame(self.tab_control)
        self.exam_tab = ttk.Frame(self.tab_control)
        self.timetable_tab = ttk.Frame(self.tab_control)
        
        # Add tabs to notebook
        self.tab_control.add(self.attendance_tab, text="Attendance")
        self.tab_control.add(self.study_tab, text="Study Planner")
        self.tab_control.add(self.exam_tab, text="Exam Reminder")
        self.tab_control.add(self.timetable_tab, text="Timetable")
        
        # Setup each tab
        self.setup_attendance_tab()
        self.setup_study_tab()
        self.setup_exam_tab()
        self.setup_timetable_tab()
        
        # Create a status bar
        self.status_bar = tk.Label(
            root, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#dfe6e9",
            fg=TEXT_COLOR,
            font=("Helvetica", 10)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Start notification thread
        threading.Thread(target=self.send_notifications, daemon=True).start()

    def load_data(self):
        try:
            with open(self.filepath, 'r') as f:
                self.data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user data: {str(e)}")
            self.data = {"password": "", "attendance": {}, "study": [], "exams": [], "timetable": []}

    def save_data(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
            self.status_bar.config(text="Data saved successfully")
        except Exception as e:
            self.status_bar.config(text=f"Error saving data: {str(e)}")

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginWindow(root)

    # -------- Attendance Tab --------
    def setup_attendance_tab(self):
        # Title
        title_label = tk.Label(
            self.attendance_tab, 
            text="Attendance Tracker", 
            font=("Helvetica", 16, "bold"),
            bg=BG_COLOR,
            fg=THEME_COLOR
        )
        title_label.pack(pady=(10, 20))
        
        # Input frame
        input_frame = tk.Frame(self.attendance_tab, bg=BG_COLOR)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Subject input
        tk.Label(
            input_frame, 
            text="Subject:", 
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).grid(row=0, column=0, padx=(0, 10), pady=10)
        
        self.attendance_entry = tk.Entry(
            input_frame, 
            font=("Helvetica", 12),
            width=30,
            bd=2,
            relief=tk.GROOVE
        )
        self.attendance_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Buttons
        mark_btn = tk.Button(
            input_frame, 
            text="Mark Present", 
            command=self.mark_attendance,
            bg=THEME_COLOR,
            fg="white",
            font=("Helvetica", 11),
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        mark_btn.grid(row=0, column=2, padx=10, pady=10)
        
        export_btn = tk.Button(
            input_frame, 
            text="Export CSV", 
            command=self.export_attendance,
            bg=BUTTON_COLOR,
            fg="white",
            font=("Helvetica", 11),
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        export_btn.grid(row=0, column=3, padx=10, pady=10)
        
        # List frame
        list_frame = tk.Frame(self.attendance_tab, bg=BG_COLOR)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # List with headers
        columns = ("Subject", "Total Classes")
        self.attendance_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show="headings",
            height=10,
            selectmode="browse",
            yscrollcommand=scrollbar.set
        )
        
        # Configure columns
        self.attendance_tree.heading("Subject", text="Subject")
        self.attendance_tree.heading("Total Classes", text="Total Classes")
        
        self.attendance_tree.column("Subject", width=300, anchor=tk.W)
        self.attendance_tree.column("Total Classes", width=150, anchor=tk.CENTER)
        
        # Configure scrollbar
        scrollbar.config(command=self.attendance_tree.yview)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()