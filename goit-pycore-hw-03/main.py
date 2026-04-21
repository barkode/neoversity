import re
from datetime import datetime, timedelta
from random import randint
from data import users


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

