"""Define enum backports from the standard library.

https://github.com/clbarnes/backports.strenum
"""

from enum import Enum
from typing import TypeVar

_S = TypeVar("_S", bound="StrEnum")


class StrEnum(str, Enum):
    """Define an Enum where members are also (and must be) strings."""

    def __new__(cls: type[_S], *values: str) -> _S:
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values}")
        if len(values) == 1:
            # it must be a string
            if not isinstance(values[0], str):
                raise TypeError(f"{values[0]} is not a string")
        if len(values) >= 2:
            # check that encoding argument is a string
            if not isinstance(values[1], str):
                raise TypeError(f"encoding must be a string, not {values[1]}")
        if len(values) == 3:
            # check that errors argument is a string
            if not isinstance(values[2], str):
                raise TypeError(f"errors must be a string, not {values[2]}")
        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    __str__ = str.__str__

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> str:
        """Return the lower-cased version of the member name."""
        return name.lower()
