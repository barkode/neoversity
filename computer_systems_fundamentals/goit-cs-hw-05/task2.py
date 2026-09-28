import argparse
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt


class TextExtractor(HTMLParser):
    """Extracts text content from an HTML document."""

    def __init__(self) -> None:
        super().__init__()
        self.text_parts = []

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)

    def get_text(self) -> str:
        """Returns the combined text extracted from the page."""
        return " ".join(self.text_parts)


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyses word frequency using MapReduce.",
        )
    parser.add_argument(
        "url",
        help="URL of the web page or text document.",
        )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of most frequent words to display in the chart.",
        )

    return parser.parse_args()


def fetch_text(url: str) -> str:
    """Downloads content from a URL and returns its text."""
    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        )

    with urlopen(request, timeout=15) as response:
        content = response.read().decode("utf-8", errors="ignore")

    parser = TextExtractor()
    parser.feed(content)

    return parser.get_text()


def normalize_text(text: str) -> list[str]:
    """Converts text into a list of lower-case words."""
    return re.findall(r"[^\W\d_]+", text.lower(), flags=re.UNICODE)


def split_into_chunks(words: list[str], chunk_size: int) -> list[list[str]]:
    """Splits words into chunks of roughly equal size."""
    return [
        words[index:index + chunk_size]
        for index in range(0, len(words), chunk_size)
        ]


def map_words(words_chunk: list[str]) -> Counter:
    """Map phase: counts the words in one text chunk."""
    return Counter(words_chunk)


def reduce_words(counters: list[Counter]) -> Counter:
    """Reduce phase: combines the individual word counts."""
    total_counter = Counter()

    for counter in counters:
        total_counter.update(counter)

    return total_counter


def map_reduce_word_count(
        text: str,
        workers: int = 4,
        ) -> Counter:
    """Counts word frequencies using the MapReduce model."""
    words = normalize_text(text)

    if not words:
        return Counter()

    chunk_size = max(1, len(words) // workers)
    chunks = split_into_chunks(words, chunk_size)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        mapped_results = list(executor.map(map_words, chunks))

    return reduce_words(mapped_results)


def visualize_top_words(word_frequencies: Counter, top_count: int) -> None:
    """Plots a bar chart of the most frequently used words."""
    top_words = word_frequencies.most_common(top_count)

    if not top_words:
        print("No words were found to visualise.")
        return

    words, frequencies = zip(*top_words)

    plt.figure(figsize=(12, 6))
    plt.bar(words, frequencies, color="steelblue")

    plt.title(f"Top {top_count} most frequently used words")
    plt.xlabel("Words")
    plt.ylabel("Number of occurrences")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def main() -> None:
    """Downloads the text, runs MapReduce and plots the results."""
    arguments = parse_arguments()

    try:
        text = fetch_text(arguments.url)
    except OSError as error:
        print(f"Could not download the text: {error}")
        return

    word_frequencies = map_reduce_word_count(text)

    print(f"Unique words found: {len(word_frequencies)}")
    print(f"Top {arguments.top} words:")

    for word, frequency in word_frequencies.most_common(arguments.top):
        print(f"{word}: {frequency}")

    visualize_top_words(word_frequencies, arguments.top)


if __name__ == "__main__":
    main()