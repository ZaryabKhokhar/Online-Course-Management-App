import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import HEADING_FONT, MAIN_FONT

class GradingSystemView(tk.Toplevel):
    def __init__(self, master, current_user, on_close_callback=None): # Add services as needed
        super().__init__(master)
        self.current_user = current_user
        self.on_close_callback = on_close_callback

        self.title("Grading System")
        self.geometry("700x500")
        self.configure(bg="#ecf0f1")

        if self.on_close_callback:
            self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        self.create_widgets()
        self.load_data_for_grading_or_viewing()

    def on_close_window(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="My Grades" if self.current_user.role == "Student" else "Grade Submissions", 
                  font=HEADING_FONT).pack(pady=10)

        self.grades_tree = ttk.Treeview(main_frame, columns=("Course", "Assignment", "Grade", "Comments"), show="headings")
        self.grades_tree.heading("Course", text="Course")
        self.grades_tree.heading("Assignment", text="Assignment")
        self.grades_tree.heading("Grade", text="Grade")
        self.grades_tree.heading("Comments", text="Comments")
        
        self.grades_tree.column("Course", width=200)
        self.grades_tree.column("Assignment", width=200)
        self.grades_tree.column("Grade", width=100, anchor=tk.CENTER)
        self.grades_tree.column("Comments", width=150)
        self.grades_tree.pack(expand=True, fill="both", pady=10)

        if self.current_user.role == "Teacher":
            grading_frame = ttk.Frame(main_frame)
            grading_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(grading_frame, text="Selected Submission ID:", font=MAIN_FONT).pack(side=tk.LEFT, padx=5)
            self.submission_id_entry = ttk.Entry(grading_frame, font=MAIN_FONT, width=10)
            self.submission_id_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(grading_frame, text="Grade:", font=MAIN_FONT).pack(side=tk.LEFT, padx=5)
            self.grade_value_entry = ttk.Entry(grading_frame, font=MAIN_FONT, width=10)
            self.grade_value_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(grading_frame, text="Comments:", font=MAIN_FONT).pack(side=tk.LEFT, padx=5)
            self.comments_entry = ttk.Entry(grading_frame, font=MAIN_FONT, width=20)
            self.comments_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
            
            submit_grade_button = ttk.Button(grading_frame, text="Submit Grade", command=self.submit_grade, style="Accent.TButton")
            submit_grade_button.pack(side=tk.LEFT, padx=5)
            
            # Add listener to tree selection to populate fields
            self.grades_tree.bind("<<TreeviewSelect>>", self.on_submission_select)


    def load_data_for_grading_or_viewing(self):
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)

        if self.current_user.role == "Student":
            # Fetch grades for self.current_user.user_id
            # Columns: Course, Assignment, Grade, Comments
            sample_data = [
                ("Intro to Python", "Lab 1", "A", "Excellent work!"),
                ("Intro to Python", "Lab 2", "B+", "Good effort, minor issues."),
                ("Web Dev Basics", "Project 1", "Pending", ""),
            ]
        elif self.current_user.role == "Teacher":
            # Fetch submissions needing grading for this teacher
            # Columns: Course, Assignment (Submission ID), Student Name, Status (e.g., Needs Grading)
            # For simplicity, using same columns as student but 'Grade' column would be for teacher input
            self.grades_tree.heading("Grade", text="Status/Enter Grade") # Modify for teacher
            self.grades_tree.heading("Comments", text="Enter Comments")
            sample_data = [
                ("Intro to Python", "Lab 1 (SubID: 101, Student: John)", "Needs Grading", ""),
                ("Web Dev Basics", "Project 1 (SubID: 102, Student: Jane)", "Needs Grading", ""),
            ]
            # You might want different columns for teachers, e.g. "Student Name", "Submission Date"
        else: # Admin
            sample_data = [("Admin View", "All Grades Overview", "N/A", "Not Implemented")]
            
        for data_row in sample_data:
            self.grades_tree.insert("", tk.END, values=data_row)

        print(f"Loading grading data for {self.current_user.username} ({self.current_user.role})")

    def on_submission_select(self, event):
        if self.current_user.role == "Teacher":
            selected_item = self.grades_tree.focus()
            if selected_item:
                item_values = self.grades_tree.item(selected_item, "values")
                # Assuming submission ID is part of the assignment string, e.g., "Lab 1 (SubID: 101, ...)"
                # This parsing is fragile and for demonstration only.
                try:
                    assignment_text = item_values[1] # Assignment column
                    sub_id_part = assignment_text.split("SubID: ")[1].split(",")[0]
                    self.submission_id_entry.delete(0, tk.END)
                    self.submission_id_entry.insert(0, sub_id_part)
                except IndexError:
                    self.submission_id_entry.delete(0, tk.END)
                    self.submission_id_entry.insert(0, "N/A")
                
                self.grade_value_entry.delete(0, tk.END)
                self.comments_entry.delete(0, tk.END)


    def submit_grade(self):
        if self.current_user.role == "Teacher":
            submission_id = self.submission_id_entry.get()
            grade_value = self.grade_value_entry.get()
            comments = self.comments_entry.get()

            if not submission_id or submission_id == "N/A" or not grade_value:
                messagebox.showerror("Error", "Submission ID and Grade value are required.")
                return

            # In a real app, call a service to save the grade
            messagebox.showinfo("Grade Submitted", f"Grade '{grade_value}' for Submission ID '{submission_id}' with comments '{comments}' submitted.")
            print(f"Teacher {self.current_user.username} submitted grade: {submission_id}, {grade_value}, {comments}")
            # Potentially reload or update the tree view
            self.load_data_for_grading_or_viewing() # Refresh list
        else:
            messagebox.showerror("Error", "Only teachers can submit grades.")