from datetime import datetime


def get_days_from_today(date: str) -> int:
	try:
		user_date = datetime.strptime(date, "%Y-%m-%d").date()
	except ValueError as e:
		print(
			f"Not correct date '{date}'. {str(e).capitalize()}. Please, use date format as 'YYYY-MM-DD'.")
		return None
	delta_time = user_date - datetime.today().date()
	return int(delta_time.days)


def get_numbers_ticket(min, max, quantity):
	pass
