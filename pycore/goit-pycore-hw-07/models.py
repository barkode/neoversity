from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Base class for record fields."""

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Class for storing contact name. Required field."""
    pass


class Phone(Field):
    """Class for storing phone numbers. Has format validation (10 digits)."""

    def __init__(self, value) -> None:
        if not self.__validate(value):
            raise ValueError("Phone number must be exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def __validate(self, value) -> bool:
        return value.isdigit() and len(value) == 10


class Record:
    """A class for storing contact information, including name and phone number."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime(
            "%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            self.phones.append(Phone(new_phone))
        else:
            raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    """A class for storing and managing records."""

    def add_record(self, record) -> Record:
        self.data[record.name.value] = record

    def find(self, name) -> Record | None:
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record {name} not found")

    def get_upcoming_birthdays(self) -> list[dict]:
        """Function to get upcoming birthdays from records"""

        today_date = datetime.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

        birthday = record.birthday.value
        birthday_this_year = birthday_this_year = birthday.replace(
            year=today_date.year)

        if birthday_this_year < today_date:
            birthday_this_year = birthday.replace(year=today_date.year + 1)

        days_to_birthday = (birthday_this_year - today_date).days

        if 0 <= days_to_birthday <= 7:
            congratulation_date = birthday_this_year
            weekday = birthday_this_year.weekday()

            if weekday == 5:
                congratulation_date += timedelta(days=2)
            elif weekday == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append({
                "name": record.name.value,
                "congratulation_date": congratulation_date.strftime(
                    "%Y-%m-%d"),
                })

        return upcoming_birthdays


class Birthday(Field):
    def __init__(self, value) -> None:
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
