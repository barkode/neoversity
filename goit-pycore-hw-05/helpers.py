import os
from pathlib import Path


def read_file(path: str) -> list:
    """Read a text file and return normalized records."""
    try:
        lines = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                line = tuple(line.split(","))
                lines.append(line)
        return lines

    except FileNotFoundError:
        print(f"File {path} not found")
        return []


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def system_check():
    """Return the current operating system family."""
    return "posix" if os.name == "posix" else "nt"


def is_directory_exists(path: str) -> bool:
    """Check whether the provided path exists and is a directory."""
    return Path(path).exists() and Path(path).is_dir()
