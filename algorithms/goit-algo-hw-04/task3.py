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


def timsort_sorted(data: list[int]) -> list[int]:
    """Вбудоване сортування Python — Timsort."""
    return sorted(data)

def timsort_sort(data: list[int]) -> list[int]:
    data = data.copy()
    data.sort()
    return data


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


def bucket_sort(data: list[int]) -> list[int]:
    """
    Сортування відрами (Bucket Sort).
    Ефективне для рівномірно розподілених даних.
    Середня складність: O(n + k), де k — кількість відер.
    Найгірша складність: O(n^2).
    """
    if not data:
        return []

    result = data.copy()
    min_val = min(result)
    max_val = max(result)

    if min_val == max_val:
        return result

    bucket_count = len(result)
    buckets: list[list[int]] = [[] for _ in range(bucket_count)]
    value_range = max_val - min_val

    for value in result:
        # Визначаємо індекс відра
        index = int((value - min_val) / value_range * (bucket_count - 1))
        buckets[index].append(value)

    # Сортуємо кожне відро вставками та збираємо результат
    sorted_result = []
    for bucket in buckets:
        sorted_result.extend(insertion_sort(bucket))

    return sorted_result


def radix_sort(data: list[int]) -> list[int]:
    """
    Порозрядне сортування (Radix Sort, LSD).
    Ефективне для цілих невід'ємних чисел.
    Складність: O(n * d), де d — кількість цифр у максимальному числі.
    """
    if not data:
        return []

    result = data.copy()

    if any(x < 0 for x in result):
        raise ValueError("Radix Sort підтримує лише невід'ємні цілі числа.")

    max_val = max(result)
    exp = 1  # Поточний розряд: 1, 10, 100, ...

    while max_val // exp > 0:
        result = _counting_sort_by_digit(result, exp)
        exp *= 10

    return result


def _counting_sort_by_digit(data: list[int], exp: int) -> list[int]:
    """Допоміжна функція: сортування підрахунком за одним розрядом."""
    n = len(data)
    output = [0] * n
    count = [0] * 10  # Цифри від 0 до 9

    for value in data:
        digit = (value // exp) % 10
        count[digit] += 1

    # Накопичувальна сума
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Будуємо вихідний масив (з кінця для стабільності)
    for i in range(n - 1, -1, -1):
        digit = (data[i] // exp) % 10
        output[count[digit] - 1] = data[i]
        count[digit] -= 1

    return output

def print_result(
        data_name: str,
        size: int,
        merge_time: float,
        insertion_time: float,
        timsort_sorted_time: float,
        timsort_sort_time: float,
        bucket_time: float,
        radix_time: float,
        ) -> None:
    """Виводить результати в табличному вигляді."""
    print(
        f"{data_name:<20}"
        f"{size:<10}"
        f"{merge_time:<18.6f}"
        f"{insertion_time:<20.6f}"
        f"{timsort_sorted_time:<18.6f}"
        f"{timsort_sort_time:<18.6f}"
        f"{bucket_time:<18.6f}"
        f"{radix_time:<18.6f}"
        )


def main() -> None:
    random.seed(42)

    sizes = [100, 1_000, 10_000]
    algorithms = [merge_sort, insertion_sort, timsort_sorted, timsort_sort, bucket_sort, radix_sort]

    print(
        f"{'Data type':<20}"
        f"{'Size':<16}"
        f"{'Merge sort, c':<18}"
        f"{'Insertion sort, c':<18}"
        f"{'Timsort sorted, c':<18}"
        f"{'Timsort sort, c':<18}"
        f"{'Bucket sort, c':<18}"
        f"{'Radix sort, c':<18}"
        )
    print("-" * 86)

    for size in sizes:
        datasets = {
            "Random": [random.randint(0, size * 10) for _ in range(size)],
            "Sorted": list(range(size)),
            "Reverse": list(range(size, 0, -1)),
            }

        for data_name, data in datasets.items():
            for algorithm in algorithms:
                test_algorithm(algorithm, data)

            merge_time = measure_time(merge_sort, data)
            insertion_time = measure_time(insertion_sort, data)
            timsort_sorted_time = measure_time(timsort_sorted, data)
            timsort_sort_time = measure_time(timsort_sort, data)
            bucket_time = measure_time(bucket_sort, data)
            radix_time = measure_time(radix_sort, data)

            print_result(
                data_name,
                size,
                merge_time,
                insertion_time,
                timsort_sorted_time,
                timsort_sort_time,
                bucket_time,
                radix_time,
                )


if __name__ == "__main__":
    main()