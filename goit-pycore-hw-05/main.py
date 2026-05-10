import sys

from helpers import clear_screen
from calculate_total_salary import calculate_total_salary
from cats_info import get_cats_info
from helper_bot import main as run_helper_bot
from directory_colorizer import main as run_directory_colorizer
from dictionaries import EXIT_PHRASES


def print_menu() -> None:
    """Print the menu."""
    print("Press [1] to run Calculation Total Salary function")
    print("Press [2] to run Get Cats Info function")
    print("Press [3] to run Directory Colorizer script")
    print("Press [4] to run CLI Helper Bot")
    print("Press [quit] to exit")


def pause() -> None:
    input("Press any key to continue...")
    clear_screen()


def prompt_path(message: str, default_path: str) -> str:
    """Prompt the user to enter a valid path and return it."""
    user_value = input(f"{message} [{default_path}]: ").strip()
    return user_value or default_path


def handle_helper_bot() -> None:
    clear_screen()
    run_helper_bot()
    pause()


def handle_directory_colorizer() -> None:
    clear_screen()
    path = prompt_path("Enter directory path", DEFAULT_PATH)
    run_directory_colorizer(path)
    pause()


def handle_cats_info() -> None:
    clear_screen()
    path = prompt_path("Enter cats info file path", DEFAULT_CATS_INFO_PATH)
    cats = get_cats_info(path)

    if not cats:
        print("No cats found.")
        pause()
        return

    print("Cats info:")
    for cat in cats:
        print(f"- ID: {cat['id']}, Name: {cat['name']}, Age: {cat['age']}")

    pause()


def handle_salary_calculation() -> None:
    clear_screen()
    path = prompt_path("Enter salaries file path", DEFAULT_SALARIES_PATH)
    total, average = calculate_total_salary(path)
    print(f"Total salary: {total}")
    print(f"Average salary: {average}")
    pause()


def main():
    clear_screen()
    while True:
        print_menu()
        user_input = input(
            "Enter command (or 'quit' for exit): ").strip().lower()

        match user_input:
            case cmd if cmd in EXIT_PHRASES:
                print("Goodbye!")
                clear_screen()
                break
            case '1':
                handle_salary_calculation()
            case '2':
                handle_cats_info()
            case '3':
                handle_directory_colorizer()
            case '4':
                handle_helper_bot()
            case _:
                clear_screen()
                print(f"You enter: {user_input}. Use help for more info.")
    sys.exit()


if __name__ == "__main__":
    main()
