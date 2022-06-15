"""Define utilities."""
from __future__ import annotations

from typing import Iterable, cast

from thefuzz import fuzz


def glob_search(data: Iterable, key: str) -> str | None:
    """Get the data point identified for a particular key according to some rules.

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
    return cast(str, sorted_matches[0])
