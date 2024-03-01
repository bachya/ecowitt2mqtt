"""Define utilities."""

from __future__ import annotations

from typing import TypeVar

from rapidfuzz import fuzz

T = TypeVar("T")

DEFAULT_FUZZY_THRESHOLD = 80


def _get_fuzzy_match(candidates: list[str], key: str) -> str:
    """Get a fuzzy match from a list of strings."""
    candidates = sorted(candidates, key=lambda m: fuzz.ratio(key, m), reverse=True)
    return candidates[0]


def glob_search(data: dict[str, T], key: str) -> tuple[str, T] | tuple[None, None]:
    """Get a key/value pair from a dict based on a target key.

    Args:
        data: The data dictionary to search.
        key: The key to search for

    Returns:
        A tuple of either the matching key/value or a None/None.
    """
    if key in data:
        # If the exact key is in the data, return it and its value:
        return (key, data[key])

    if matches := [k for k in data if k in key]:
        # If there are any keys that are substrings of the target key, return the
        # closest one:
        match = _get_fuzzy_match(matches, key)
        return (match, data[match])

    if matches := [k for k in data if fuzz.ratio(key, k) >= DEFAULT_FUZZY_THRESHOLD]:
        # If there are any keys that are fuzzy matches of the target key, return the
        # closest one:
        match = _get_fuzzy_match(matches, key)
        return (match, data[match])

    # ...otherwise, return None/None:
    return (None, None)
