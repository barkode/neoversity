import sqlite3
from datetime import datetime
from random import choice, randint

import faker

NUMBER_COMPANIES = 3
NUMBER_EMPLOYEES = 30
NUMBER_POST = 5


def generate_fake_data(number_companies, number_employees, number_post) -> \
        tuple[list, list, list]:
    fake_data = faker.Faker()
    fake_companies = [fake_data.company() for _ in range(number_companies)]
    fake_employees = [fake_data.name() for _ in range(number_employees)]
    fake_posts = [fake_data.job() for _ in range(number_post)]

    return fake_companies, fake_employees, fake_posts


def prepare_data(companies, employees, posts) -> tuple[list, list, list]:
    for_companies = [(c,) for c in companies]
    for_employees = [(emp, choice(posts), randint(1, len(companies))) for emp
                     in employees]
    for_payments = []

    for month in range(1, 12 + 1):
        payment_date = datetime(2021, month, randint(10, 20)).date()
        for emp_id in range(1, len(employees) + 1):
            for_payments.append(
                (emp_id, payment_date.isoformat(), randint(1000, 10000)))

    return for_companies, for_employees, for_payments


def insert_data_to_db(companies, employees, payments) -> None:
    with sqlite3.connect("salary.db") as con:
        cur = con.cursor()

        sql_to_companies = """INSERT INTO companies(company_name)
                              VALUES (?)"""
        cur.executemany(sql_to_companies, companies)
        sql_to_employees = """INSERT INTO employees(employee, post, company_id)
                              VALUES (?, ?, ?)"""
        cur.executemany(sql_to_employees, employees)
        sql_to_payments = """INSERT INTO payments(employee_id, date_of, total)
                             VALUES (?, ?, ?)"""
        cur.executemany(sql_to_payments, payments)


if __name__ == "__main__":
    companies, employees, payments = prepare_data(
        *generate_fake_data(NUMBER_COMPANIES, NUMBER_EMPLOYEES, NUMBER_POST))
    insert_data_to_db(companies, employees, payments)
