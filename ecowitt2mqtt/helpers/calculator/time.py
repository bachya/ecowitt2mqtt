"""Define time utilities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


def calculate_dt_from_epoch(ecowitt: Ecowitt, *, value: int) -> CalculatedDataPoint:
    """Calculate a datetime from an epoch."""
    return CalculatedDataPoint(
        datetime.utcfromtimestamp(value).replace(tzinfo=timezone.utc), None
    )
