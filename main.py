from datetime import datetime

def get_days_from_today(date: str) -> int:
    try:
        user_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        print(f"Sorry, {e}")
        return None
    delta_time = user_date - datetime.today().date()
    return delta_time.days

get_days_from_today("2021-10-09") # −157
get_days_from_today("2026-04-06") # 0 (today)
get_days_from_today("2028-12-09") # positive (future)
get_days_from_today("2020-20-20") # Error message, returns None
get_days_from_today("2020-02-29") # Valid leap year date
get_days_from_today("2021-02-29") # Error message, returns None