"""Спільні утиліти проєкту: розподіл файлів, робота з конфігом,
збереження та красивий вивід результатів.
"""

import json
import os


def split_files(files: list[str], n: int) -> list[list[str]]:
    """Рівномірно розподіляє список файлів між n групами (порціями).

    Використовується, щоб розбити всі файли між потоками/процесами.

    :param files: список шляхів до файлів
    :param n: кількість груп (потоків або процесів)
    :return: список груп, кожна з яких — список файлів
    """
    if n <= 0:
        n = 1
    # Не створюємо більше груп, ніж є файлів.
    n = min(n, len(files)) if files else 1

    chunks: list[list[str]] = [[] for _ in range(n)]
    # "Розкидаємо" файли по колу (round-robin) для рівномірності.
    for idx, filepath in enumerate(files):
        chunks[idx % n].append(filepath)

    # Прибираємо порожні групи (якщо файлів менше за n).
    return [chunk for chunk in chunks if chunk]


def load_config(path: str) -> dict:
    """Читає JSON конфіг-файл і повертає словник з налаштуваннями.

    :param path: шлях до JSON-файлу
    :return: словник налаштувань
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_results(data: dict, path: str) -> None:
    """Зберігає результати у JSON-файл з відступами.

    :param data: дані для збереження
    :param path: шлях до вихідного файлу
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Результати збережено у файл: {path}")
    except OSError as exc:
        print(f"  [ERROR] Не вдалося зберегти результати у {path}: {exc}")


def print_results(results: dict[str, list[str]], title: str, elapsed: float) -> None:
    """Красиво виводить результати пошуку у консоль.

    :param results: словник {ключове_слово: [список файлів]}
    :param title: заголовок блоку (наприклад, назва режиму)
    :param elapsed: витрачений час у секундах
    """
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    if not results:
        print("  Жодного ключового слова не знайдено.")
    else:
        # Виводимо ключові слова відсортованими для стабільного вигляду.
        for keyword in sorted(results.keys()):
            files = results[keyword]
            print(f"  '{keyword}': знайдено у {len(files)} файлах")
            # Показуємо лише перші 3 файли, щоб не засмічувати консоль.
            for filepath in files[:3]:
                print(f"       - {os.path.basename(filepath)}")
            if len(files) > 3:
                print(f"       ... та ще {len(files) - 3} файл(ів)")
    print("-" * 60)
    print(f"  Витрачено часу: {elapsed:.4f} секунд")
    print("=" * 60)
