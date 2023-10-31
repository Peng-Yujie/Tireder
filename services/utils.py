from datetime import datetime


def get_week_and_day(date):
    # Convert the string date to a datetime object if it's a string
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')

    week_number = date.isocalendar()[1]  # Week number in the year
    day_of_week = date.weekday()  # Day of the week (0 for Monday, 6 for Sunday)

    return week_number, day_of_week


def generate_wall(records, this_date=datetime.now()):
    # Get the week number and day of the week
    week_number, day_of_week = get_week_and_day(this_date)
    print(week_number, day_of_week)

    # Initialize an empty wall as a list of lists
    wall = [['0' for _ in range(week_number)] for _ in range(7)]

    # Calculate the remaining days for the last week
    remaining_days = 6 - day_of_week

    # Fill the wall based on the existence of records
    for record in records:
        record_date = record.get('date', None)
        if not record_date:
            continue
        record_week, record_day = get_week_and_day(record_date)
        print(record_week, record_day)
        wall[record_day][week_number-record_week] = 'X'

    # Fill the remaining days of the last week with 'O'
    for i in range(remaining_days):
        wall[day_of_week+i+1][0] = 'O'

    for row in wall:
        for col in row:
            print(col, end=' ')
        print()

    return wall

# # Example usage:
# sample_records = [
#     {"tired_level": "2", "add_notes": "Example note 1", "date": "2023-10-30", "time": "15:39:52"},
#     {"tired_level": "2", "add_notes": "Example note 2", "date": "2023-10-29", "time": "15:44:55"}
# ]
#
# # Generate a contribution wall
# wall = generate_wall(sample_records)
# for row in wall:
#     print(' '.join(row))  # Print each row of the wall