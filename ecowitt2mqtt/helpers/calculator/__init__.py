"""Define various calculators."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ecowitt2mqtt.helpers.typing import DataValueType

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


@dataclass(frozen=True)
class CalculatedDataPoint:
    """Define a calculated data point."""

    value: DataValueType
    unit: str | None


def calculate_noop(ecowitt: Ecowitt, value: DataValueType) -> CalculatedDataPoint:
    """Define a noop calculator."""
    return CalculatedDataPoint(value, None)
