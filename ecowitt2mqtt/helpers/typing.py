"""Define typing helpers."""
from collections.abc import Collection
from datetime import datetime
from typing import Literal, Union

# pylint: disable=consider-alternative-union-syntax
CalculatedValueType = Union[Collection[str], float, str, datetime, None]
PreCalculatedValueType = Union[float, str]
UnitSystemType = Literal["imperial", "metric"]
