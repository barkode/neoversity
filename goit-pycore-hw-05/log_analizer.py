import sys

from pathlib import Path

default_file_path = "log.log"


def parse_log_line(line: str) -> dict:
    """Function parse log line and return dict with data"""
    parts = line.strip().split(' ', 3)
    if len(parts) < 4:
        raise ValueError(f"Invalid log line: {line.strip()}")
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3],
        }


def load_logs(file_path: str) -> list:
    """Function load logs from file"""
    try:
        lines = []
        with open(file_path, encoding="utf-8") as f:
            lines = [line for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    except IOError as err:
        print(f"File error: {err}")
        sys.exit(1)

    logs = []

    for line in lines:
        try:
            logs.append(parse_log_line(line))
        except ValueError as err:
            print(f"Invalid log line: {err}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """Function filter logs by level"""
    return list(
        filter(lambda log: log["level"].upper() == level.upper(), logs))


def count_logs_by_level(logs: list) -> dict:
    """Count logs by level"""
    counts = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def display_log_counts(counts: dict):
    """Format and display log counts"""
    print(f"\n{'Logging level':<17}| {'Quantity'}")
    print(f"{'-' * 17}|{'-' * 10}")
    for level, count in counts.items():
        print(f"{level:<17}| {count}")


def main():
    """ Main function"""
    if len(sys.argv) < 2:
        print(
            "Using: python main.py <path_to_file> [logging_level]")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    filter_level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if filter_level:
        filtered = filter_logs_by_level(logs, filter_level)
        print(f"\nLog details for the level '{filter_level}':")
        if filtered:
            for log in filtered:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print(f"Entries with level '{filter_level}' not found.")


if __name__ == "__main__":
    main()
