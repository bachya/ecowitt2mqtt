"""Define time utilities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from ecowitt2mqtt.const import LOGGER, TIME_SECONDS
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


def calculate_dt_from_epoch(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float | str
) -> CalculatedDataPoint:
    """Calculate a datetime from an epoch."""
    try:
        float_value = float(value)
    except ValueError:
        LOGGER.debug("Can't convert value to number: %s", value)
        return CalculatedDataPoint(data_point_key=data_point_key, value=None)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=datetime.utcfromtimestamp(float_value).replace(tzinfo=timezone.utc),
    )


def calculate_runtime(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate a datetime from an epoch."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=TIME_SECONDS
    )
