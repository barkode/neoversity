# Parallel Keyword Search in Text Files

This project demonstrates **parallel keyword searching** across large numbers of\
text files using two approaches:

* **Threads** (`threading`) — each thread processes its own chunk of files;

* **Processes** (`multiprocessing`) — each process processes its own chunk of files.

Within **each** thread/process, files are read **asynchronously** using\
`asyncio` + `aiofiles` (all files in the chunk are read concurrently via\
`asyncio.gather`). At the end, results from both modes can be compared by execution time.

---

## Project Structure

```
keyword_searcher/
├── generate_files.py   # generator for test .txt files
├── utils.py            # shared utilities (file distribution, config, saving, output)
├── thread_search.py    # search via threads (threading + asyncio + aiofiles)
├── process_search.py   # search via processes (multiprocessing + asyncio + aiofiles)
├── main.py             # entry point, CLI, mode comparison
├── config.json         # example configuration file
└── README.md           # this documentation
```

---

## Installation

Requires **Python 3.10+**. Install the `aiofiles` dependency:

```bash
pip install aiofiles
```

---

## Step 1. Generating Test Files

The `generate_files.py` script creates test text files populated with\
random words (which are guaranteed to include the target keywords).

```bash
python generate_files.py --count 30 --words 1000 --output-dir test_files
```

### Parameters for `generate_files.py`

| Parameter | Default | Description |
| --- | --- | --- |
| `--count` | `20` | Number of files to generate |
| `--words` | `1000` | Number of words in each file |
| `--output-dir` | `test_files` | Directory for saving files |

---

## Step 2. Running the Search

### Option A — via command-line arguments

```bash
python main.py --keywords python asyncio thread --mode both
```

Example with explicit thread/process counts and directory:

```bash
python main.py --files-dir test_files --keywords python asyncio queue \
    --threads 4 --processes 4 --mode both --output results.json
```

Threads only:

```bash
python main.py --keywords python asyncio --mode thread
```

Processes only:

```bash
python main.py --keywords python asyncio --mode process
```

### Option B — via configuration file

Create/edit `config.json`:

```json
{
  "files_dir": "test_files",
  "keywords": ["python", "asyncio", "thread", "process"],
  "threads": 4,
  "processes": 4,
  "output": "results.json",
  "mode": "both"
}
```

Run:

```bash
python main.py --config config.json
```

> **Important:** values from the configuration file **override** command-line arguments.

---

## Parameters for `main.py`

| Parameter | Default | Description |
| --- | --- | --- |
| `--config` | `None` | Path to JSON configuration file (overrides CLI) |
| `--files-dir` | `test_files` | Directory containing text files |
| `--keywords` | `None` | List of keywords (space-separated), e.g. `python asyncio` |
| `--threads` | `None` | Number of threads; if not specified — `os.cpu_count()` |
| `--processes` | `None` | Number of processes; if not specified — `os.cpu_count()` |
| `--output` | `results.json` | File for saving results |
| `--mode` | `both` | Mode: `thread`, `process` or `both` |

---

## Results Format (`results.json`)

```json
{
  "threading": {
    "elapsed_sec": 0.0123,
    "results": {
      "python": ["test_files/file_0001.txt", "test_files/file_0002.txt"],
      "asyncio": ["test_files/file_0001.txt"]
    }
  },
  "multiprocessing": {
    "elapsed_sec": 0.0456,
    "results": {
      "python": ["test_files/file_0001.txt", "test_files/file_0002.txt"],
      "asyncio": ["test_files/file_0001.txt"]
    }
  }
}
```

For each mode, the following is stored:

* `elapsed_sec` — elapsed time in seconds;

* `results` — dictionary `{keyword: [list of files where it was found]}`.

---

## Quick Start (all together)

```bash
pip install aiofiles
python generate_files.py --count 30
python main.py --keywords python asyncio thread --mode both
```

---

## Architecture Notes

* **Load distribution.** Files are evenly distributed amongst threads/processes\
  using a round-robin approach (`utils.split_files`).

* **Asynchronous reading.** Within each thread/process, the call to `asyncio.run(...)`\
  launches concurrent reading of all files in the chunk via `aiofiles`.

* **Data exchange.**

  * Threads use a shared dictionary protected by `threading.Lock`.

  * Processes pass local results to the main process via `multiprocessing.Queue`.

* **Fault tolerance.** Read errors for individual files (`OSError`/`IOError`)\
  do not halt the programme — a warning `[WARNING]` is displayed, execution continues.

* **Cross-platform support.** `multiprocessing.freeze_support()` is called before\
  `main()` for correct operation on Windows.