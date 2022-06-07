"""Define utility modules."""
from __future__ import annotations

import asyncio
from typing import Any, Callable, Iterable

from thefuzz import fuzz


def execute_callback(callback: Callable[..., Any], *args: Any) -> None:
    """Schedule a callback to be called."""
    if asyncio.iscoroutinefunction(callback):
        asyncio.create_task(callback(*args))
    else:
        callback(*args)


def glob_search(data: Iterable[str], key: str) -> str | None:
    """Search an iterable for a key according to some rules.

    1. If the exact key exists, return it.
    2. If a single glob exists return it.
    3. If multiple globs exist, return the "closest" (Levenshtein distance).
    4. If none of these are satisfied, return None.
    """
    if key in data:
        return key

    # If no keys (specific or globbed) match, we don't have a calculator:
    if not (matches := [k for k in data if k in key]):
        return None

    # Return the closest match based on the Levenshtein distance from the key:
    #   Example Key: "winddir_avg10m"
    #   Matches: ["wind", "winddir"]
    #   Closest Match: "winddir"
    sorted_matches = sorted(
        matches, key=lambda m: fuzz.ratio(key, m), reverse=True  # type: ignore
    )
    return sorted_matches[0]
