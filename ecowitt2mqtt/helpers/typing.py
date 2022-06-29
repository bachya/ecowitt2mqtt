"""Define typing helpers."""
from datetime import datetime
from typing import Collection, Literal, Union

DataValueType = Union[Collection[str], float, str, datetime, None]
UnitSystemType = Literal["imperial", "metric"]
