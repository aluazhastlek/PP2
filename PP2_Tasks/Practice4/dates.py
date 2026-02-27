from datetime import datetime, timedelta

# 1) Subtract five days from current date
current_date = datetime.now()                 # Get current date and time
five_days_ago = current_date - timedelta(days=5)  # Subtract 5 days

print("Current date:", current_date)
print("Five days ago:", five_days_ago)


# 2) Print yesterday, today, tomorrow
today = datetime.now().date()                 # Get today's date (without time)
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("\nYesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


# 3) Drop microseconds from datetime
now_with_micro = datetime.now()               # Current datetime with microseconds
now_without_micro = now_with_micro.replace(microsecond=0)  # Remove microseconds

print("\nWith microseconds:", now_with_micro)
print("Without microseconds:", now_without_micro)


# 4) Calculate difference between two dates in seconds
date1 = datetime(2025, 6, 1, 12, 0, 0)
date2 = datetime(2025, 6, 2, 12, 0, 0)

difference = date2 - date1                   # timedelta object
seconds = difference.total_seconds()         # Convert to seconds

print("\nDifference in seconds:", seconds)