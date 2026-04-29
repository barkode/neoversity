import os
import pathlib
import sys
from colorama import Fore, Back, Style, init

COLORS = {
    }

init(autoreset=True)
def colorize_directory(path):
    """Function colorize directory"""
    pass


def clear_screen():
    """Function that clear console"""
    os.system("clear" if os.name == "posix" else "cls")
def main():
    if sys.argv != 2:
        print(f"Використання: {sys.argv[0]} <шлях>", file=sys.stderr)
        print(f"Отримано аргументів: {len(sys.argv) - 1}", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]

print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')

if __name__ == '__main__':
    clear_screen()
    main()