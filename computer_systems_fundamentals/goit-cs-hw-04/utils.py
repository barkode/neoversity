"""Shared project utilities: file distribution, configuration handling,
saving results and formatted output.
"""

import json
import os


def split_files(files: list[str], n: int) -> list[list[str]]:
    """Evenly distributes a list of files amongst n groups (chunks).

    Used to split all files amongst threads/processes.

    :param files: list of file paths
    :param n: number of groups (threads or processes)
    :return: list of groups, each being a list of files
    """
    if n <= 0:
        n = 1
    # Don't create more groups than there are files.
    n = min(n, len(files)) if files else 1

    chunks: list[list[str]] = [[] for _ in range(n)]
    # "Scatter" files in a round-robin manner for even distribution.
    for idx, filepath in enumerate(files):
        chunks[idx % n].append(filepath)

    # Remove empty groups (if there are fewer files than n).
    return [chunk for chunk in chunks if chunk]


def load_config(path: str) -> dict:
    """Reads a JSON configuration file and returns a dictionary of settings.

    :param path: path to the JSON file
    :return: dictionary of settings
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_results(data: dict, path: str) -> None:
    """Saves results to a JSON file with indentation.

    :param data: data to save
    :param path: path to the output file
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Results saved to file: {path}")
    except OSError as exc:
        print(f"  [ERROR] Failed to save results to {path}: {exc}")


def print_results(results: dict[str, list[str]], title: str, elapsed: float) -> None:
    """Neatly prints search results to the console.

    :param results: dictionary {keyword: [list of files]}
    :param title: block title (e.g., mode name)
    :param elapsed: elapsed time in seconds
    """
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    if not results:
        print("  No keywords found.")
    else:
        # Print keywords sorted for stable output.
        for keyword in sorted(results.keys()):
            files = results[keyword]
            print(f"  '{keyword}': found in {len(files)} file(s)")
            # Show only the first 3 files to avoid cluttering the console.
            for filepath in files[:3]:
                print(f"       - {os.path.basename(filepath)}")
            if len(files) > 3:
                print(f"       ... and {len(files) - 3} more")
    print("-" * 60)
    print(f"  Time elapsed: {elapsed:.4f} seconds")
    print("=" * 60)
