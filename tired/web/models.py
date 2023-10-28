import uuid
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.id = str(uuid.uuid4())

    def __to_dict__(self):
        return {
            "username": self.username,
            "password": self.password,
            "id": self.id
        }

