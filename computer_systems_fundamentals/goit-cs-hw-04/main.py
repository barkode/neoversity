"""Точка входу проєкту: паралельний пошук ключових слів у текстових файлах.

Підтримує два режими:
  * thread - пошук через потоки (threading);
  * process - пошук через процеси (multiprocessing);
  * both - обидва режими з порівнянням часу виконання.

Налаштування можна задати через аргументи командного рядка або через
JSON конфіг-файл (--config). Значення з конфіг-файлу перекривають CLI.
"""

import argparse
import glob
import multiprocessing
import os

from process_search import search_with_processes
from thread_search import search_with_threads
from utils import load_config, print_results, save_results


def parse_args() -> argparse.Namespace:
    """Парсить аргументи командного рядка."""
    parser = argparse.ArgumentParser(
        description="Паралельний пошук ключових слів у текстових файлах."
    )
    parser.add_argument(
        "--config", type=str, default=None,
        help="Шлях до JSON конфіг-файлу (перекриває аргументи CLI).",
    )
    parser.add_argument(
        "--files-dir", type=str, default="test_files",
        help="Директорія з текстовими файлами (за замовчуванням 'test_files').",
    )
    parser.add_argument(
        "--keywords", nargs="+", default=None,
        help="Список ключових слів для пошуку (через пробіл).",
    )
    parser.add_argument(
        "--threads", type=int, default=None,
        help="Кількість потоків (якщо не задано — os.cpu_count()).",
    )
    parser.add_argument(
        "--processes", type=int, default=None,
        help="Кількість процесів (якщо не задано — os.cpu_count()).",
    )
    parser.add_argument(
        "--output", type=str, default="results.json",
        help="Файл для збереження результатів (за замовчуванням 'results.json').",
    )
    parser.add_argument(
        "--mode", choices=["thread", "process", "both"], default="both",
        help="Режим пошуку: thread, process або both (за замовчуванням 'both').",
    )
    return parser.parse_args()


def apply_config(args: argparse.Namespace) -> argparse.Namespace:
    """Застосовує налаштування з конфіг-файлу поверх аргументів CLI.

    Значення з конфіг-файлу мають вищий пріоритет, ніж CLI.
    """
    if not args.config:
        return args

    try:
        config = load_config(args.config)
    except (OSError, ValueError) as exc:
        print(f"  [ERROR] Не вдалося прочитати конфіг '{args.config}': {exc}")
        return args

    # Перекриваємо значення, якщо вони присутні у конфізі.
    if "files_dir" in config:
        args.files_dir = config["files_dir"]
    if "keywords" in config:
        args.keywords = config["keywords"]
    if "threads" in config:
        args.threads = config["threads"]
    if "processes" in config:
        args.processes = config["processes"]
    if "output" in config:
        args.output = config["output"]
    if "mode" in config:
        args.mode = config["mode"]

    return args


def collect_files(files_dir: str) -> list[str]:
    """Збирає всі .txt файли з указаної директорії."""
    pattern = os.path.join(files_dir, "*.txt")
    return sorted(glob.glob(pattern))


def print_header(
    files: list[str],
    keywords: list[str],
    threads: int | None,
    processes: int | None,
    mode: str,
) -> None:
    """Виводить заголовок зі статистикою запуску."""
    cpu = os.cpu_count() or 1
    print()
    print("#" * 60)
    print("#" + " ПАРАЛЕЛЬНИЙ ПОШУК КЛЮЧОВИХ СЛІВ".center(58) + "#")
    print("#" * 60)
    print(f"  Файлів знайдено   : {len(files)}")
    print(f"  Ключові слова     : {', '.join(keywords)}")
    print(f"  Ядер CPU          : {cpu}")
    print(f"  Потоків           : {threads if threads is not None else f'авто ({cpu})'}")
    print(f"  Процесів          : {processes if processes is not None else f'авто ({cpu})'}")
    print(f"  Режим             : {mode}")
    print("#" * 60)


def main() -> None:
    """Головна логіка програми."""
    args = parse_args()
    args = apply_config(args)

    # Перевіряємо, що задані ключові слова.
    if not args.keywords:
        print("  [ERROR] Не задано жодного ключового слова. "
              "Використайте --keywords або конфіг-файл.")
        return

    files = collect_files(args.files_dir)
    if not files:
        print(f"  [ERROR] У директорії '{args.files_dir}' не знайдено .txt файлів. "
              "Спочатку згенеруйте їх через generate_files.py.")
        return

    print_header(files, args.keywords, args.threads, args.processes, args.mode)

    output_data: dict = {}

    thread_elapsed: float | None = None
    process_elapsed: float | None = None

    # --- Режим потоків ---
    if args.mode in ("thread", "both"):
        t_results, thread_elapsed = search_with_threads(
            files, args.keywords, args.threads
        )
        print_results(t_results, "РЕЗУЛЬТАТИ: ПОТОКИ (threading)", thread_elapsed)
        output_data["threading"] = {
            "elapsed_sec": thread_elapsed,
            "results": t_results,
        }

    # --- Режим процесів ---
    if args.mode in ("process", "both"):
        p_results, process_elapsed = search_with_processes(
            files, args.keywords, args.processes
        )
        print_results(p_results, "РЕЗУЛЬТАТИ: ПРОЦЕСИ (multiprocessing)", process_elapsed)
        output_data["multiprocessing"] = {
            "elapsed_sec": process_elapsed,
            "results": p_results,
        }

    # --- Порівняння часу, якщо обидва режими ---
    if args.mode == "both" and thread_elapsed is not None and process_elapsed is not None:
        print()
        print("=" * 60)
        print("  ПОРІВНЯННЯ ЧАСУ ВИКОНАННЯ")
        print("=" * 60)
        print(f"  Потоки (threading)      : {thread_elapsed:.4f} с")
        print(f"  Процеси (multiprocessing): {process_elapsed:.4f} с")
        if thread_elapsed < process_elapsed:
            diff = process_elapsed - thread_elapsed
            print(f"  Швидше: ПОТОКИ на {diff:.4f} с")
        elif process_elapsed < thread_elapsed:
            diff = thread_elapsed - process_elapsed
            print(f"  Швидше: ПРОЦЕСИ на {diff:.4f} с")
        else:
            print("  Час однаковий.")
        print("=" * 60)

    # --- Збереження результатів у JSON ---
    print()
    save_results(output_data, args.output)


if __name__ == "__main__":
    # Потрібно для коректної роботи multiprocessing на Windows / при заморожуванні.
    multiprocessing.freeze_support()
    main()
