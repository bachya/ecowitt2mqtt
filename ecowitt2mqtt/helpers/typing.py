"""Define typing helpers."""
from datetime import datetime
from typing import Collection, Literal, Union

CalculatedValueType = Union[Collection[str], float, str, datetime, None]
PreCalculatedValueType = Union[float, str]
UnitSystemType = Literal["imperial", "metric"]
