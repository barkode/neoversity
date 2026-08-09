import argparse
import shutil
from pathlib import Path


def copy_and_sort_files(source_dir: Path, destination_dir: Path) -> None:
    """
    Рекурсивно обходить source_dir, копіює файли в destination_dir
    та сортує їх за розширенням.
    """
    try:
        for item in source_dir.iterdir():
            # Не обробляємо директорію призначення, якщо вона розміщена всередині source_dir
            if item.resolve() == destination_dir.resolve():
                continue

            if item.is_dir():
                copy_and_sort_files(item, destination_dir)

            elif item.is_file():
                extension = item.suffix[1:].lower() or "no_extension"
                target_dir = destination_dir / extension
                target_dir.mkdir(parents=True, exist_ok=True)

                target_file = target_dir / item.name

                # Уникаємо перезапису файлу з однаковою назвою
                counter = 1
                while target_file.exists():
                    target_file = target_dir / f"{item.stem}_{counter}{item.suffix}"
                    counter += 1

                shutil.copy2(item, target_file)
                print(f"Скопійовано: {item} -> {target_file}")

    except PermissionError:
        print(f"Помилка доступу до директорії: {source_dir}")
    except OSError as error:
        print(f"Помилка під час обробки {source_dir}: {error}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Рекурсивне копіювання та сортування файлів за розширенням."
        )
    parser.add_argument(
        "source",
        type=Path,
        help="Шлях до вихідної директорії.",
        )
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        default=Path("dist"),
        help="Шлях до директорії призначення. За замовчуванням: dist.",
        )

    args = parser.parse_args()

    source_dir = args.source.resolve()
    destination_dir = args.destination.resolve()

    if not source_dir.exists():
        print(f"Помилка: директорія не існує: {source_dir}")
        return

    if not source_dir.is_dir():
        print(f"Помилка: {source_dir} не є директорією.")
        return

    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
        copy_and_sort_files(source_dir, destination_dir)
        print("\nСортування файлів завершено.")
    except PermissionError:
        print(f"Немає прав для створення директорії: {destination_dir}")
    except OSError as error:
        print(f"Сталася помилка: {error}")


if __name__ == "__main__":
    main()