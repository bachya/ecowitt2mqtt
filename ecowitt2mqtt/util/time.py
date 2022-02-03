"""Define time utilities."""
from datetime import datetime, timezone


def calculate_epoch(value: int) -> datetime:
    """Calculate a datetime from an epoch."""
    return datetime.utcfromtimestamp(value).replace(tzinfo=timezone.utc)
