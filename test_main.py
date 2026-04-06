import unittest
from datetime import date

from main import get_days_from_today, get_numbers_ticket


class GetDaysFromToday(unittest.TestCase):
	def test_past_day(self):
		result = get_days_from_today("2021-10-09")
		self.assertIsInstance(result, int)
		self.assertEqual(result, -1640)

	def test_today(self):
		result = get_days_from_today(str(date.today()))
		self.assertIsInstance(result, int)
		self.assertEqual(result, 0)

	def test_future_day(self):
		result = get_days_from_today("2028-12-09")
		self.assertIsInstance(result, int)
		self.assertGreater(result, 0)

	def test_invalid_month(self):
		self.assertIsNone(get_days_from_today("2020-20-20"))

	def test_valid_leap_year(self):
		result = get_days_from_today("2020-02-29")
		self.assertIsInstance(result, int)
		self.assertLess(result, 0)

	def test_invalid_leap_year(self):
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


class NormalizePhone(unittest.TestCase):
	pass


class GetUpcomingBirthdays(unittest.TestCase):
	pass


if __name__ == "__main__":
	unittest.main()
