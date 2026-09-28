# Concurrency and MapReduce Utilities

This repository contains two Python utility scripts demonstrating asynchronous I/O and multithreaded MapReduce
processing.

## Prerequisites

Install Python 3.10 or newer, then install the required dependencies:

```bash
pip install aiofiles matplotlib
```

## Project Structure

- `task1.py` — Asynchronous file sorter that organizes files by extension.
- `task2.py` — Multithreaded MapReduce word-frequency analyser and visualizer.
- `README.md` — Project documentation and usage guide.

## Task 1: Asynchronous File Sorter

The `task1.py` script recursively reads files in a source directory and copies them into subfolders in the destination
directory, organized by file extension.

### Features

- Asynchronous directory traversal and file copying using `asyncio` and `aiofiles`.
- Limits concurrent copy operations with an `asyncio.Semaphore`.
- Stores files without extensions in the `no_extension/` folder.
- Logs operations and errors.
- Accepts paths through command-line arguments.

### Usage

```bash
python task1_sort_files.py <source_directory> <destination_directory>
```

Example:

```bash
python task1_sort_files.py ./downloads ./sorted_storage
```

Files with a `.jpg` extension are copied to `./sorted_storage/jpg/`, `.pdf` files to `./sorted_storage/pdf/`, and files
without extensions to `./sorted_storage/no_extension/`.

## Task 2: Multithreaded MapReduce Word Analyser

The `task2.py` script fetches content from a URL, counts word frequencies using a multithreaded
MapReduce approach, and plots the most frequent words.

### Features

- Extracts text from web pages using Python's standard-library HTML parser.
- Normalizes words to lower case and supports Unicode letters.
- Map phase: counts words in chunks using `concurrent.futures.ThreadPoolExecutor`.
- Reduce phase: combines the partial word counts.
- Displays a bar chart using `matplotlib`.

### Usage

```bash
python task2_mapreduce_words.py <url> [--top N]
```

Arguments:

- `url` — URL of the page or text document to analyse.
- `--top N` — Number of most frequent words to show; defaults to 10.

Example:

```bash
python task2_mapreduce_words.py "https://www.gutenberg.org/files/1342/1342-0.txt" --top 15
```

The script prints the word-frequency results and opens a window displaying the chart.
