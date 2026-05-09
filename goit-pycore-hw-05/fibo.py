from typing import Callable


def caching_fibonacci() -> Callable:
    cache = {0: 0, 1: 1}

    def fibonacci(n: int) -> int:
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
