import os
from pathlib import Path

def read_file(path: str) -> list:
    """Function read file and check if it exists"""
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
    """function that clears screen"""
    os.system("cls" if os.name == "nt" else "clear")

def system_check():
    """function that checks whether system is available"""
    return "posix" if os.name == "posix" else "nt"

def is_directory_exists(path: str) -> bool:
    """function that checks whether directory exists"""

    return Path(path).exists()