from datetime import datetime
from random import choice, randint

import faker

NUMBER_COMPANIES = 3
NUMBER_EMPLOYEES = 30
NUMBER_POST = 5


def generate_fake_data(number_companies, number_employees, number_post) -> \
        tuple[list, list, list]:
    fake_companies = []
    fake_employees = []
    fake_posts = []
    fake_data = faker.Faker()

    for _ in range(number_companies):
        fake_companies.append(fake_data.company())

    for _ in range(number_employees):
        fake_employees.append(fake_data.name())

    for _ in range(number_post):
        fake_posts.append(fake_data.job())

    return fake_companies, fake_employees, fake_posts


def prepare_data(companies, employees, posts) -> tuple[list, list, list]:
    for_companies = []
    for_employees = []
    for_payments = []

    for company in companies:
        for_companies.append((company,))

    for employee in employees:
        for_employees.append(
            (employee, choice(posts), randint(1, NUMBER_COMPANIES)))

    for month in range(1, 12 + 1):
        payment_date = datetime(2021, month, randint(10, 20)).date()
        for emp in range(1, NUMBER_EMPLOYEES + 1):
            for_payments.append((emp, payment_date, randint(1000, 10000)))

    return for_companies, for_employees, for_payments
