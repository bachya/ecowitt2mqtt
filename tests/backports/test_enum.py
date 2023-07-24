"""Define tests for enum backports."""
# pylint: disable=too-few-public-methods,unused-variable
from enum import auto

import pytest

from ecowitt2mqtt.backports.enum import StrEnum


def test_strenum() -> None:
    """Test StrEnum."""

    class TestEnum(StrEnum):
        """Define a test StrEnum."""

        TEST = "test"

    test = TestEnum.TEST
    assert str(test) == "test"
    assert test == "test"
    assert TestEnum("test") == TestEnum.TEST
    assert TestEnum(TestEnum.TEST) == TestEnum.TEST

    with pytest.raises(ValueError):
        TestEnum(42)  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        TestEnum("str but unknown")

    with pytest.raises(TypeError):

        class FailEnum(StrEnum):
            """Define an incorrect StrEnum."""

            TEST = 42

    with pytest.raises(TypeError):

        class FailEnum2(StrEnum):
            """Define an StrEnum that implements auto()."""

            TEST = auto()
