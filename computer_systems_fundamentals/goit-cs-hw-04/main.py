"""Project entry point: parallel keyword search in text files.

Supports two modes:
  * thread  - search via threads (threading);
  * process - search via processes (multiprocessing);
  * both    - both modes with execution time comparison.

Settings can be specified via command-line arguments or via
a JSON configuration file (--config). Configuration file values override CLI.
"""

import argparse
import glob
import multiprocessing
import os

from process_search import search_with_processes
from thread_search import search_with_threads
from utils import load_config, print_results, save_results


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Parallel keyword search in text files."
    )
    parser.add_argument(
        "--config", type=str, default=None,
        help="Path to JSON configuration file (overrides CLI arguments).",
    )
    parser.add_argument(
        "--files-dir", type=str, default="test_files",
        help="Directory containing text files (default: 'test_files').",
    )
    parser.add_argument(
        "--keywords", nargs="+", default=None,
        help="List of keywords to search for (space-separated).",
    )
    parser.add_argument(
        "--threads", type=int, default=None,
        help="Number of threads (if not specified — os.cpu_count()).",
    )
    parser.add_argument(
        "--processes", type=int, default=None,
        help="Number of processes (if not specified — os.cpu_count()).",
    )
    parser.add_argument(
        "--output", type=str, default="results.json",
        help="File for saving results (default: 'results.json').",
    )
    parser.add_argument(
        "--mode", choices=["thread", "process", "both"], default="both",
        help="Search mode: thread, process or both (default: 'both').",
    )
    return parser.parse_args()


def apply_config(args: argparse.Namespace) -> argparse.Namespace:
    """Applies configuration file settings on top of CLI arguments.

    Configuration file values have higher priority than CLI.
    """
    if not args.config:
        return args

    try:
        config = load_config(args.config)
    except (OSError, ValueError) as exc:
        print(f"  [ERROR] Failed to read config '{args.config}': {exc}")
        return args

    # Override values if they are present in the config.
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
    """Collects all .txt files from the specified directory."""
    pattern = os.path.join(files_dir, "*.txt")
    return sorted(glob.glob(pattern))


def print_header(
    files: list[str],
    keywords: list[str],
    threads: int | None,
    processes: int | None,
    mode: str,
) -> None:
    """Prints header with execution statistics."""
    cpu = os.cpu_count() or 1
    print()
    print("#" * 60)
    print("#" + " PARALLEL KEYWORD SEARCH".center(58) + "#")
    print("#" * 60)
    print(f"  Files found       : {len(files)}")
    print(f"  Keywords          : {', '.join(keywords)}")
    print(f"  CPU cores         : {cpu}")
    print(f"  Threads           : {threads if threads is not None else f'auto ({cpu})'}")
    print(f"  Processes         : {processes if processes is not None else f'auto ({cpu})'}")
    print(f"  Mode              : {mode}")
    print("#" * 60)


def main() -> None:
    """Main programme logic."""
    args = parse_args()
    args = apply_config(args)

    # Check that keywords are specified.
    if not args.keywords:
        print("  [ERROR] No keywords specified. "
              "Use --keywords or a configuration file.")
        return

    files = collect_files(args.files_dir)
    if not files:
        print(f"  [ERROR] No .txt files found in directory '{args.files_dir}'. "
              "First generate them via generate_files.py.")
        return

    print_header(files, args.keywords, args.threads, args.processes, args.mode)

    output_data: dict = {}

    thread_elapsed: float | None = None
    process_elapsed: float | None = None

    # --- Thread mode ---
    if args.mode in ("thread", "both"):
        t_results, thread_elapsed = search_with_threads(
            files, args.keywords, args.threads
        )
        print_results(t_results, "RESULTS: THREADS (threading)", thread_elapsed)
        output_data["threading"] = {
            "elapsed_sec": thread_elapsed,
            "results": t_results,
        }

    # --- Process mode ---
    if args.mode in ("process", "both"):
        p_results, process_elapsed = search_with_processes(
            files, args.keywords, args.processes
        )
        print_results(p_results, "RESULTS: PROCESSES (multiprocessing)", process_elapsed)
        output_data["multiprocessing"] = {
            "elapsed_sec": process_elapsed,
            "results": p_results,
        }

    # --- Time comparison if both modes ---
    if args.mode == "both" and thread_elapsed is not None and process_elapsed is not None:
        print()
        print("=" * 60)
        print("  EXECUTION TIME COMPARISON")
        print("=" * 60)
        print(f"  Threads (threading)        : {thread_elapsed:.4f} s")
        print(f"  Processes (multiprocessing): {process_elapsed:.4f} s")
        if thread_elapsed < process_elapsed:
            diff = process_elapsed - thread_elapsed
            print(f"  Faster: THREADS by {diff:.4f} s")
        elif process_elapsed < thread_elapsed:
            diff = thread_elapsed - process_elapsed
            print(f"  Faster: PROCESSES by {diff:.4f} s")
        else:
            print("  Same time.")
        print("=" * 60)

    # --- Save results to JSON ---
    print()
    save_results(output_data, args.output)


if __name__ == "__main__":
    # Required for correct multiprocessing operation on Windows / when freezing.
    multiprocessing.freeze_support()
    main()
