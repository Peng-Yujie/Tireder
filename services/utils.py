from datetime import datetime


def get_week_and_day(date):
    # Convert the string date to a datetime object if it's a string
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')

    week_number = date.isocalendar()[1]  # Week number in the year
    day_of_week = date.weekday()  # Day of the week (0 for Monday, 6 for Sunday)

    return week_number, day_of_week
