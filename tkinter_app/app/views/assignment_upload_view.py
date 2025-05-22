import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.utils.style import HEADING_FONT, MAIN_FONT

class AssignmentUploadView(tk.Toplevel):
    def __init__(self, master, current_user, on_close_callback=None): # Add services as needed
        super().__init__(master)
        self.current_user = current_user
        self.on_close_callback = on_close_callback

        self.title("Assignments")
        self.geometry("600x400")
        self.configure(bg="#ecf0f1")

        if self.on_close_callback:
            self.protocol("WM_DELETE_WINDOW", self.on_close_window)
        
        self.create_widgets()

    def on_close_window(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Assignments", font=HEADING_FONT).pack(pady=10)

        if self.current_user.role == "Student":
            ttk.Label(main_frame, text="Select Assignment:", font=MAIN_FONT).pack(pady=(5,0))
            # In a real app, populate this with assignments for the student's courses
            self.assignment_combobox = ttk.Combobox(main_frame, font=MAIN_FONT, state="readonly", width=40)
            self.assignment_combobox['values'] = ["Assignment 1 - Python Basics", "Assignment 2 - Web Concepts"]
            self.assignment_combobox.pack(pady=5)
            if self.assignment_combobox['values']:
                self.assignment_combobox.current(0)

            ttk.Button(main_frame, text="Select File to Upload", command=self.select_file, style="Accent.TButton").pack(pady=10)
            self.file_label = ttk.Label(main_frame, text="No file selected", font=MAIN_FONT)
            self.file_label.pack(pady=5)
            ttk.Button(main_frame, text="Upload Assignment", command=self.upload_assignment, style="Accent.TButton").pack(pady=10)

        elif self.current_user.role == "Teacher":
            ttk.Label(main_frame, text="Create or View Assignments (Teacher View)", font=MAIN_FONT).pack(pady=10)
            # Teacher specific UI for creating assignments or viewing submissions
            ttk.Button(main_frame, text="Create New Assignment", command=self.create_assignment, style="Accent.TButton").pack(pady=10)
            ttk.Button(main_frame, text="View Submissions", command=self.view_submissions, style="Accent.TButton").pack(pady=10)

        else: # Admin or other roles
            ttk.Label(main_frame, text="Assignment Overview (Admin View)", font=MAIN_FONT).pack(pady=10)

    def select_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.file_label.config(text=filepath)
        else:
            self.file_label.config(text="No file selected")

    def upload_assignment(self):
        filepath = self.file_label.cget("text")
        assignment_name = self.assignment_combobox.get()
        if filepath != "No file selected" and assignment_name:
            messagebox.showinfo("Upload", f"Simulating upload of '{filepath}' for '{assignment_name}'.")
            print(f"Student {self.current_user.username} uploading {filepath} for {assignment_name}")
            # Add actual service call here
        else:
            messagebox.showerror("Error", "Please select an assignment and a file.")
    
    def create_assignment(self):
        messagebox.showinfo("Teacher Action", "Opening 'Create New Assignment' form (not implemented).")
        print(f"Teacher {self.current_user.username} attempting to create an assignment.")
        # Implement assignment creation UI and service call

    def view_submissions(self):
        messagebox.showinfo("Teacher Action", "Opening 'View Submissions' interface (not implemented).")
        print(f"Teacher {self.current_user.username} attempting to view submissions.")
        # Implement UI to view submissions for teacher's courses