from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get("_id")
        return str(object_id)


# Define tiredness level
class Tiredness:
    LEVELS = {
        1: "A LITTLE TIRED",
        2: "TIRED",
        3: "VERY TIRED",
        4: "FXXKING TIRED"
    }

    COLORS = {
        1: "green",
        2: "yellow",
        3: "orange",
        4: "red"
    }

    def __init__(self, level, note=None):
        self.level = level
        self.note = note if note else None

    def to_dict(self):
        return {
            "level": self.level,
            "note": self.note
        }

    def get_color(self):
        return self.COLORS.get(self.level, "White")

    def get_level(self):
        return self.LEVELS.get(self.level, 0)
