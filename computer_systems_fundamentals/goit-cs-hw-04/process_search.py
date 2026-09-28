"""Keyword search using processes (multiprocessing).

Each process handles its own chunk of files. Within the process, files are read
asynchronously via asyncio + aiofiles. Results from each process are passed
to the main process via multiprocessing.Queue and merged there.
"""

import asyncio
import multiprocessing
import os
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
    """Function executed by a separate process.

    Runs asynchronous search on its chunk of files and puts local
    results into the queue for the main process.

    :param files: chunk of files for this process
    :param keywords: list of keywords
    :param queue: queue for passing results to the main process
    """
    local_results = asyncio.run(search_files_async(files, keywords))
    queue.put(local_results)


def search_with_processes(
    files: list[str], keywords: list[str], num_processes: int | None = None
) -> tuple[dict[str, list[str]], float]:
    """Main search function using processes.

    :param files: list of all files
    :param keywords: list of keywords
    :param num_processes: number of processes; if None — os.cpu_count()
    :return: tuple (results_dictionary, elapsed_time_in_seconds)
    """
    if num_processes is None:
        num_processes = os.cpu_count() or 1
    # No point creating more processes than there are files.
    if files:
        num_processes = min(num_processes, len(files))
    num_processes = max(num_processes, 1)

    final_results: dict[str, list[str]] = {kw: [] for kw in keywords}
    queue: "multiprocessing.Queue" = multiprocessing.Queue()

    # Split files into chunks by number of processes.
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

    # First, retrieve all results from the queue (one per process)
    # to avoid blocking, and only then call join().
    for _ in processes:
        local_results = queue.get()
        for kw, file_list in local_results.items():
            final_results.setdefault(kw, []).extend(file_list)

    for p in processes:
        p.join()

    elapsed = time.perf_counter() - start
    return final_results, elapsed
