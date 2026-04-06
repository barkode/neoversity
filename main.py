from datetime import datetime, date

def get_days_from_today(date: str) -> int:
    try:
        user_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        print(f"Not correct date '{date}'. {str(e).capitalize()}. Please, use date format as 'YYYY-MM-DD'.")
        return None
    delta_time = user_date - datetime.today().date()
    return delta_time.days

assert get_days_from_today("2021-10-09") == -1640 # -1640

d = str(date.today())
assert get_days_from_today(d) == 0 # 0 (today)

assert get_days_from_today("2028-12-09") > 0 # positive (future)

assert get_days_from_today("2020-20-20") is None # Error message, returns None

assert get_days_from_today("2021-02-29") is None # Valid leap year date
assert get_days_from_today("2020-02-29") < 0 # Valid leap year date

assert get_days_from_today("2021-02-29") is None # Error message, returns None