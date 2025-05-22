from app.models.user_model import User

class AuthService:
    def __init__(self):
        self.users = [
            User(1, "admin", "admin123", "Admin", "admin@example.com", "Admin User"),
            User(2, "teacher1", "teacher123", "Teacher", "teacher1@example.com", "Prof. Ada"),
            User(3, "student1", "student123", "Student", "student1@example.com", "John Doe")
        ]
        self.current_user = None

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"User {username} logged in successfully as {user.role}.")
                return user
        print("Invalid username or password.")
        return None

    def logout(self):
        print(f"User {self.current_user.username if self.current_user else 'None'} logged out.")
        self.current_user = None

    def get_current_user(self):
        return self.current_user

    def register_user(self, username, password, role, email, full_name):
        # In a real app, check for existing username/email and save to DB
        new_id = len(self.users) + 1
        new_user = User(new_id, username, password, role, email, full_name)
        self.users.append(new_user)
        print(f"User {username} registered successfully as {role}.")
        return new_user