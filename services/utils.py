from datetime import datetime


# def get_week_and_day(date):
#     # Convert the string date to a datetime object if it's a string
#     if isinstance(date, str):
#         date = datetime.strptime(date, '%Y-%m-%d')
#
#     week_number = date.isocalendar()[1]  # Week number in the year
#     day_of_week = date.weekday()  # Day of the week (0 for Monday, 6 for Sunday)
#
#     return week_number, day_of_week


def get_year_week_day(date):
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')

    year = date.year
    week = date.isocalendar()[1]
    day_of_week = date.weekday()

    return year, week, day_of_week


def weeks_of_year(year):
    last_day = datetime.date(year, 12, 31)
    week_num = last_day.isocalendar()
    return week_num


def get_brick_index(date, this_year, this_week):
    brick_year, brick_week, brick_day = get_year_week_day(date)
    row = brick_day
    # if these dates are in the same year
    if this_year == brick_year:
        col = this_week - brick_week
    elif this_year - brick_year == 1:
        last_year_weeks = weeks_of_year(brick_year)
        col = this_week + int(last_year_weeks) - brick_week
    else:
        col = -1

    return row, col


# TODO: define a algorithm to calculate the color of brick of a date
