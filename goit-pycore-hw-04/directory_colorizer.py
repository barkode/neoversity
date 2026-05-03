import sys
import os
from pathlib import Path
from colorama import Fore, Style, init
from helpers import COLOUR_SCHEMA


def clear_screen():
    """function that clears screen"""
    os.system("cls" if os.name == "nt" else "clear")


def print_directory_tree(path, indent=""):
    for item in path.iterdir():
        if item.is_dir():
            colour = COLOUR_SCHEMA.get("directory")
            icon = COLOUR_SCHEMA.get("icon_directory")
            print(indent + colour + icon + item.name)
            print_directory_tree(item, indent + "    ")
        else:
            ext = item.suffix.lower()
            colour = COLOUR_SCHEMA.get(ext, COLOUR_SCHEMA["default"])
            icon_file = COLOUR_SCHEMA.get("icon_file")
            print(indent + colour + icon_file + item.name)


def system_check():
    """function that checks whether system is available"""
    return "posix" if os.name == "posix" else "nt"


def main():
    init(autoreset=True)

    clear_screen()

    if len(sys.argv) != 2:
        print(f"Помилка: потрібно передати шлях до директорії.")
        print(f"Приклад: python3 {sys.argv[0]} <шлях до директорії>")
        return

    directory_path = Path(sys.argv[1])

    if not directory_path.exists():
        print("Помилка: такого шляху не існує.")
        return

    if not directory_path.is_dir():
        print("Помилка: вказаний шлях не є директорією.")
        return

    print(Fore.YELLOW + f"Структура директорії: {directory_path}")
    print_directory_tree(directory_path)
    print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
