"""Define typing helpers."""
from datetime import datetime
from typing import Collection, Literal, TypeVar, Union

CalculatedValueType = TypeVar(
    "CalculatedValueType", bound=Union[Collection[str], float, str, datetime, None]
)
PreCalculatedValueType = TypeVar(
    "PreCalculatedValueType", bound=Union[float, int, str, None]
)
UnitSystemType = Literal["imperial", "metric"]
