"""Define typing helpers."""
from datetime import datetime
from typing import Literal, Union

DataValueType = Union[float, int, str, datetime, None]
UnitSystemType = Literal["imperial", "metric"]
