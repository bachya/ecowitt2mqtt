"""Define typing helpers."""
from collections.abc import Collection
from datetime import datetime
from typing import Literal, Union

CalculatedValueType = Collection[str] | float, str | datetime | None
PreCalculatedValueType = float | str
UnitSystemType = Literal["imperial", "metric"]
