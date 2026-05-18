from collections import UserDict


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

    def __validate(self, value) -> bool:
        return value.isdigit() and len(value) == 10


class Record:
    """A class for storing contact information, including name and phone number."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"

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


class AddressBook(UserDict):
    """A class for storing and managing records."""

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
