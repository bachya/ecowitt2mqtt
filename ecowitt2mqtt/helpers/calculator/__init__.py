"""Define various calculators."""
from __future__ import annotations

from dataclasses import dataclass

from ecowitt2mqtt.helpers.typing import DataValueType


@dataclass(frozen=True)
class CalculatedDataPoint:
    """Define a calculated data point."""

    value: DataValueType
    unit: str | None
