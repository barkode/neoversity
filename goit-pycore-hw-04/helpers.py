import os


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


def clear_screen():
    """function that clears screen"""
    os.system("cls" if os.name == "nt" else "clear")
