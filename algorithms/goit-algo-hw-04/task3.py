import random
import statistics
import timeit
from typing import Callable


def insertion_sort(data: list[int]) -> list[int]:
    """Сортування вставками."""
    result = data.copy()

    for index in range(1, len(result)):
        current_value = result[index]
        position = index - 1

        while position >= 0 and result[position] > current_value:
            result[position + 1] = result[position]
            position -= 1

        result[position + 1] = current_value

    return result


def merge(left: list[int], right: list[int]) -> list[int]:
    """Об'єднує два відсортовані списки."""
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])

    return merged


def merge_sort(data: list[int]) -> list[int]:
    """Рекурсивне сортування злиттям."""
    if len(data) <= 1:
        return data

    middle = len(data) // 2
    left_half = merge_sort(data[:middle])
    right_half = merge_sort(data[middle:])

    return merge(left_half, right_half)


def timsort(data: list[int]) -> list[int]:
    """Вбудоване сортування Python — Timsort."""
    return sorted(data)


def measure_time(
        algorithm: Callable[[list[int]], list[int]],
        data: list[int],
        repeats: int = 5,
        ) -> float:
    """Повертає середній час виконання алгоритму."""
    timer = timeit.Timer(lambda: algorithm(data))
    measurements = timer.repeat(repeat=repeats, number=1)

    return statistics.mean(measurements)


def test_algorithm(
        algorithm: Callable[[list[int]], list[int]],
        data: list[int],
        ) -> None:
    """Перевіряє правильність сортування перед вимірюванням часу."""
    if algorithm(data) != sorted(data):
        raise ValueError(f"Алгоритм {algorithm.__name__} працює некоректно.")


def print_result(
        data_name: str,
        size: int,
        merge_time: float,
        insertion_time: float,
        timsort_time: float,
        ) -> None:
    """Виводить результати в табличному вигляді."""
    print(
        f"{data_name:<20}"
        f"{size:<10}"
        f"{merge_time:<18.6f}"
        f"{insertion_time:<20.6f}"
        f"{timsort_time:<18.6f}"
        )


def main() -> None:
    random.seed(42)

    sizes = [100, 1_000, 3_000]
    algorithms = [merge_sort, insertion_sort, timsort]

    print(
        f"{'Тип даних':<20}"
        f"{'Розмір':<10}"
        f"{'Merge sort, c':<18}"
        f"{'Insertion sort, c':<20}"
        f"{'Timsort, c':<18}"
        )
    print("-" * 86)

    for size in sizes:
        datasets = {
            "Випадкові": [random.randint(0, size * 10) for _ in range(size)],
            "Відсортовані": list(range(size)),
            "У зворотному порядку": list(range(size, 0, -1)),
            }

        for data_name, data in datasets.items():
            for algorithm in algorithms:
                test_algorithm(algorithm, data)

            merge_time = measure_time(merge_sort, data)
            insertion_time = measure_time(insertion_sort, data)
            timsort_time = measure_time(timsort, data)

            print_result(
                data_name,
                size,
                merge_time,
                insertion_time,
                timsort_time,
                )


if __name__ == "__main__":
    main()