from collections import UserDict


class Field:
    """Base class for record fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing contact name. Required field."""
    pass


class Phone(Field):
    """Class for storing phone numbers. Has format validation (10 digits)."""
    pass


class Record:
    """A class for storing contact information, including name and phone number."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """A class for storing and managing records."""
    pass
