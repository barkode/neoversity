import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)


# def print_directory_tree(path, indent=""):
#     for item in path.iterdir():
#         if item.is_dir():
#             print(indent + Fore.BLUE + "📁 " + item.name)
#             print_directory_tree(item, indent + "    ")
#         else:
#             print(indent + Fore.GREEN + "📄 " + item.name)


def main():
    if len(sys.argv) < 2:
        print("Помилка: потрібно передати шлях до директорії.")
        print("Приклад: python hw03.py C:\\Users\\Alex\\Desktop\\test")
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


if __name__ == "__main__":
    main()