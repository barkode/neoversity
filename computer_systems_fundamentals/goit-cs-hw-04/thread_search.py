"""Keyword search using threads (threading).

Each thread processes its own chunk of files. Within the thread, files are read
asynchronously via asyncio + aiofiles (asyncio.gather across all files in the chunk).
Results from all threads are merged into a shared dictionary protected by Lock.
"""

import asyncio
import os
import threading
import time

import aiofiles

from utils import split_files


async def search_in_file(filepath: str, keywords: list[str]) -> dict[str, bool]:
    """Asynchronously reads a file and checks for the presence of each keyword.

    :param filepath: path to the file
    :param keywords: list of keywords
    :return: dictionary {keyword: found}
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
        # A problematic file shouldn't break the entire search.
        print(f"  [WARNING] Failed to read {filepath}: {exc}")
    return found


async def search_files_async(
    files: list[str], keywords: list[str]
) -> dict[str, list[str]]:
    """Asynchronously searches for keywords in all files in the chunk.

    :param files: list of files to process
    :param keywords: list of keywords
    :return: dictionary {keyword: [files where found]}
    """
    results: dict[str, list[str]] = {kw: [] for kw in keywords}

    # Launch reading of all files in parallel via asyncio.
    tasks = [search_in_file(filepath, keywords) for filepath in files]
    per_file_results = await asyncio.gather(*tasks)

    # Merge results for each file.
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
    """Function executed by a separate thread.

    Runs asynchronous search on its chunk of files, then under Lock protection
    adds the findings to the shared results dictionary.

    :param files: chunk of files for this thread
    :param keywords: list of keywords
    :param shared_results: shared results dictionary from all threads
    :param lock: lock for safe updating of the shared dictionary
    """
    local_results = asyncio.run(search_files_async(files, keywords))

    # Safely merge local results into the shared dictionary.
    with lock:
        for kw, file_list in local_results.items():
            shared_results.setdefault(kw, []).extend(file_list)


def search_with_threads(
    files: list[str], keywords: list[str], num_threads: int | None = None
) -> tuple[dict[str, list[str]], float]:
    """Main search function using threads.

    :param files: list of all files
    :param keywords: list of keywords
    :param num_threads: number of threads; if None — os.cpu_count()
    :return: tuple (results_dictionary, elapsed_time_in_seconds)
    """
    if num_threads is None:
        num_threads = os.cpu_count() or 1
    # No point creating more threads than there are files.
    if files:
        num_threads = min(num_threads, len(files))
    num_threads = max(num_threads, 1)

    shared_results: dict[str, list[str]] = {kw: [] for kw in keywords}
    lock = threading.Lock()

    # Split files into chunks by number of threads.
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

    # Wait for all threads to complete.
    for t in threads:
        t.join()

    elapsed = time.perf_counter() - start
    return shared_results, elapsed
