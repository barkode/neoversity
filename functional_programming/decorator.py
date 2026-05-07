from typing import Callable


def complicated(x: int, y: int) -> int:
    return x + y


def logger(func: Callable) -> Callable:
    def inner(x: int, y: int) -> int:
        print(f"Call function: {func.__name__}: {x}, {y}")
        result = func(x, y)
        print(f"Function {func.__name__} finished with result: {result}")
        return result

    return inner


complicated = logger(complicated)
print(complicated(2, 3))

# Rewrite code with python @decorator

print("Rewrite code with python @decorator")


@logger
def complicated(x: int, y: int) -> int:
    return x + y


print(complicated(2, 3))

# Preserving the metadata of the original function
from functools import wraps


def logger(func: Callable) -> Callable:
    @wraps(func)
    def inner(x: int, y: int) -> int:
        print(f"Call function: {func.__name__}: {x}, {y}")
        result = func(x, y)
        print(f"Function {func.__name__} finished with result: {result}")
        return result

    return inner


@logger
def complicated(x: int, y: int) -> int:
    return x + y


print(complicated(2, 3))
print(f"Decorated function name: {complicated.__name__}")
