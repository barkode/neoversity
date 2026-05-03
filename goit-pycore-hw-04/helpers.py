from colorama import Fore, Style

def read_file(path: str) -> list:
    """Function read file and check if it exists"""
    try:
        lines = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    line = tuple(line.split(","))
                    lines.append(line)

                except (ValueError, IndexError):
                    print(f"Error in line {line}")
                    continue
        return lines

    except FileNotFoundError:
        print(f"File {path} not found")
        return []


EXIT_COMMANDS = ['exit', 'close', 'good bye', 'bye']

HELP_COMMANDS_DICTIONARY = {
    'exit': 'Exit',
    'close': 'Close',
    }

DEFAULT_PATH = './'

COLOUR_SCHEMA = {
    ".py": Fore.CYAN + Style.BRIGHT,
    ".exe": Fore.RED + Style.BRIGHT,
    ".txt": Fore.WHITE + Style.BRIGHT,
    ".md": Fore.GREEN + Style.BRIGHT,
    ".pdf": Fore.YELLOW + Style.BRIGHT,
    ".jpg": Fore.MAGENTA + Style.BRIGHT,
    ".png": Fore.MAGENTA + Style.BRIGHT,
    ".zip": Fore.RED + Style.BRIGHT,
    "directory": Fore.BLUE + Style.BRIGHT,
    "default": Fore.WHITE + Style.DIM,
    "error": Fore.RED,
    "warning": Fore.YELLOW,
    "reset": Fore.RESET,
    "icon_directory": "📁 ",
    "icon_file": "📄 "
    }
