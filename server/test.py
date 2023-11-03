# This file is for testing purposes only


from datetime import datetime, timedelta


def get_index_of_date(d):
    # Get the current date and find the starting day (index 0,0) of the week
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    print(f"Start of the week: {start_of_week}")

    # Calculate the difference in days between the given date and the start of the week
    day_difference = (d - start_of_week).days

    # Calculate the index using the day difference and the 2D array structure (7 rows, 52 columns)
    row = day_difference % 7
    col = day_difference // 7

    return row, col


# Example usage:
given_date = datetime(2023, 10, 25)  # Replace this with your desired date
index = get_index_of_date(given_date)
print(f"Index of the date {given_date}: {index}")


# def get_bricks(records):
#     # Find the tiredness level for each date
#     bricks = {}
#
#     for record in records:
#         record_date = record.get('date', None)
#         if not record_date:
#             continue
#         # Get the number of records for this date
#         if record_date in bricks:
#             bricks[record_date] += 1
#         else:
#             bricks[record_date] = 1
#
#     return bricks


# def generate_wall(records, this_date=datetime.now()):
#     # Get the week number and day of the week
#     week_number, day_of_week = get_week_and_day(this_date)
#     print(week_number, day_of_week)
#
#     # Initialize an empty wall as a list of lists
#     wall = [[0 for _ in range(week_number)] for _ in range(7)]
#
#     # Calculate the remaining days for the last week
#     remaining_days = 6 - day_of_week
#
#     # Get the brick for each date
#     bricks = get_bricks(records)
#     # Assign the level of the day to the item in the wall
#     for brick in bricks:
#         brick_week, brick_day = get_week_and_day(brick)
#         wall[brick_day][week_number-brick_week] = bricks[brick]
#
#     # Fill the remaining days of the last week with 'O'
#     for i in range(remaining_days):
#         wall[day_of_week+i+1][0] = -1
#
#     for w_row in wall:
#         for w_col in w_row:
#             print(w_col, end=' ')
#         print()
#
#     return wall
#
#
# def generate_wall(records, this_date=datetime.now()):
#     # Get the week number and day of the week
#     week_number, day_of_week = get_week_and_day(this_date)
#     print(week_number, day_of_week)
#
#     # Initialize an empty wall as a list of lists
#     wall = [['0' for _ in range(week_number)] for _ in range(7)]
#
#     # Calculate the remaining days for the last week
#     remaining_days = 6 - day_of_week
#
#     # Fill the wall based on the existence of records
#     for record in records:
#         record_date = record.get('date', None)
#         if not record_date:
#             continue
#         record_week, record_day = get_week_and_day(record_date)
#         print(record_week, record_day)
#         wall[record_day][week_number-record_week] = 'X'
#
#     # Fill the remaining days of the last week with 'O'
#     for i in range(remaining_days):
#         wall[day_of_week+i+1][0] = 'O'
#
#     for row in wall:
#         for col in row:
#             print(col, end=' ')
#         print()
#
#     return wall

# # Example usage:
# sample_records = [
#     {"tired_level": "2", "add_notes": "Example note 1", "date": "2023-10-30", "time": "15:39:52"},
#     {"tired_level": "2", "add_notes": "Example note 2", "date": "2023-10-29", "time": "15:44:55"}
# ]
