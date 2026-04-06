import unittest
from datetime import date

from main import get_days_from_today, get_numbers_ticket, normalize_phone


class GetDaysFromToday(unittest.TestCase):
	""" Test cases for the get_days_from_today function. """

	def test_past_day(self):
		"""Test with a past date to ensure it returns a negative number of days."""

		test_date = "2021-10-09"
		expected = (date.fromisoformat(test_date) - date.today()).days
		result = get_days_from_today(test_date)
		self.assertIsInstance(result, int)
		self.assertEqual(result, expected)

	def test_today(self):
		"""Test with a today date to ensure it returns zero number of days."""

		result = get_days_from_today(str(date.today()))
		self.assertIsInstance(result, int)
		self.assertEqual(result, 0)

	def test_future_day(self):
		"""Test with a future date to ensure it returns a positive number of days."""

		test_date = "2028-12-09"
		result = get_days_from_today(test_date)
		self.assertIsInstance(result, int)
		self.assertGreater(result, 0)

	def test_invalid_month(self):
		"""Test with an invalid month to ensure it returns correct message."""

		test_date = "2020-20-20"
		self.assertIsNone(get_days_from_today(test_date))

	def test_valid_leap_year(self):
		"""Test with a valid leap year to ensure it returns correct message."""

		test_date = "2020-02-29"
		result = get_days_from_today(test_date)
		self.assertIsInstance(result, int)
		self.assertLess(result, 0)

	def test_invalid_leap_year(self):
		"""Test with an invalid leap year to ensure it returns correct message."""

		test_date = "2021-02-29"
		self.assertIsNone(get_days_from_today(test_date))


class GetNumbersTicket(unittest.TestCase):
	"""Test cases for the get_numbers_ticket function."""

	def test_common_lottery_6_of_49(self):
		"""Common lottery: 6 numbers from 1 to 49"""

		result = get_numbers_ticket(1, 49, 6)
		self.assertEqual(len(result), 6)
		self.assertEqual(result, sorted(result))
		self.assertEqual(len(set(result)), 6)
		self.assertTrue(all(1 <= n <= 49 for n in result))

	def test_common_lottery_5_of_36(self):
		""" Common lottery: 5 numbers from 1 to 36 """

		result = get_numbers_ticket(1, 36, 5)
		self.assertEqual(len(result), 5)
		self.assertEqual(result, sorted(result))
		self.assertEqual(len(set(result)), 5)
		self.assertTrue(all(1 <= n <= 36 for n in result))

	def test_quantity_equals_min(self):
		""" quantity == min: minimum number of tickets """

		result = get_numbers_ticket(9, 100, 9)
		self.assertEqual(len(result), 9)

	def test_quantity_equals_max(self):
		""" quantity == max: maximum number of tickets """

		result = get_numbers_ticket(1, 99, 99)
		self.assertEqual(len(result), 99)

	def test_one_number(self):
		""" min == max == quantity == 88 : only one number in the ticket """

		result = get_numbers_ticket(1, 1, 1)
		self.assertEqual(result, [1])

	def test_max_boundary(self):
		"""max == 1000: maximum boundary for max parameter"""
		result = get_numbers_ticket(1, 1000, 21)
		self.assertEqual(len(result), 21)
		self.assertTrue(all(1 <= n <= 1000 for n in result))

	def test_min_boundary(self):
		"""min == 1: minimum boundary for min parameter"""
		result = get_numbers_ticket(1, 100, 13)
		self.assertEqual(len(result), 13)

	def test_result_is_sorted(self):
		""" result == sorted """

		result = get_numbers_ticket(1, 1000, 24)
		self.assertEqual(result, sorted(result))

	def test_min_less_than_1(self):
		""" min less than 1: invalid parameter """

		self.assertEqual(get_numbers_ticket(0, 99, 20), [])

	def test_min_negative(self):
		""" min negative: invalid parameter """

		self.assertEqual(get_numbers_ticket(-1, 99, 20), [])

	def test_max_grater_than_1000(self):
		""" max greater than 1000: invalid parameter """

		self.assertEqual(get_numbers_ticket(1, 1001, 20), [])

	def test_quantity_less_than_min(self):
		""" quantity < min: quantity less than minimin invalid parameter """

		self.assertEqual(get_numbers_ticket(5, 100, 4), [])

	def test_min_greater_than_max(self):
		""" min greater than max: invalid parameter """

		self.assertEqual(get_numbers_ticket(19, 18, 5), [])

	def test_zero_quantity(self):
		""" zero quantity: invalid parameter """

		self.assertEqual(get_numbers_ticket(1, 99, 0), [])

	def test_min_equals_max_quantity_invalid(self):
		""" min equals max but quantity not equals min: invalid parameter """

		self.assertEqual(get_numbers_ticket(7, 7, 4), [])

	def test_max_exactly_1000_quantity_equal_max(self):
		""" max exactly 1000 and quantity == max: invalid parameter """

		result = get_numbers_ticket(1, 1000, 1000)
		self.assertEqual(len(result), 1000)


class NormalizePhone(unittest.TestCase):
	"""Test cases for the normalize_phone function."""

	def test_local_phone_number(self):
		self.assertEqual(normalize_phone("067\\t123 4567"), "+380671234567")

	def test_number_with_brackets_and_newline(self):
		self.assertEqual(normalize_phone("(095) 234-5678\n"), "+380952345678")


class GetUpcomingBirthdays(unittest.TestCase):
	"""Test cases for the get_upcoming_birthdays function."""
	pass


if __name__ == "__main__":
	unittest.main(verbosity=2)
