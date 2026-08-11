from collections import Counter
from timeit import timeit

COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int) -> dict:
    """Повертає решту за жадібним алгоритмом."""
    if not isinstance(amount, int) or amount < 0:
        raise ValueError("Сума має бути цілим невід'ємним числом.")

    result = {}

    for coin in COINS:
        count, amount = divmod(amount, coin)

        if count > 0:
            result[coin] = count

    return result


def find_min_coins(amount: int) -> dict:
    """Повертає решту з мінімальною кількістю монет методом ДП."""
    if not isinstance(amount, int) or amount < 0:
        raise ValueError("Сума має бути цілим невід'ємним числом.")

    min_coins = [float("inf")] * (amount + 1)
    last_coin = [0] * (amount + 1)
    min_coins[0] = 0

    for current_amount in range(1, amount + 1):
        for coin in COINS:
            if coin <= current_amount:
                candidate = min_coins[current_amount - coin] + 1

                if candidate < min_coins[current_amount]:
                    min_coins[current_amount] = candidate
                    last_coin[current_amount] = coin

    result = Counter()
    current_amount = amount

    while current_amount > 0:
        coin = last_coin[current_amount]
        result[coin] += 1
        current_amount -= coin

    return dict(sorted(result.items()))


if __name__ == "__main__":
    amount = 113

    print(f"Сума: {amount}")
    print("Жадібний алгоритм:", find_coins_greedy(amount))
    print("Динамічне програмування:", find_min_coins(amount))

    large_amount = 10_000

    greedy_time = timeit(
        lambda: find_coins_greedy(large_amount),
        number=1_000,
        )

    dynamic_time = timeit(
        lambda: find_min_coins(large_amount),
        number=10,
        )

    print(f"Час жадібного алгоритму для {large_amount}: {greedy_time:.6f} с")
    print(f"Час ДП для {large_amount}: {dynamic_time:.6f} с")