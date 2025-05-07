import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from plyer import notification
import json
import os
import csv
import datetime

DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Life Tools - Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#e0f7fa")

        self.frame = tk.Frame(root, bg="#ffffff", bd=3, relief="ridge")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=230)

        tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#ffffff").place(x=20, y=20)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12), width=22)
        self.username_entry.place(x=100, y=20)

        tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#ffffff").place(x=20, y=60)
        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 12), width=22)
        self.password_entry.place(x=100, y=60)

        # Adding spacing between buttons
        tk.Button(self.frame, text="Login", command=self.login, font=("Arial", 12), bg="#00796b", fg="white").place(x=40, y=110, width=90)
        tk.Button(self.frame, text="Register", command=self.register, font=("Arial", 12), bg="#0288d1", fg="white").place(x=160, y=110, width=90)

        # Adding spacing between buttons
        tk.Label(self.frame, text=" ", bg="#ffffff").place(x=20, y=150)  # Empty label for spacing

        # Forgot Password Button
        tk.Button(self.frame, text="Forgot Password?", command=self.forgot_password, font=("Arial", 10), bg="#f44336", fg="white").place(x=100, y=170)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        filepath = os.path.join(DATA_DIR, f"{username}.json")

        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                user_data = json.load(f)
                if user_data.get("password") == password:
                    self.root.destroy()
                    root = tk.Tk()
                    CampusLifeApp(root, username)
                else:
                    messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "User not found")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        filepath = os.path.join(DATA_DIR, f"{username}.json")

        if os.path.exists(filepath):
            messagebox.showerror("Error", "User already exists")
        else:
            data = {"password": password, "attendance": {}, "study": [], "exams": [], "timetable": []}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Success", "User registered! You can now log in.")
        
        # Clear the entries and allow the user to register again
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        # Optional: Bring focus to the username entry field to allow easy registration
        self.username_entry.focus()


    def forgot_password(self):
        forgot_window = tk.Toplevel(self.root)
        forgot_window.title("Forgot Password")
        forgot_window.geometry("350x200")
        forgot_window.configure(bg="#e0f7fa")

        tk.Label(forgot_window, text="Enter Username to Reset Password", font=("Arial", 12), bg="#e0f7fa").pack(pady=20)

        tk.Label(forgot_window, text="Username:", font=("Arial", 12), bg="#e0f7fa").pack()
        username_entry = tk.Entry(forgot_window, font=("Arial", 12), width=22)
        username_entry.pack(pady=10)

        tk.Button(forgot_window, text="Reset Password", command=lambda: self.reset_password(username_entry.get().strip(), forgot_window), font=("Arial", 12), bg="#0288d1", fg="white").pack(pady=10)

    def reset_password(self, username, forgot_window):
        filepath = os.path.join(DATA_DIR, f"{username}.json")
        if os.path.exists(filepath):
            new_password = tk.simpledialog.askstring("New Password", "Enter new password:", show="*")
            if new_password:
                with open(filepath, 'r+') as f:
                    user_data = json.load(f)
                    user_data["password"] = new_password
                    f.seek(0)
                    json.dump(user_data, f, indent=4)
                messagebox.showinfo("Success", "Password has been reset.")
                forgot_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a new password.")
        else:
            messagebox.showerror("Error", "User not found")

class CampusLifeApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Campus Life Tools - {username}")
        self.root.geometry("800x600")
        self.root.configure(bg="#f1f8e9")
        self.filepath = os.path.join(DATA_DIR, f"{username}.json")

        self.load_data()

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook.Tab", font=("Arial", 14), padding=[10, 5], background="#aed581", foreground="black")
        style.map("TNotebook.Tab", background=[("selected", "#558b2f")], foreground=[("selected", "white")])

        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        self.attendance_tab = ttk.Frame(self.tab_control)
        self.study_tab = ttk.Frame(self.tab_control)
        self.exam_tab = ttk.Frame(self.tab_control)
        self.timetable_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.attendance_tab, text="Attendance")
        self.tab_control.add(self.study_tab, text="Study Planner")
        self.tab_control.add(self.exam_tab, text="Exam Reminder")
        self.tab_control.add(self.timetable_tab, text="Timetable")

        self.setup_attendance_tab()
        self.setup_study_tab()
        self.setup_exam_tab()
        self.setup_timetable_tab()
        self.send_notifications()

    def load_data(self):
        with open(self.filepath, 'r') as f:
            self.data = json.load(f)

    def save_data(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

    def setup_attendance_tab(self):
        frame = ttk.Frame(self.attendance_tab)
        frame.pack(pady=20)

        tk.Label(frame, text="Subject:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.attendance_entry = tk.Entry(frame, font=("Arial", 12))
        self.attendance_entry.grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Mark Present", command=self.mark_attendance, bg="#43a047", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Export CSV", command=self.export_attendance, bg="#5e35b1", fg="white").grid(row=0, column=3, padx=5)

        self.attendance_list = tk.Listbox(self.attendance_tab, width=80, font=("Arial", 11), bd=2, relief="groove")
        self.attendance_list.pack(pady=10)

        for sub, count in self.data["attendance"].items():
            self.attendance_list.insert(tk.END, f"{sub} - Total: {count}")

    def mark_attendance(self):
        sub = self.attendance_entry.get().strip()
        if sub:
            self.data["attendance"][sub] = self.data["attendance"].get(sub, 0) + 1
            self.attendance_list.insert(tk.END, f"{sub} - Total: {self.data['attendance'][sub]}")
            self.attendance_entry.delete(0, tk.END)
            self.save_data()

    def export_attendance(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Subject", "Total"])
                for sub, count in self.data["attendance"].items():
                    writer.writerow([sub, count])
            messagebox.showinfo("Exported", f"Saved to {path}")

    def setup_study_tab(self):
        frame = ttk.Frame(self.study_tab)
        frame.pack(pady=20)

        tk.Label(frame, text="Topic:", font=("Arial", 12)).grid(row=0, column=0)
        self.study_entry = tk.Entry(frame, font=("Arial", 12))
        self.study_entry.grid(row=0, column=1)
        tk.Button(frame, text="Add", command=self.add_study, bg="#00796b", fg="white").grid(row=0, column=2, padx=5)

        self.study_list = tk.Listbox(self.study_tab, width=80, font=("Arial", 11), bd=2, relief="groove")
        self.study_list.pack(pady=10)
        self.study_list.bind('<Double-1>', self.toggle_study_done)

        for topic in self.data["study"]:
            self.study_list.insert(tk.END, topic)

    def add_study(self):
        topic = self.study_entry.get().strip()
        if topic:
            item = f"[ ] {topic}"
            self.study_list.insert(tk.END, item)
            self.data["study"].append(item)
            self.study_entry.delete(0, tk.END)
            self.save_data()

    def toggle_study_done(self, event):
        index = self.study_list.curselection()[0]
        current = self.data["study"][index]
        if current.startswith("[ ]"):
            new = current.replace("[ ]", "[X]", 1)
        else:
            new = current.replace("[X]", "[ ]", 1)
        self.data["study"][index] = new
        self.study_list.delete(index)
        self.study_list.insert(index, new)
        self.save_data()

    def setup_exam_tab(self):
        frame = ttk.Frame(self.exam_tab)
        frame.pack(pady=20)

        tk.Label(frame, text="Exam Name:", font=("Arial", 12)).grid(row=0, column=0)
        self.exam_entry = tk.Entry(frame, font=("Arial", 12))
        self.exam_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Date:", font=("Arial", 12)).grid(row=0, column=2)
        self.exam_date = DateEntry(frame, font=("Arial", 12), date_pattern='y-mm-dd')
        self.exam_date.grid(row=0, column=3, padx=5)

        tk.Button(frame, text="Add Exam", command=self.add_exam, bg="#0288d1", fg="white").grid(row=0, column=4, padx=5)

        self.exam_list = tk.Listbox(self.exam_tab, width=80, font=("Arial", 11), bd=2, relief="groove")
        self.exam_list.pack(pady=10)

        for exam in self.data["exams"]:
            self.exam_list.insert(tk.END, f"{exam['name']} - {exam['date']}")

    def add_exam(self):
        name = self.exam_entry.get().strip()
        date = self.exam_date.get()
        if name and date:
            self.data["exams"].append({"name": name, "date": date})
            self.exam_list.insert(tk.END, f"{name} - {date}")
            self.exam_entry.delete(0, tk.END)
            self.save_data()

    def setup_timetable_tab(self):
        frame = ttk.Frame(self.timetable_tab)
        frame.pack(pady=20)

        tk.Label(frame, text="Time:", font=("Arial", 12)).grid(row=0, column=0)
        self.time_entry = tk.Entry(frame, font=("Arial", 12))
        self.time_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Subject:", font=("Arial", 12)).grid(row=0, column=2)
        self.subject_entry = tk.Entry(frame, font=("Arial", 12))
        self.subject_entry.grid(row=0, column=3, padx=5)

        tk.Button(frame, text="Add Timetable", command=self.add_timetable, bg="#43a047", fg="white").grid(row=0, column=4, padx=5)

        self.timetable_list = tk.Listbox(self.timetable_tab, width=80, font=("Arial", 11), bd=2, relief="groove")
        self.timetable_list.pack(pady=10)

        for entry in self.data["timetable"]:
            self.timetable_list.insert(tk.END, f"{entry['time']} - {entry['subject']}")

    def add_timetable(self):
        time = self.time_entry.get().strip()
        subject = self.subject_entry.get().strip()
        if time and subject:
            self.data["timetable"].append({"time": time, "subject": subject})
            self.timetable_list.insert(tk.END, f"{time} - {subject}")
            self.time_entry.delete(0, tk.END)
            self.subject_entry.delete(0, tk.END)
            self.save_data()

    def send_notifications(self):
        now = datetime.datetime.now()
        for exam in self.data["exams"]:
            exam_date = datetime.datetime.strptime(exam["date"], "%Y-%m-%d")
            if now.date() == exam_date.date():
                notification.notify(
                    title="Exam Reminder",
                    message=f"Today is your {exam['name']} exam!",
                    timeout=10
                )

if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
    self.root.mainloop()
    self.root.destroy()
