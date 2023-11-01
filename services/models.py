from flask_login import UserMixin
from datetime import datetime
from services.utils import get_week_and_day


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get("_id")
        return str(object_id)


class Brick:
    def __init__(self, record_count=0, record_value=0):
        self.record_count = record_count
        self.record_sum = record_value
        self.color = 'lightgrey'

    def update(self, tired_level):
        self.record_count += 1
        self.record_sum += int(tired_level)
        self.color = self.get_brick_color()

    def get_brick_color(self):
        if self.record_count == 0 or self.record_sum == 0:
            return 'lightgrey'
        else:
            rank = self.record_sum / self.record_count  # TODO: Change this to a better algorithm
            if rank < 3:
                return 'green'
            elif rank < 5:
                return 'yellow'
            else:
                return 'red'

    def to_json(self):
        return {
            "record_count": self.record_count,
            "record_sum": self.record_sum,
            "color": self.color
        }

    @staticmethod
    def from_json(brick_json):
        record_count = brick_json.get('record_count', 0)
        record_sum = brick_json.get('record_sum', 0)
        brick = Brick(record_count, record_sum)
        brick.color = brick_json.get('color', 'lightgrey')
        return brick

    # def __init__(self, brick_json):
    #     self.brick_json = brick_json
    #
    # def update_brick(self, tired_level):
    #     if 'record_count' in self.brick_json:
    #         record_count = int(self.brick_json['record_count'])
    #         self.brick_json['record_count'] = record_count + 1
    #     else:
    #         self.brick_json['record_count'] = 1
    #     if 'record_sum' in self.brick_json:
    #         record_sum = int(self.brick_json['record_sum'])
    #         self.brick_json['record_sum'] = record_sum + int(tired_level)
    #     else:
    #         self.brick_json['record_sum'] = int(tired_level)
    #     self.brick_json['color'] = self.get_brick_color()
    #
    #     return self.brick_json
    #
    # def get_brick_color(self):
    #     if 'record_count' not in self.brick_json or 'record_sum' not in self.brick_json:
    #         return 'lightgrey'
    #     else:
    #         rank = self.brick_json['record_sum'] / self.brick_json['record_count']
    #         if rank < 3:
    #             return 'green'
    #         elif rank < 5:
    #             return 'yellow'
    #         else:
    #             return 'red'


class Wall:
    def __init__(self, bricks, this_date=datetime.now()):
        self.week_number, self.day_of_week = get_week_and_day(this_date)
        self.wall_list = [['lightgrey' for _ in range(52)] for _ in range(7)]
        self.build_wall(bricks)

    def build_wall(self, bricks):
        # Assign the level of the day to the item in the wall
        for date, brick_json in bricks.items():
            brick_week, brick_day = get_week_and_day(date)
            self.wall_list[brick_day][self.week_number - brick_week] = brick_json.get('color', 'lightgrey')

        # Fill the remaining days of the last week with ' '
        remaining_days = 6 - self.day_of_week
        for i in range(remaining_days):
            self.wall_list[self.day_of_week + i + 1][0] = ' '

        # for w_row in self.wall_list:
        #     for w_col in w_row:
        #         print(w_col, end=' ')
        #     print()


