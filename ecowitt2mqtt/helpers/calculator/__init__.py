"""Define various calculators."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ecowitt2mqtt.helpers.typing import DataValueType


class DataPointType(Enum):
    """Define types of battery configuration."""

    BOOLEAN = 1
    NON_BOOLEAN = 2


@dataclass
class CalculatedDataPoint:
    """Define a calculated data point."""

    data_point_key: str
    value: DataValueType
    unit: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    data_type: DataPointType = DataPointType.NON_BOOLEAN
