import sys
from constants import EXIT_PHRASES


def parse_input(user_input):
    parts = user_input.strip().split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


def add_contact(args, contacts):
    if len(args) != 2:
        return "Usage: add [name] [phone]"

    name, phone = args
    contacts[name] = phone
    return "Contact added."


def change_contact(args, contacts):
    if len(args) != 2:
        return "Usage: change [name] [new_phone]"

    name, phone = args

    if name not in contacts:
        return "Contact not found."

    contacts[name] = phone
    return "Contact updated."


def show_phone(args, contacts):
    if len(args) != 1:
        return "Usage: phone [name]"

    name = args[0]

    if name not in contacts:
        return "Contact not found."

    return contacts[name]


def show_all(contacts):
    if not contacts:
        return "No contacts found."

    result = []

    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")

    return "\n".join(result)


def print_help():
    """function that prints help"""
    help_text = """Available commands:
- hello: Greet the bot.
- add [name] [phone]: Add a new contact.
- change [name] [new_phone]: Change the phone number of an existing contact.
- phone [name]: Show the phone number of a contact.
- all: Show all contacts.
- help: Show this help message.
- exit, quit, bye: Exit the bot."""
    print(help_text)


def main():
    contacts = {}

    print("Welcome to the assistant bot!")

    while True:

        user_input = input("Enter a command or <help> to see all commands\n: ")
        command, args = parse_input(user_input)

        match command:
            case cmd if cmd in EXIT_PHRASES:
                print("Good bye!")
                break

            case "hello":
                print("Hello there! What we're looking for?")
            case "add":
                add_contact(args, contacts)
            case "change":
                change_contact(args, contacts)
            case "phone":
                show_phone(args, contacts)
            case "all":
                show_all(contacts)
            case "help":
                print_help()
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
