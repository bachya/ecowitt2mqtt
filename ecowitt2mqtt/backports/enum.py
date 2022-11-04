"""Define enum backports from the standard library."""
# pylint: disable=unused-variable
from __future__ import annotations

from enum import Enum
from typing import Any, TypeVar

_StrEnumSelfT = TypeVar("_StrEnumSelfT", bound="StrEnum")


class StrEnum(str, Enum):
    """Define a partial backport of Python 3.11's StrEnum."""

    def __new__(
        cls: type[_StrEnumSelfT], value: str, *args: Any, **kwargs: Any
    ) -> _StrEnumSelfT:
        """Create a new StrEnum instance.

        Args:
            value: The enum value.
            args: Additional args.
            kwargs: Additional kwargs.

        Returns:
            The enum.

        Raises:
            TypeError: Raised when an enumerated value isn't a string.
        """
        if not isinstance(value, str):
            raise TypeError(f"{value!r} is not a string")
        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self) -> str:
        """Return self.value.

        Returns:
            The string value.
        """
        return str(self.value)

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list[Any],
    ) -> Any:
        """Make `auto()` explicitly unsupported.

        We may revisit this when it's very clear that Python 3.11's `StrEnum.auto()`
        behavior will no longer change.

        Args:
            name: The name of the enum.
            start: The starting index.
            count: The total number of enumerated values.
            last_values: Previously enumerated values.

        Raises:
            TypeError: Always raised.
        """
        raise TypeError("auto() is not supported by this implementation")
