"""Define various calculators."""
from typing import TypeVar

T = TypeVar("T")


def calculate_noop(value: T) -> T:
    """Define a noop calculator."""
    return value
