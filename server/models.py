from flask_login import UserMixin
from datetime import datetime
from .utils import get_brick_index, get_year_week_day
from server import ai_client


"""USER"""


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('_id', None)
        return str(object_id)


class Brick:
    def __init__(self, record_count=0, record_value=0):
        self.record_count = record_count
        self.record_sum = record_value
        self.color = self.get_brick_color()

    def update(self, tired_level):
        self.record_count += 1
        self.record_sum += int(tired_level)
        self.color = self.get_brick_color()

    def get_brick_color(self):
        if self.record_count == 0 or self.record_sum == 0:
            return '#EBEDF0'
        else:
            #  Determine the color of the brick based on the average tired level and the number of records
            rank = 0.5 * self.record_sum / self.record_count + self.record_count * 0.5
            if rank == 0:
                return '#EBEDF0'
            elif rank < 3:
                return '#FAF04D'
            elif rank < 4:
                return '#FFC002'
            elif rank < 5:
                return '#F79218'
            else:
                return '#6b4323'

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
        brick.color = brick_json.get('color', '#EBEDF0')
        return brick


class Wall:
    def __init__(self, bricks):
        self.wall_list = [['#EBEDF0' for _ in range(52)] for _ in range(7)]
        self.build_wall(bricks)

    def build_wall(self, bricks, this_date=datetime.now()):
        this_year, this_week, this_day = get_year_week_day(this_date)
        # Assign the level of the day to the item in the wall
        for date, brick_json in bricks.items():
            # brick_week, brick_day = get_week_and_day(date)
            # self.wall_list[brick_day][self.week_number - brick_week] = brick_json.get('color', 'lightgrey')
            row, col = get_brick_index(date, this_year, this_week)
            # jump the brick if it's out of range
            if row < 0 or row > 6 or col < 0 or col > 51:
                continue
            self.wall_list[row][col] = brick_json.get('color', '#EBEDF0')
        # Fill the remaining days of the last week with ' '
        for day in range(this_day + 1, 7):
            self.wall_list[day][0] = ' '

        # for w_row in self.wall_list:
        #     for w_col in w_row:
        #         print(w_col, end=' ')
        #     print()


"""CHATBOT"""


class Chat:
    def __init__(self):
        self.conversation = [
            {
                "role": "assistant",
                "content": "Hello, I am your personal assistant. I am here to help you with your daily life. What can I do for you?",
            }
        ]

    def __repr__(self):
        # return a representation of the chat
        return f"[Chat: {self.conversation}]"

    def get_ai_response(self, user_in: str = None):
        if user_in is None or len(user_in) == 0:
            return 'I\'m sorry, I don\'t understand.'
        else:
            user_in += ' Answer me in 100 words or less.'

        self.conversation.append({
            "role": "user",
            "content": user_in,
        })

        try:
            reply = ai_client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=self.conversation,
                max_tokens=128,
            )
            print(reply)
            reply_text = str(reply.choices[0].message.content)
        except Exception as e:
            print(e)
            reply_text = 'I\'m sorry, I don\'t understand.'

        self.conversation.append({
            "role": "assistant",
            "content": reply_text,
        })
        return reply_text
