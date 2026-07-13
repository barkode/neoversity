import os


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def system_check():
    """Return the current operating system family."""
    return "posix" if os.name == "posix" else "nt"
