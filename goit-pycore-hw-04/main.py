import sys
from constants import EXIT_PHRASES
from helpers import clear_screen
from calculate_total_salary import calculate_total_salary



def print_menu() -> None:
    print(
        "Press [1] to run Calculation Total Salary function (default file: salaries.txt)")
    print(
        "Press [2] to run Get Cats Info function (default file: cats_info.txt)")
    print(
        "Press [3] to run Directory Colorizer script (default directory: current directory)")
    print("Press [4] to run CLI Helper Bot")


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
                clear_screen()
                total, avg = calculate_total_salary()
                print(f"Total salary: {total}, Average salary: {avg}")
            case '2':
                clear_screen()
                print("CASE 2")
            case '3':
                clear_screen()
                print("CASE 3")
            case '4':
                clear_screen()
                print("CASE 4")
            case _:
                clear_screen()
                print(f"You enter: {user_input}. Use help for more info.")
    sys.exit()


if __name__ == "__main__":
    main()
