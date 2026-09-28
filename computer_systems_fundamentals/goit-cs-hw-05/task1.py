import argparse
import asyncio
import logging
from pathlib import Path

import aiofiles


CHUNK_SIZE = 1024 * 1024
MAX_CONCURRENT_COPIES = 20


async def get_directory_entries(folder: Path) -> list[Path]:
    """Asynchronously returns the entries in a folder."""
    try:
        return await asyncio.to_thread(lambda: list(folder.iterdir()))
    except OSError as error:
        logging.error("Could not read folder %s: %s", folder, error)
        return []


async def copy_file(
        source_file: Path,
        output_folder: Path,
        semaphore: asyncio.Semaphore,
        ) -> None:
    """Copies a file to a subfolder named after its extension."""
    extension = source_file.suffix.lower().lstrip(".") or "no_extension"
    destination_folder = output_folder / extension
    destination_file = destination_folder / source_file.name

    try:
        async with semaphore:
            await asyncio.to_thread(
                destination_folder.mkdir,
                parents=True,
                exist_ok=True,
                )

            async with aiofiles.open(source_file, "rb") as source:
                async with aiofiles.open(destination_file, "wb") as destination:
                    while chunk := await source.read(CHUNK_SIZE):
                        await destination.write(chunk)

            logging.info(
                "Copied file: %s -> %s",
                source_file,
                destination_file,
                )
    except OSError as error:
        logging.error("Could not copy file %s: %s", source_file, error)


async def read_folder(
        source_folder: Path,
        output_folder: Path,
        semaphore: asyncio.Semaphore,
        ) -> None:
    """Recursively reads a folder and starts asynchronous file copying."""
    copy_tasks = []

    for item in await get_directory_entries(source_folder):
        try:
            if item.is_dir():
                await read_folder(item, output_folder, semaphore)
            elif item.is_file():
                copy_tasks.append(copy_file(item, output_folder, semaphore))
        except OSError as error:
            logging.error("Could not process %s: %s", item, error)

    if copy_tasks:
        await asyncio.gather(*copy_tasks)


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Asynchronously sorts files by extension.",
        )
    parser.add_argument(
        "source",
        type=Path,
        help="Path to the source folder containing the files.",
        )
    parser.add_argument(
        "output",
        type=Path,
        help="Path to the destination folder.",
        )

    return parser.parse_args()


async def main() -> None:
    """Runs the main asynchronous program."""
    arguments = parse_arguments()
    source_folder = arguments.source.resolve()
    output_folder = arguments.output.resolve()

    if not source_folder.exists():
        logging.error("Source folder does not exist: %s", source_folder)
        return

    if not source_folder.is_dir():
        logging.error("The specified path is not a folder: %s", source_folder)
        return

    await asyncio.to_thread(
        output_folder.mkdir,
        parents=True,
        exist_ok=True,
        )

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_COPIES)

    logging.info("Starting to sort files from %s", source_folder)
    await read_folder(source_folder, output_folder, semaphore)
    logging.info("Sorting complete. Output folder: %s", output_folder)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        )

    asyncio.run(main())