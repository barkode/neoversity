import time
import functools


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[{func.__name__}] виконано за {(end - start) * 1000:.4f} мс")
        return result

    return wrapper


@timer
def caching_fibonacci(number: int) -> int:
    cache = {0: 0, 1: 1}

    def fibonacci(n: int) -> int:
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci(number)


print("BEFORE CACHE :")
for i in range(101):
    print(f"FOR number {i} : {caching_fibonacci(i)}")

print("AFTER CACHE :")
for i in range(101):
    print(f"FOR number {i} : {caching_fibonacci(i)}")
