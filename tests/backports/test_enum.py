"""Test enum backports."""
import pytest

from ecowitt2mqtt.backports.enum import StrEnum


def test_invalid_strenum():  # noqa: D202
    """Test invalid use of a StrEnum."""

    with pytest.raises(TypeError):

        class InvalidTest(StrEnum):
            """Define an invalid StrEnum."""

            VAL1 = 12


def test_valid_strenum():
    """Test valid use of a StrEnum."""

    class ValidTest(StrEnum):
        """Define a valid test StrEnum."""

        VAL1 = "val1"
        VAL2 = "val2"
        VAL3 = "val3"

    assert ValidTest.VAL1 == "val1"
    assert str(ValidTest.VAL1) == "val1"
    assert ValidTest.VAL1 != ValidTest.VAL2
