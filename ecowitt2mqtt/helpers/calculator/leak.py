"""Define moisture utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, DataPointType

if TYPE_CHECKING:
    from ecowitt2mqtt.config import Config


class LeakState(StrEnum):
    """Define types of battery configuration."""

    OFF = "OFF"
    ON = "ON"


def calculate_leak(
    config: Config, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate a boolean leak state."""
    if value == 0.0:
        return CalculatedDataPoint(
            data_point_key=data_point_key,
            value=LeakState.OFF,
            data_type=DataPointType.BOOLEAN,
        )
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=LeakState.ON,
        data_type=DataPointType.BOOLEAN,
    )
