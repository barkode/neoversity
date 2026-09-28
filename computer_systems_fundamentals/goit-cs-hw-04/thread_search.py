"""Пошук ключових слів за допомогою потоків (threading).

Кожен потік обробляє свою порцію файлів. Усередині потоку файли читаються
асинхронно через asyncio + aiofiles (asyncio.gather по всіх файлах порції).
Результати всіх потоків об'єднуються у спільний словник під захистом Lock.
"""

import asyncio
import os
import threading
import time

import aiofiles

from utils import split_files


async def search_in_file(filepath: str, keywords: list[str]) -> dict[str, bool]:
    """Асинхронно читає файл і перевіряє наявність кожного ключового слова.

    :param filepath: шлях до файлу
    :param keywords: список ключових слів
    :return: словник {ключове_слово: чи_знайдено}
    """
    found: dict[str, bool] = {kw: False for kw in keywords}
    try:
        async with aiofiles.open(filepath, "r", encoding="utf-8") as f:
            content = await f.read()
        content_lower = content.lower()
        for kw in keywords:
            if kw.lower() in content_lower:
                found[kw] = True
    except (OSError, IOError) as exc:
        # Проблемний файл не має ламати весь пошук.
        print(f"  [WARNING] Не вдалося прочитати {filepath}: {exc}")
    return found


async def search_files_async(
    files: list[str], keywords: list[str]
) -> dict[str, list[str]]:
    """Асинхронно шукає ключові слова у всіх файлах порції.

    :param files: список файлів для обробки
    :param keywords: список ключових слів
    :return: словник {ключове_слово: [файли, де знайдено]}
    """
    results: dict[str, list[str]] = {kw: [] for kw in keywords}

    # Запускаємо читання всіх файлів паралельно через asyncio.
    tasks = [search_in_file(filepath, keywords) for filepath in files]
    per_file_results = await asyncio.gather(*tasks)

    # Об'єднуємо результати по кожному файлу.
    for filepath, found in zip(files, per_file_results):
        for kw, is_found in found.items():
            if is_found:
                results[kw].append(filepath)
    return results


def thread_worker(
    files: list[str],
    keywords: list[str],
    shared_results: dict[str, list[str]],
    lock: threading.Lock,
) -> None:
    """Функція, яку виконує окремий потік.

    Запускає асинхронний пошук по своїй порції файлів, а потім під захистом
    Lock додає знайдене до спільного словника результатів.

    :param files: порція файлів для цього потоку
    :param keywords: список ключових слів
    :param shared_results: спільний словник результатів усіх потоків
    :param lock: замок для безпечного оновлення спільного словника
    """
    local_results = asyncio.run(search_files_async(files, keywords))

    # Безпечно зливаємо локальні результати у спільний словник.
    with lock:
        for kw, file_list in local_results.items():
            shared_results.setdefault(kw, []).extend(file_list)


def search_with_threads(
    files: list[str], keywords: list[str], num_threads: int | None = None
) -> tuple[dict[str, list[str]], float]:
    """Головна функція пошуку через потоки.

    :param files: список усіх файлів
    :param keywords: список ключових слів
    :param num_threads: кількість потоків; якщо None — os.cpu_count()
    :return: кортеж (словник_результатів, витрачений_час_у_секундах)
    """
    if num_threads is None:
        num_threads = os.cpu_count() or 1
    # Немає сенсу створювати більше потоків, ніж є файлів.
    if files:
        num_threads = min(num_threads, len(files))
    num_threads = max(num_threads, 1)

    shared_results: dict[str, list[str]] = {kw: [] for kw in keywords}
    lock = threading.Lock()

    # Розбиваємо файли на порції по кількості потоків.
    chunks = split_files(files, num_threads)

    start = time.perf_counter()

    threads: list[threading.Thread] = []
    for chunk in chunks:
        t = threading.Thread(
            target=thread_worker,
            args=(chunk, keywords, shared_results, lock),
        )
        t.start()
        threads.append(t)

    # Чекаємо завершення всіх потоків.
    for t in threads:
        t.join()

    elapsed = time.perf_counter() - start
    return shared_results, elapsed
