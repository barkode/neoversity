import unittest
from datetime import date

from main import get_days_from_today, get_numbers_ticket


class GetDaysFromToday(unittest.TestCase):
	def test_past_day(self):
		"""Test with a past date to ensure it returns a negative number of days."""
		result = get_days_from_today("2021-10-09")
		self.assertIsInstance(result, int)
		self.assertEqual(result, -1640)

	def test_today(self):
		"""Test with a today date to ensure it returns zero number of days."""
		result = get_days_from_today(str(date.today()))
		self.assertIsInstance(result, int)
		self.assertEqual(result, 0)

	def test_future_day(self):
		"""Test with a future date to ensure it returns a positive number of days."""
		result = get_days_from_today("2028-12-09")
		self.assertIsInstance(result, int)
		self.assertGreater(result, 0)

	def test_invalid_month(self):
		"""Test with an invalid month to ensure it returns correct message."""
		self.assertIsNone(get_days_from_today("2020-20-20"))

	def test_valid_leap_year(self):
		"""Test with a valid leap year to ensure it returns correct message."""
		result = get_days_from_today("2020-02-29")
		self.assertIsInstance(result, int)
		self.assertLess(result, 0)

	def test_invalid_leap_year(self):
		"""Test with an invalid leap year to ensure it returns correct message."""
		self.assertIsNone(get_days_from_today("2021-02-29"))


class GetNumbersTicket(unittest.TestCase):

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

		result = get_numbers_ticket(88, 88, 1)
		self.assertEqual(result, [88])


class NormalizePhone(unittest.TestCase):
	pass


class GetUpcomingBirthdays(unittest.TestCase):
	pass


if __name__ == "__main__":
	unittest.main()
