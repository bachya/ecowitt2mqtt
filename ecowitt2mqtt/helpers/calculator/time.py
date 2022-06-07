"""Define time utilities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from ecowitt2mqtt.const import TIME_SECONDS
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


def calculate_dt_from_epoch(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate a datetime from an epoch."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=datetime.utcfromtimestamp(value).replace(tzinfo=timezone.utc),
    )


def calculate_runtime(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate a datetime from an epoch."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=TIME_SECONDS
    )
