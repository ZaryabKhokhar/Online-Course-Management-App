import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from app.utils.style import HEADING_FONT, MAIN_FONT
from datetime import datetime

class MessageBoardView(tk.Toplevel):
    def __init__(self, master, current_user, on_close_callback=None): # Add services as needed
        super().__init__(master)
        self.current_user = current_user
        self.on_close_callback = on_close_callback
        
        self.messages = [ # Sample messages
            {"user": "Admin", "timestamp": "2025-05-20 10:00", "text": "Welcome to the new semester!"},
            {"user": "Teacher Ada", "timestamp": "2025-05-20 11:30", "text": "Python Assignment 1 due next Friday."}
        ]

        self.title("Message Board / Announcements")
        self.geometry("700x500")
        self.configure(bg="#ecf0f1")

        if self.on_close_callback:
            self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        self.create_widgets()
        self.load_messages()

    def on_close_window(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Announcements & Messages", font=HEADING_FONT).pack(pady=10)

        self.message_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED, height=15, font=MAIN_FONT)
        self.message_display.pack(pady=10, fill="both", expand=True)
        
        if self.current_user.role in ["Admin", "Teacher"]:
            input_frame = ttk.Frame(main_frame)
            input_frame.pack(fill=tk.X, pady=(0,10))

            self.message_entry = ttk.Entry(input_frame, font=MAIN_FONT, width=60)
            self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,10))
            
            post_button = ttk.Button(input_frame, text="Post Message", command=self.post_message, style="Accent.TButton")
            post_button.pack(side=tk.LEFT)

    def load_messages(self):
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete('1.0', tk.END)
        for msg in self.messages:
            self.message_display.insert(tk.END, f"[{msg['timestamp']}] {msg['user']}:\n{msg['text']}\n\n")
        self.message_display.config(state=tk.DISABLED)
        print("Messages loaded.")

    def post_message(self):
        if self.current_user.role not in ["Admin", "Teacher"]:
            messagebox.showerror("Permission Denied", "You do not have permission to post messages.")
            return

        new_message_text = self.message_entry.get()
        if not new_message_text.strip():
            messagebox.showwarning("Empty Message", "Cannot post an empty message.")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        user_name = self.current_user.full_name if self.current_user.full_name else self.current_user.username
        
        self.messages.append({"user": user_name, "timestamp": timestamp, "text": new_message_text})
        
        # In a real app, save this message to the database via a service
        print(f"User {user_name} posted: {new_message_text}")
        
        self.message_entry.delete(0, tk.END)
        self.load_messages() # Refresh the display