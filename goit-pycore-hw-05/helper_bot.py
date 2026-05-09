from constants import EXIT_PHRASES


def parse_input(user_input: str) -> tuple:
    parts = user_input.strip().lower().split()
    return parts[0], parts[1:] if parts else ("", [])


def add_contact(args: list, contacts: dict) -> str:
    if len(args) != 2:
        return "Usage: add [name] [phone]"

    name, phone = args
    name = name.strip().capitalize()
    contacts[name] = phone
    return "Contact added."


def change_contact(args: list, contacts: dict) -> str:
    if len(args) != 2:
        return "Usage: change [name] [new_phone]"

    name, phone = args

    if name not in contacts:
        return "Contact not found."

    contacts[name] = phone
    return "Contact updated."


def show_phone(args: list, contacts: dict) -> str:
    if len(args) != 1:
        return "Usage: phone [name]"

    name = args[0]

    if name not in contacts:
        return "Contact not found."

    return contacts[name]


def show_all(contacts: dict) -> str:
    if not contacts:
        return "No contacts found."

    result = [f"{name}: {phone}" for name, phone in sorted(contacts.items())]

    return "\n".join(result)


def show_help():
    """function that prints help"""
    return """Available commands:
- hello: Greet the bot.
- add [name] [phone]: Add a new contact.
- change [name] [new_phone]: Change the phone number of an existing contact.
- phone [name]: Show the phone number of a contact.
- all: Show all contacts.
- help: Show this help message.
- exit, quit, bye: Exit the bot."""


def main() -> None:
    contacts: dict = {}

    print("Welcome to the assistant bot!")
    print("Type 'help' to see all available commands.")

    while True:

        try:
            user_input = input(
                "Enter a command\n: ")
            command, args = parse_input(user_input)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not command:
            print("Please enter a command.")
            continue

        match command:
            case cmd if cmd in EXIT_PHRASES:
                print("Good bye!")
                break

            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args, contacts))
            case "phone":
                print(show_phone(args, contacts))
            case "all":
                print(show_all(contacts))
            case "help":
                print(show_help())
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
