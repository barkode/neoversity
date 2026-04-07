import re
from datetime import datetime, timedelta
from random import randint


def get_days_from_today(date: str) -> int | None:
    """Calculate the number of days from today to the given date."""

    try:
        user_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as e:
        print(
            f"Not correct date '{date}'. {str(e).capitalize()}. Please, use date format as 'YYYY-MM-DD'.")
        return None
    delta_time = user_date - datetime.today().date()
    return int(delta_time.days)


def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    """ Calculate the numbers of tickets from the given min and max dates."""

    if min < 1 or max > 1000 or not (min <= quantity <= max):
        return []

    numbers_ticket = set()
    while len(numbers_ticket) != quantity:
        number = randint(min, max)
        numbers_ticket.add(number)
    return sorted(numbers_ticket)


def normalize_phone(phone_number: str) -> str:
    """Function to normalize the phone number"""

    modified_text = re.sub(r"\D", "", phone_number)
    modified_text = re.sub(r"^38", "", modified_text)
    modified_text = "+38" + modified_text
    return modified_text


def get_upcoming_birthdays(users: list[dict]) -> list[dict]:
    """Function to get upcoming birthdays from users"""

    today_date = datetime.today().date()
    upcoming_birthdays = []

    for user in users:
        name = user["name"]
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        birthday_this_year = datetime(year=today_date.year,
                                      month=birthday.month,
                                      day=birthday.day).date()

        if birthday_this_year < today_date:
            birthday_this_year = datetime(year=today_date.year + 1,
                                          month=birthday.month,
                                          day=birthday.day).date()

        days_to_birthday = (birthday_this_year - today_date).days

        if 0 <= days_to_birthday <= 7:
            congratulation_date = birthday_this_year
            weekday = birthday_this_year.weekday()

            if weekday == 5:
                congratulation_date += timedelta(days=2)
            elif weekday == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append(
                {"name": user["name"],
                 "congratulation_date": congratulation_date.strftime(
                     "%Y-%m-%d"), })
        else:
            continue

    return upcoming_birthdays
