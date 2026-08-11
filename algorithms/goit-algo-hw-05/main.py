import timeit
from pathlib import Path


def boyer_moore_search(text: str, pattern: str) -> int:
    """Пошук підрядка алгоритмом Боєра—Мура."""
    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length == 0:
        return 0
    if pattern_length > text_length:
        return -1

    bad_character_table = {
        char: index for index, char in enumerate(pattern)
        }

    shift = 0

    while shift <= text_length - pattern_length:
        index = pattern_length - 1

        while index >= 0 and pattern[index] == text[shift + index]:
            index -= 1

        if index < 0:
            return shift

        mismatched_char = text[shift + index]
        last_occurrence = bad_character_table.get(mismatched_char, -1)
        shift += max(1, index - last_occurrence)

    return -1


def build_lps(pattern: str) -> list[int]:
    """Створює таблицю найдовших префіксів для алгоритму КМП."""
    lps = [0] * len(pattern)
    length = 0
    index = 1

    while index < len(pattern):
        if pattern[index] == pattern[length]:
            length += 1
            lps[index] = length
            index += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[index] = 0
            index += 1

    return lps


def kmp_search(text: str, pattern: str) -> int:
    """Пошук підрядка алгоритмом Кнута—Морріса—Пратта."""
    if not pattern:
        return 0

    lps = build_lps(pattern)
    text_index = 0
    pattern_index = 0

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                return text_index - pattern_index

        elif pattern_index != 0:
            pattern_index = lps[pattern_index - 1]
        else:
            text_index += 1

    return -1


def rabin_karp_search(text: str, pattern: str) -> int:
    """Пошук підрядка алгоритмом Рабіна—Карпа."""
    pattern_length = len(pattern)
    text_length = len(text)
    base = 256
    prime = 101

    if pattern_length == 0:
        return 0
    if pattern_length > text_length:
        return -1

    pattern_hash = 0
    text_hash = 0
    highest_power = 1

    for _ in range(pattern_length - 1):
        highest_power = (highest_power * base) % prime

    for index in range(pattern_length):
        pattern_hash = (base * pattern_hash + ord(pattern[index])) % prime
        text_hash = (base * text_hash + ord(text[index])) % prime

    for index in range(text_length - pattern_length + 1):
        if pattern_hash == text_hash:
            if text[index:index + pattern_length] == pattern:
                return index

        if index < text_length - pattern_length:
            text_hash = (
                                base * (text_hash - ord(
                            text[index]) * highest_power)
                                + ord(text[index + pattern_length])
                        ) % prime

    return -1


def read_text(filename: str) -> str:
    """Читає текстові файли, збережені у кодуванні Windows-1251."""
    return Path(filename).read_text(encoding="cp1251")


def measure_time(search_function, text: str, pattern: str,
                 number: int = 1000) -> float:
    """
    Вимірює середній час одного запуску пошуку в мілісекундах.
    Використовується найкращий результат із кількох серій вимірювань.
    """
    timer = timeit.Timer(lambda: search_function(text, pattern))
    best_total_time = min(timer.repeat(repeat=5, number=number))

    return best_total_time / number * 1000


def print_results(article_name: str, results: dict) -> None:
    """Виводить результати вимірювань у вигляді таблиці."""
    print(f"\n{'=' * 70}")
    print(article_name)
    print(f"{'=' * 70}")
    print(f"{'Алгоритм':<25}{'Існуючий, мс':>20}{'Вигаданий, мс':>20}")
    print("-" * 70)

    for algorithm, times in results.items():
        print(
            f"{algorithm:<25}{times['existing']:>20.6f}{times['missing']:>20.6f}")

    fastest_existing = min(results, key=lambda name: results[name]["existing"])
    fastest_missing = min(results, key=lambda name: results[name]["missing"])

    print("Найшвидший для наявного підрядка:", fastest_existing)
    print("Найшвидший для вигаданого підрядка:", fastest_missing)


def main() -> None:
    text_1 = read_text("text1.txt")
    text_2 = read_text("text2.txt")

    # Підрядки, які наявні у відповідних статтях.
    existing_pattern_1 = "алгоритм сортування"
    existing_pattern_2 = "рекомендаційної системи"

    # Підрядки, яких гарантовано немає у статтях.
    missing_pattern_1 = "квантовий_пошук_відсутній_у_статті"
    missing_pattern_2 = "квантовий_пошук_відсутній_у_статті"

    algorithms = {
        "Боєра—Мура": boyer_moore_search,
        "Кнута—Морріса—Пратта": kmp_search,
        "Рабіна—Карпа": rabin_karp_search,
        }

    articles = {
        "article1": "Стаття 1: Використання алгоритмів у бібліотеках мов програмування",
        "article2": "Стаття 2: Методи та структури даних для рекомендаційної системи",
        }

    # Перевірка коректності обраних підрядків.
    assert existing_pattern_1 in text_1, "Підрядок для text1.txt не знайдено."
    assert existing_pattern_2 in text_2, "Підрядок для text2.txt не знайдено."
    assert missing_pattern_1 not in text_1, "Вигаданий підрядок є у text1.txt."
    assert missing_pattern_2 not in text_2, "Вигаданий підрядок є у text2.txt."

    results_1 = {
        name: {
            "existing": measure_time(function, text_1, existing_pattern_1),
            "missing": measure_time(function, text_1, missing_pattern_1),
            }
        for name, function in algorithms.items()
        }

    results_2 = {
        name: {
            "existing": measure_time(function, text_2, existing_pattern_2),
            "missing": measure_time(function, text_2, missing_pattern_2),
            }
        for name, function in algorithms.items()
        }

    print_results(
        articles["article1"],
        results_1)
    print_results(
        articles["article2"],
        results_2)

    combined_results = {
        name: results_1[name]["existing"]
              + results_1[name]["missing"]
              + results_2[name]["existing"]
              + results_2[name]["missing"]
        for name in algorithms
        }

    overall_fastest = min(combined_results, key=combined_results.get)

    print(f"\n{'=' * 70}")
    print("ЗАГАЛЬНИЙ ВИСНОВОК")
    print(f"{'=' * 70}")
    print("Найшвидший алгоритм за сумою чотирьох вимірювань:", overall_fastest)


if __name__ == "__main__":
    main()
