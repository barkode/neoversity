import re

from typing import Callable, Generator


def generator_numbers(text: str) -> Generator:
    """Generator numbers from text"""
    for match in re.finditer(r'\d+\.\d+|\d+', text):
        yield float(match.group())


def sum_profit(text: str, func: Callable) -> float:
    """Sum profit from text"""
    return sum(func(text))
