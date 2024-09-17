from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# For simplicity, we'll use an in-memory user store. In a real application, use a database.
users = {}

def create_user(username, password):
    if username not in users:
        users[username] = User(username, username, password)
        return True
    return False

def get_user(username):
    return users.get(username)