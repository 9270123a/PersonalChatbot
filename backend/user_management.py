import json
import hashlib

class UserManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        if username in self.users:
            return False, "User already exists"
        self.users[username] = self.hash_password(password)
        self.save_users()
        return True, "User registered successfully"

    def login_user(self, username, password):
        if username not in self.users:
            return False, "User does not exist"
        if self.users[username] == self.hash_password(password):
            return True, "Login successful"
        return False, "Incorrect password"