"""Define various calculators."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, TypeVar

from ecowitt2mqtt.helpers.typing import PreCalculatedValueType

if TYPE_CHECKING:
    from ecowitt2mqtt.config import Config

_CalculatorType = TypeVar("_CalculatorType", bound="Calculator")
_CalculateFromPayloadFuncType = Callable[
    [_CalculatorType, Dict[str, PreCalculatedValueType]], "CalculatedDataPoint"
]


def requires_keys(
    *keys: Iterable[str],
) -> Callable[[_CalculateFromPayloadFuncType], _CalculateFromPayloadFuncType]:
    """Define a decorator that requires certain payload keys to exist."""

    def decorator(func: _CalculateFromPayloadFuncType) -> _CalculateFromPayloadFuncType:
        """Decorate."""

        @wraps(func)
        def wrapper(
            calculator: _CalculatorType, value: dict[str, PreCalculatedValueType]
        ) -> CalculatedDataPoint:
            """Wrap."""
            if not all(k for k in keys if k in value):
                return calculator.get_calculated_data_point(None)
            return func(calculator, value)

        return wrapper

    return decorator


class DataPointType(Enum):
    """Define types of battery configuration."""

    BOOLEAN = 1
    NON_BOOLEAN = 2


@dataclass
class CalculatedDataPoint(Generic[PreCalculatedValueType]):
    """Define a calculated data point."""

    data_point_key: str
    value: PreCalculatedValueType
    unit: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    data_type: DataPointType = DataPointType.NON_BOOLEAN


class Calculator(ABC):
    """Define a calculator."""

    def __init__(self, config: Config, payload_key: str, data_point_key: str) -> None:
        """Initialize."""
        self._config = config
        self._data_point_key = data_point_key
        self._payload_key = payload_key

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        return None

    @abstractmethod
    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""

    @abstractmethod
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""

    def get_calculated_data_point(
        self,
        value: PreCalculatedValueType,
        *,
        attributes: dict[str, Any] | None = None,
        data_type: DataPointType | None = None,
    ) -> CalculatedDataPoint:
        """Get the output unit for this calculation."""
        data_point = CalculatedDataPoint(
            data_point_key=self._data_point_key, value=value
        )

        if attributes:
            data_point.attributes = attributes
        if data_type:
            data_point.data_type = data_type

        return data_point


class SimpleCalculator(Calculator):
    """Define a calculator that returns a value as-is (with an added unit)."""

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        return self.get_calculated_data_point(value)
