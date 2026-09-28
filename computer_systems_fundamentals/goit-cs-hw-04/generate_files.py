"""Генератор тестових текстових файлів для демонстрації пошуку ключових слів.

Скрипт створює задану кількість .txt файлів, наповнених випадковими словами.
Серед випадкових слів гарантовано зустрічаються "ключові" слова.

Приклад запуску:
    python generate_files.py --count 30 --words 1000 --output-dir test_files
"""

import argparse
import os
import random

# Ключові слова, які ми хочемо мати у файлах, щоб пошук їх знаходив.
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

# Додатковий набір "шумових" слів для наповнення файлів.
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
    """Формує загальний словник слів (ключові + шумові).

    Ключові слова додаються кілька разів, щоб підвищити ймовірність їх
    появи у згенерованих файлах.
    """
    vocabulary: list[str] = []
    # Додаємо ключові слова з підвищеною вагою.
    vocabulary.extend(KEYWORDS * 3)
    vocabulary.extend(FILLER_WORDS)
    return vocabulary


def generate_file(filepath: str, words_count: int, vocabulary: list[str]) -> None:
    """Генерує один текстовий файл із випадкових слів.

    :param filepath: шлях до файлу, який треба створити
    :param words_count: скільки слів записати у файл
    :param vocabulary: словник, з якого обираються випадкові слова
    """
    # Обираємо випадкові слова зі словника.
    words = [random.choice(vocabulary) for _ in range(words_count)]

    # Розбиваємо слова на "рядки" по 12 слів для читабельності.
    lines: list[str] = []
    for i in range(0, len(words), 12):
        lines.append(" ".join(words[i:i + 12]))

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    """Точка входу: парсить аргументи та генерує файли."""
    parser = argparse.ArgumentParser(
        description="Генератор тестових текстових файлів для пошуку ключових слів."
    )
    parser.add_argument(
        "--count", type=int, default=20,
        help="Кількість файлів для генерації (за замовчуванням 20).",
    )
    parser.add_argument(
        "--words", type=int, default=1000,
        help="Кількість слів у кожному файлі (за замовчуванням 1000).",
    )
    parser.add_argument(
        "--output-dir", type=str, default="test_files",
        help="Директорія для збереження файлів (за замовчуванням 'test_files').",
    )
    args = parser.parse_args()

    # Створюємо директорію для вихідних файлів, якщо її ще немає.
    os.makedirs(args.output_dir, exist_ok=True)

    vocabulary = build_vocabulary()

    print("=" * 60)
    print("  ГЕНЕРАЦІЯ ТЕСТОВИХ ФАЙЛІВ")
    print("=" * 60)
    print(f"  Кількість файлів : {args.count}")
    print(f"  Слів у файлі     : {args.words}")
    print(f"  Директорія       : {args.output_dir}")
    print("-" * 60)

    for i in range(1, args.count + 1):
        filename = f"file_{i:04d}.txt"
        filepath = os.path.join(args.output_dir, filename)
        try:
            generate_file(filepath, args.words, vocabulary)
            print(f"  [{i}/{args.count}] Створено: {filename}")
        except OSError as exc:
            # Не падаємо через один проблемний файл — просто попереджаємо.
            print(f"  [WARNING] Не вдалося створити {filename}: {exc}")

    print("-" * 60)
    print(f"  Готово! Згенеровано файлів у '{args.output_dir}'.")
    print("=" * 60)


if __name__ == "__main__":
    main()
