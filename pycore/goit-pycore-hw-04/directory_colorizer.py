import sys
from pathlib import Path
from colorama import Fore, Style, init
from helpers import clear_screen
from constants import COLOUR_SCHEMA, DEFAULT_PATH


def print_directory_tree(path, indent=""):
    try:
        items = path.iterdir()
    except PermissionError:
        print(indent + COLOUR_SCHEMA.get("error", "") + "[Permission denied]")
        return

    for item in items:
        if item.is_dir():
            colour = COLOUR_SCHEMA.get("directory", "")
            icon = COLOUR_SCHEMA.get("icon_directory", "")
            print(indent + colour + icon + item.name)
            print_directory_tree(item, indent + "    ")
        else:
            ext = item.suffix.lower()
            colour = COLOUR_SCHEMA.get(ext, COLOUR_SCHEMA["default"])
            icon_file = COLOUR_SCHEMA.get("icon_file", "")
            print(indent + colour + icon_file + item.name)


def main(path=None) -> None:
    init(autoreset=True)
    clear_screen()

    err = COLOUR_SCHEMA.get("error")
    warn = COLOUR_SCHEMA.get("warning")
    reset = COLOUR_SCHEMA.get("reset")

    if path is not None:
        directory_path = Path(path)
    elif len(sys.argv) == 2:
        directory_path = Path(sys.argv[1])
    elif len(sys.argv) > 2:
        print(f"{err}ERROR:{reset} enter the path to the directory..")
        print(
            f"{warn}Example:{reset} python3 {sys.argv[0]} <path to the directory>")
        return
    else:
        print(f"{warn}No path provided. Using default: {DEFAULT_PATH}{reset}")
        directory_path = Path(DEFAULT_PATH)

    if not directory_path.exists():
        print(f"{err}ERROR:{reset} the path doesn't exist")
        return

    if not directory_path.is_dir():
        print(f"{err}ERROR:{reset} The path is not a directory.")
        return

    print(Fore.YELLOW + f"Directory structure: {directory_path}")
    print_directory_tree(directory_path)


if __name__ == "__main__":
    main()
