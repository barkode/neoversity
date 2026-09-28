"""Test text file generator for demonstrating keyword search.

This script creates a specified number of .txt files populated with random words.
Target keywords are guaranteed to appear amongst the random words, ensuring the
search has something to find.

Example usage:
    python generate_files.py --count 30 --words 1000 --output-dir test_files
"""

import argparse
import os
import random

# Target keywords we want to include in files so the search can find them.
KEYWORDS: list[str] = [
    "python",
    "asyncio",
    "thread",
    "process",
    "queue",
    "file",
    "search",
    "keyword",
    "parallel",
    "concurrent",
]

# Additional "filler" words to populate the files.
FILLER_WORDS: list[str] = [
    "data", "code", "system", "network", "server", "client", "memory",
    "disk", "cache", "buffer", "token", "module", "package", "function",
    "variable", "loop", "array", "object", "class", "method", "value",
    "index", "string", "number", "boolean", "list", "dict", "set",
    "tuple", "lambda", "generator", "iterator", "decorator", "context",
    "socket", "protocol", "request", "response", "session", "cookie",
    "header", "payload", "stream", "chunk", "batch", "worker", "task",
    "event", "signal", "timer", "clock", "random", "sample", "vector",
]


def build_vocabulary() -> list[str]:
    """Builds the complete word vocabulary (keywords + filler words).

    Keywords are added multiple times to increase the probability of their
    appearance in generated files.
    """
    vocabulary: list[str] = []
    # Add keywords with increased weight.
    vocabulary.extend(KEYWORDS * 3)
    vocabulary.extend(FILLER_WORDS)
    return vocabulary


def generate_file(filepath: str, words_count: int, vocabulary: list[str]) -> None:
    """Generates a single text file from random words.

    :param filepath: path to the file to create
    :param words_count: number of words to write to the file
    :param vocabulary: vocabulary from which random words are chosen
    """
    # Choose random words from the vocabulary.
    words = [random.choice(vocabulary) for _ in range(words_count)]

    # Split words into "lines" of 12 words for readability.
    lines: list[str] = []
    for i in range(0, len(words), 12):
        lines.append(" ".join(words[i:i + 12]))

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    """Entry point: parses arguments and generates files."""
    parser = argparse.ArgumentParser(
        description="Test text file generator for keyword search."
    )
    parser.add_argument(
        "--count", type=int, default=20,
        help="Number of files to generate (default: 20).",
    )
    parser.add_argument(
        "--words", type=int, default=1000,
        help="Number of words in each file (default: 1000).",
    )
    parser.add_argument(
        "--output-dir", type=str, default="test_files",
        help="Directory for saving files (default: 'test_files').",
    )
    args = parser.parse_args()

    # Create the output directory if it doesn't exist yet.
    os.makedirs(args.output_dir, exist_ok=True)

    vocabulary = build_vocabulary()

    print("=" * 60)
    print("  TEST FILE GENERATION")
    print("=" * 60)
    print(f"  Number of files  : {args.count}")
    print(f"  Words per file   : {args.words}")
    print(f"  Directory        : {args.output_dir}")
    print("-" * 60)

    for i in range(1, args.count + 1):
        filename = f"file_{i:04d}.txt"
        filepath = os.path.join(args.output_dir, filename)
        try:
            generate_file(filepath, args.words, vocabulary)
            print(f"  [{i}/{args.count}] Created: {filename}")
        except OSError as exc:
            # Don't crash due to one problematic file — just warn.
            print(f"  [WARNING] Failed to create {filename}: {exc}")

    print("-" * 60)
    print(f"  Done! Generated files in '{args.output_dir}'.")
    print("=" * 60)


if __name__ == "__main__":
    main()
