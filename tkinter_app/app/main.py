import tkinter as tk
from tkinter import ttk, messagebox
from app.views.login_view import LoginView
from app.views.course_creation_view import CourseCreationView
from app.views.student_enrollment_view import StudentEnrollmentView
from app.views.assignment_upload_view import AssignmentUploadView
from app.views.progress_tracking_view import ProgressTrackingView
from app.views.grading_system_view import GradingSystemView
from app.views.message_board_view import MessageBoardView
from app.services.auth_service import AuthService
from app.services.course_service import CourseService
from app.services.user_service import UserService
from app.services.enrollment_service import EnrollmentService
# Import necessary color variables from your style module
from app.utils.style import HEADING_FONT, MAIN_FONT, PRIMARY_COLOR, LIGHT_TEXT_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR, NAVY_BLUE, WARM_CREAM, MUTED_GOLD

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Course Management System")
        self.geometry("800x600")
        # Use BACKGROUND_COLOR for the main window background
        self.configure(bg=BACKGROUND_COLOR)

        self.auth_service = AuthService()
        self.course_service = CourseService()
        self.user_service = UserService(self.auth_service) # Pass auth_service to user_service
        self.enrollment_service = EnrollmentService()
        self.current_user = None
        self.open_windows = {} # To track open Toplevel windows

        self.current_view = None
        self.show_login_view()

    def show_login_view(self):
        if self.current_view:
            self.current_view.destroy()
        # Pass the main application instance to LoginView
        self.login_view_frame = LoginView(self, self.show_main_app_for_user)
        self.login_view_frame.pack(expand=True, fill=tk.BOTH)
        self.current_view = self.login_view_frame
        if hasattr(self, 'main_frame'):
            self.main_frame.pack_forget()
            del self.main_frame
        if hasattr(self, 'sidebar_frame'):
            self.sidebar_frame.pack_forget()
            del self.sidebar_frame


    def show_main_app_for_user(self, user):
        self.current_user = user
        if self.current_view:
            self.current_view.destroy()

        # Hide login view explicitly if it still exists
        if hasattr(self, 'login_view_frame') and self.login_view_frame.winfo_exists():
             self.login_view_frame.pack_forget()

        self.create_main_layout()
        self.update_sidebar_buttons()
        self.show_welcome_dashboard()


    def create_main_layout(self):
        # Sidebar background using PRIMARY_COLOR (Navy Blue)
        self.sidebar_frame = tk.Frame(self, bg=PRIMARY_COLOR, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Main content area background using BACKGROUND_COLOR (Warm Cream)
        self.main_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.main_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Sidebar header using colors from the palette
        self.sidebar_header = tk.Label(self.sidebar_frame, text="Menu", font=HEADING_FONT, bg=PRIMARY_COLOR, fg=LIGHT_TEXT_COLOR, pady=10)
        self.sidebar_header.pack(pady=(10,20))

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_dashboard(self):
        self.clear_main_frame()
        welcome_text = f"Welcome, {self.current_user.full_name} ({self.current_user.role})!"
        # Labels in main frame using BACKGROUND_COLOR and NAVY_BLUE for text
        ttk.Label(self.main_frame, text=welcome_text, font=HEADING_FONT, background=BACKGROUND_COLOR, foreground=NAVY_BLUE).pack(pady=20, padx=20, anchor="center")
        ttk.Label(self.main_frame, text="Select an option from the menu to get started.", font=MAIN_FONT, background=BACKGROUND_COLOR, foreground=NAVY_BLUE).pack(pady=10, padx=20, anchor="center")


    def update_sidebar_buttons(self):
        for widget in self.sidebar_frame.winfo_children():
            if widget != self.sidebar_header: # Don't destroy header
                widget.destroy()

        buttons_config = []

        # Define button configurations based on user role
        if self.current_user.role == "Admin":
            buttons_config = [
                ("Course Management", self.open_course_management),
                ("User Management", lambda: self.show_placeholder_view("User Management")),
                ("View Announcements", self.open_message_board),
            ]
        elif self.current_user.role == "Teacher":
            buttons_config = [
                ("My Courses", self.open_course_management), # Teachers might view/edit their courses
                ("Assignments", self.open_assignment_view),
                ("Grading", self.open_grading_system),
                ("Student Progress", self.open_progress_tracking),
                ("Announcements", self.open_message_board),
            ]
        elif self.current_user.role == "Student":
            buttons_config = [
                ("Enroll in Courses", self.open_student_enrollment),
                ("My Assignments", self.open_assignment_view),
                ("My Progress", self.open_progress_tracking),
                ("My Grades", self.open_grading_system),
                ("Announcements", self.open_message_board),
            ]

        # Add logout button for all roles
        buttons_config.append(("Logout", self.logout))

        # Configure the style for sidebar buttons
        style = ttk.Style()
        # Changed background to BACKGROUND_COLOR (Warm Cream) and foreground to NAVY_BLUE
        style.configure("Sidebar.TButton", font=MAIN_FONT, background=BACKGROUND_COLOR, foreground=NAVY_BLUE, borderwidth=0, focusthickness=0, padding=10)
        # Active state background using SECONDARY_COLOR (Muted Gold)
        style.map("Sidebar.TButton", background=[('active', SECONDARY_COLOR)], relief=[('pressed', 'flat'), ('active', 'flat')])


        # Create and pack the buttons
        for text, command in buttons_config:
            btn = ttk.Button(self.sidebar_frame, text=text, command=command, style="Sidebar.TButton", width=20)
            btn.pack(fill=tk.X, pady=5, padx=10)

    def open_view_as_toplevel(self, view_class, view_name, *args):
        # Check if a window of this type is already open
        if view_name in self.open_windows and self.open_windows[view_name].winfo_exists():
            # If it exists and is not destroyed, bring it to the front
            self.open_windows[view_name].lift()
            self.open_windows[view_name].focus()
        else:
            # Create a new Toplevel window
            # Define a callback to remove the window from the open_windows dict when closed
            on_close = lambda: self.open_windows.pop(view_name, None)
            # Instantiate the view class as a Toplevel window, passing necessary arguments and the close callback
            new_window = view_class(self, *args, on_close_callback=on_close)
            # Store the new window in the dictionary
            self.open_windows[view_name] = new_window


    def open_course_management(self):
        # Open CourseCreationView as a Toplevel window
        self.open_view_as_toplevel(CourseCreationView, "CourseManagement", self.course_service, self.user_service)

    def open_student_enrollment(self):
        # Open StudentEnrollmentView as a Toplevel window
        self.open_view_as_toplevel(StudentEnrollmentView, "StudentEnrollment", self.enrollment_service, self.course_service, self.user_service, self.current_user)

    def open_assignment_view(self):
        # Open AssignmentUploadView as a Toplevel window
        self.open_view_as_toplevel(AssignmentUploadView, "AssignmentUpload", self.current_user)

    def open_progress_tracking(self):
        # Open ProgressTrackingView as a Toplevel window
        self.open_view_as_toplevel(ProgressTrackingView, "ProgressTracking", self.current_user)

    def open_grading_system(self):
        # Open GradingSystemView as a Toplevel window
        self.open_view_as_toplevel(GradingSystemView, "GradingSystem", self.current_user)

    def open_message_board(self):
        # Open MessageBoardView as a Toplevel window
        self.open_view_as_toplevel(MessageBoardView, "MessageBoard", self.current_user)

    def show_placeholder_view(self, view_name):
        self.clear_main_frame()
        # Placeholder label using colors from the palette
        ttk.Label(self.main_frame, text=f"{view_name} - Not Implemented Yet", font=HEADING_FONT, background=BACKGROUND_COLOR, foreground=NAVY_BLUE).pack(pady=20)
        print(f"Placeholder for {view_name}")

    def logout(self):
        # Perform logout logic
        self.auth_service.logout()
        self.current_user = None

        # Close all open Toplevel windows
        for window_name in list(self.open_windows.keys()): # Iterate over a copy of keys to avoid issues while modifying the dict
            window = self.open_windows.pop(window_name, None)
            if window and window.winfo_exists():
                window.destroy()

        # Show the login view again
        self.show_login_view()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
