from colorama import Fore, Style

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

EXIT_PHRASES = ['exit', 'close', 'bye', 'quit', 'q']

HELP_COMMANDS_DICTIONARY = {
    'exit': 'Exit',
    'close': 'Close',
    }

DEFAULT_PATH = '.'
DEFAULT_SALARIES_PATH = "salaries.txt"
DEFAULT_CATS_INFO_PATH = "cats_info.txt"
