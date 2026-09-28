"""Пошук ключових слів за допомогою процесів (multiprocessing).

Кожен процес обробляє свою порцію файлів. Усередині процесу файли читаються
асинхронно через asyncio + aiofiles. Результати кожного процесу передаються
головному процесу через multiprocessing.Queue і там об'єднуються.
"""

import asyncio
import multiprocessing
import os
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

    tasks = [search_in_file(filepath, keywords) for filepath in files]
    per_file_results = await asyncio.gather(*tasks)

    for filepath, found in zip(files, per_file_results):
        for kw, is_found in found.items():
            if is_found:
                results[kw].append(filepath)
    return results


def process_worker(
    files: list[str],
    keywords: list[str],
    queue: "multiprocessing.Queue",
) -> None:
    """Функція, яку виконує окремий процес.

    Запускає асинхронний пошук по своїй порції файлів і кладе локальні
    результати у чергу для головного процесу.

    :param files: порція файлів для цього процесу
    :param keywords: список ключових слів
    :param queue: черга для передачі результатів головному процесу
    """
    local_results = asyncio.run(search_files_async(files, keywords))
    queue.put(local_results)


def search_with_processes(
    files: list[str], keywords: list[str], num_processes: int | None = None
) -> tuple[dict[str, list[str]], float]:
    """Головна функція пошуку через процеси.

    :param files: список усіх файлів
    :param keywords: список ключових слів
    :param num_processes: кількість процесів; якщо None — os.cpu_count()
    :return: кортеж (словник_результатів, витрачений_час_у_секундах)
    """
    if num_processes is None:
        num_processes = os.cpu_count() or 1
    # Немає сенсу створювати більше процесів, ніж є файлів.
    if files:
        num_processes = min(num_processes, len(files))
    num_processes = max(num_processes, 1)

    final_results: dict[str, list[str]] = {kw: [] for kw in keywords}
    queue: "multiprocessing.Queue" = multiprocessing.Queue()

    # Розбиваємо файли на порції по кількості процесів.
    chunks = split_files(files, num_processes)

    start = time.perf_counter()

    processes: list[multiprocessing.Process] = []
    for chunk in chunks:
        p = multiprocessing.Process(
            target=process_worker,
            args=(chunk, keywords, queue),
        )
        p.start()
        processes.append(p)

    # Спершу забираємо всі результати з черги (по одному на процес),
    # щоб уникнути блокування, і лише потім робимо join().
    for _ in processes:
        local_results = queue.get()
        for kw, file_list in local_results.items():
            final_results.setdefault(kw, []).extend(file_list)

    for p in processes:
        p.join()

    elapsed = time.perf_counter() - start
    return final_results, elapsed
