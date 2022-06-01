"""Define time utilities."""
from datetime import datetime, timezone

from ecowitt2mqtt.helpers.typing import DataValueType


def calculate_dt_from_epoch(value: int) -> DataValueType:
    """Calculate a datetime from an epoch."""
    return datetime.utcfromtimestamp(value).replace(tzinfo=timezone.utc)
