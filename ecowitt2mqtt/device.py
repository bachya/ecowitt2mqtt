"""Simple data object to store device details."""
from typing import NamedTuple

class Device(NamedTuple):
    """Simple data object to provide device details."""
    manufacturer: str
    name: str
