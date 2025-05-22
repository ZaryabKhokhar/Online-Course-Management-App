import tkinter as tk
from tkinter import ttk, messagebox
from app.services.auth_service import AuthService
from app.utils.style import HEADING_FONT, MAIN_FONT

class LoginView(tk.Frame):
    def __init__(self, master, show_main_app_callback):
        super().__init__(master)
        self.master = master
        self.show_main_app_callback = show_main_app_callback
        self.auth_service = AuthService() # This should ideally be passed or be a singleton

        self.master.title("Login - Online Course Management System")
        self.master.geometry("400x300")
        self.master.configure(bg="#ecf0f1")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Login", font=HEADING_FONT).pack(pady=10)

        ttk.Label(main_frame, text="Username:", font=MAIN_FONT).pack(pady=(10,0))
        self.username_entry = ttk.Entry(main_frame, font=MAIN_FONT, width=30)
        self.username_entry.pack()
        self.username_entry.insert(0, "admin") # Default for testing

        ttk.Label(main_frame, text="Password:", font=MAIN_FONT).pack(pady=(10,0))
        self.password_entry = ttk.Entry(main_frame, show="*", font=MAIN_FONT, width=30)
        self.password_entry.pack()
        self.password_entry.insert(0, "admin123") # Default for testing

        login_button = ttk.Button(main_frame, text="Login", command=self.attempt_login, style="Accent.TButton")
        login_button.pack(pady=20, ipadx=10, ipady=5)
        
        # Basic style for the button
        style = ttk.Style()
        style.configure("Accent.TButton", font=MAIN_FONT, background="#3498db", foreground="black")
        style.map("Accent.TButton", background=[('active', '#2980b9')])


    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.auth_service.login(username, password)
        if user:
            messagebox.showinfo("Login Successful", f"Welcome {user.full_name} ({user.role})!")
            self.show_main_app_callback(user) # Pass the user object
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")