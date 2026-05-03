import sys
import os
from pathlib import Path
from colorama import Fore, Style, init
from helpers import clear_screen
from constants import COLOUR_SCHEMA


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


def main():
    init(autoreset=True)

    clear_screen()

    if len(sys.argv) != 2:
        err = COLOUR_SCHEMA.get("error")
        warn = COLOUR_SCHEMA.get("warning")
        reset = COLOUR_SCHEMA.get("reset")
        print(f"{err}ERROR:{reset} enter the path to the directory..")
        print(
            f"{warn}Example:{reset} python3 {sys.argv[0]} <path to the directory>")
        return

    directory_path = Path(sys.argv[1])

    if not directory_path.exists():
        err = COLOUR_SCHEMA.get("error")
        reset = COLOUR_SCHEMA.get("reset")
        print(f"{err}ERROR:{reset} the path doesn't exist")
        return

    if not directory_path.is_dir():
        err = COLOUR_SCHEMA.get("error")
        reset = COLOUR_SCHEMA.get("reset")
        print(f"{err}ERROR:{reset} The path is not a directory.")
        return

    print(Fore.YELLOW + f"Directory structure: {directory_path}")
    print_directory_tree(directory_path)
    print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
