from flask_login import UserMixin
import uuid


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.id = str(uuid.uuid4())

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "id": self.id
        }

    def from_dict(dict):
        user = User(dict["username"], dict["password"])
        user.id = dict["id"]
        return user
