"""Define typing helpers."""
from datetime import datetime
from typing import Any, Dict, Literal, Union

DataValueType = Union[Dict[str, Any], float, str, datetime, None]
UnitSystemType = Literal["imperial", "metric"]
