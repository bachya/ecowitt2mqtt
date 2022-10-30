"""Define utilities."""
from __future__ import annotations

from typing import TypeVar, cast

from rapidfuzz import fuzz

T = TypeVar("T")


def glob_search(data: dict[str, T], key: str) -> tuple[str, T] | tuple[None, None]:
    """Get a key/value pair from a dict based on some rules.

    1. If the exact key exists, use it.
    2. If a single glob exists, use it.
    3. If multiple globs exist, use the "closest" (Levenshtein distance).
    4. If none of these are satisfied, return None.

    Args:
        data: The data dictionary to search.
        key: The key to search for

    Returns:
        A tuple of either the matching key/value or a None/None.
    """
    if key in data:
        return (key, data[key])

    # If no keys (specific or globbed) match, we don't have a calculator:
    if not (matches := [k for k in data if k in key]):
        return (None, None)

    # Return the closest match based on the Levenshtein distance from the key:
    #   Example Key: "winddir_avg10m"
    #   Matches: ["wind", "winddir"]  # noqa: E800
    #   Closest Match: "winddir"
    sorted_matches = sorted(
        matches, key=lambda m: cast(str, fuzz.ratio(key, m)), reverse=True
    )
    match = sorted_matches[0]
    return (match, data[match])
