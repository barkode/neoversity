from log_color import Fore


def log_info(message) -> None:
    print(f"{Fore.BLUE} [INFO] {Fore.RESET} {message}")


def log_warning(message) -> None:
    print(f"{Fore.YELLOW} [WARNING] {Fore.RESET} {message}")


def log_error(message) -> None:
    print(f"{Fore.RED} [ERROR] {Fore.RESET} {message}")
