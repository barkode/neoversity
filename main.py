from datetime import datetime
from random import randint

def get_days_from_today(date: str) -> int | None:
	try:
		user_date = datetime.strptime(date, "%Y-%m-%d").date()
	except ValueError as e:
		print(
			f"Not correct date '{date}'. {str(e).capitalize()}. Please, use date format as 'YYYY-MM-DD'.")
		return None
	delta_time = user_date - datetime.today().date()
	return int(delta_time.days)


def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int | None]:
	try:
		if min < 1 or max > 1000 or not min <= quantity <= max:
			return []
		numbers_ticket = set()
		while len(numbers_ticket) != quantity:
			number = randint(min, max)
			numbers_ticket.add(number)
		return sorted(numbers_ticket)
	except ValueError as e:
		return []
