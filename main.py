import re
from datetime import datetime
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

	modified_text = re.sub(r"\D", "", phone_number).strip()
	modified_text = re.sub(r"^38?", "", modified_text)
	modified_text = "+38" + modified_text
	return modified_text


def get_upcoming_birthdays(users: list[dict]) -> list[dict]:
	pass


raw_numbers = [
	"067\\t123 4567",
	"(095) 234-5678\\n",
	"+380 44 123 4567",
	"380501234567",
	"    +38(050)123-32-34",
	"     0503451234",
	"(050)8889900",
	"38050-111-22-22",
	"38050 111 22 11   ",
	]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)
