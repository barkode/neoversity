# Паралельний пошук ключових слів у текстових файлах

Проєкт демонструє **паралельний пошук ключових слів** у великій кількості\
текстових файлів двома способами:

* **Потоки** (`threading`) — кожен поток обробляє свою порцію файлів;

* **Процеси** (`multiprocessing`) — кожен процес обробляє свою порцію файлів.

У **кожному** потоці/процесі файли читаються **асинхронно** через\
`asyncio` + `aiofiles` (усі файли порції читаються одночасно через\
`asyncio.gather`). Наприкінці результати обох режимів можна порівняти за часом.

---

## Структура проєкту

```
keyword_searcher/
├── generate_files.py   # генератор тестових .txt файлів
├── utils.py            # спільні утиліти (розподіл файлів, конфіг, збереження, вивід)
├── thread_search.py    # пошук через потоки (threading + asyncio + aiofiles)
├── process_search.py   # пошук через процеси (multiprocessing + asyncio + aiofiles)
├── main.py             # точка входу, CLI, порівняння режимів
├── config.json         # приклад конфіг-файлу
└── README.md           # ця інструкція
```

---

## Встановлення

Потрібен **Python 3.10+**. Встановіть залежність `aiofiles`:

```bash
pip install aiofiles
```

---

## Крок 1. Генерація тестових файлів

Скрипт `generate_files.py` створює тестові текстові файли, наповнені\
випадковими словами (серед яких гарантовано трапляються ключові слова).

```bash
python generate_files.py --count 30 --words 1000 --output-dir test_files
```

### Параметри `generate_files.py`

| Параметр | За замовчуванням | Опис |
| --- | --- | --- |
| `--count` | `20` | Кількість файлів для генерації |
| `--words` | `1000` | Кількість слів у кожному файлі |
| `--output-dir` | `test_files` | Директорія для збереження файлів |

---

## Крок 2. Запуск пошуку

### Варіант А - через аргументи командного рядка

```bash
python main.py --keywords python asyncio thread --mode both
```

Приклад з явним вказанням кількості потоків/процесів та директорії:

```bash
python main.py --files-dir test_files --keywords python asyncio queue \
    --threads 4 --processes 4 --mode both --output results.json
```

Лише потоки:

```bash
python main.py --keywords python asyncio --mode thread
```

Лише процеси:

```bash
python main.py --keywords python asyncio --mode process
```

### Варіант Б — через конфіг-файл

Створіть/відредагуйте `config.json`:

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

Запустіть:

```bash
python main.py --config config.json
```

> **Важливо:** значення з конфіг-файлу **перекривають** аргументи командного рядка.

---

## Параметри `main.py`

| Параметр | За замовчуванням | Опис |
| --- | --- | --- |
| `--config` | `None` | Шлях до JSON конфіг-файлу (перекриває CLI) |
| `--files-dir` | `test_files` | Директорія з текстовими файлами |
| `--keywords` | `None` | Список ключових слів (через пробіл), напр. `python asyncio` |
| `--threads` | `None` | Кількість потоків; якщо не задано — `os.cpu_count()` |
| `--processes` | `None` | Кількість процесів; якщо не задано — `os.cpu_count()` |
| `--output` | `results.json` | Файл для збереження результатів |
| `--mode` | `both` | Режим: `thread`, `process` або `both` |

---

## Формат результатів (`results.json`)

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

Для кожного режиму зберігається:

* `elapsed_sec` — витрачений час у секундах;

* `results` — словник `{ключове_слово: [список файлів, де воно знайдено]}`.

---

## Швидкий старт (усе разом)

```bash
`pip install aiofiles`
`python generate_files.py --count 30`
`python main.py --keywords python asyncio thread --mode both`
```

---

## Примітки щодо архітектури

* **Розподіл навантаження.** Файли рівномірно розкидаються між потоками/процесами\
  за принципом round-robin (`utils.split_files`).

* **Асинхронне читання.** Усередині кожного потоку/процесу виклик `asyncio.run(...)`\
  запускає одночасне читання всіх файлів порції через `aiofiles`.

* **Обмін даними.**

    * Потоки використовують спільний словник під захистом `threading.Lock`.

    * Процеси передають локальні результати головному процесу через `multiprocessing.Queue`.

* **Стійкість до помилок.** Помилки читання окремих файлів (`OSError`/`IOError`)\
  не зупиняють програму — виводиться попередження `[WARNING]`, робота триває.

* **Кросплатформність.** `multiprocessing.freeze_support()` викликається перед\
  `main()` для коректної роботи на Windows.