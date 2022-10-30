"""Define typing helpers."""
from datetime import datetime
from typing import Literal

CalculatedValueType = list[str] | float | str | datetime | None
PreCalculatedValueType = float | str
UnitSystemType = Literal["imperial", "metric"]
