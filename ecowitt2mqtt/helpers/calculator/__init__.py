"""Define various calculators."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Dict, TypeVar

from ecowitt2mqtt.const import UNIT_SYSTEM_IMPERIAL
from ecowitt2mqtt.errors import EcowittError
from ecowitt2mqtt.helpers.typing import CalculatedValueType, PreCalculatedValueType

if TYPE_CHECKING:
    from ecowitt2mqtt.config import Config

_CalculatorType = TypeVar("_CalculatorType", bound="Calculator")
_CalculateFromPayloadFuncType = Callable[
    [_CalculatorType, Dict[str, PreCalculatedValueType]], "CalculatedDataPoint"
]


class CalculationKeysMissingError(EcowittError):
    """Define an error when keys required for a calculated data point are missing."""

    pass


class DataPointType(Enum):
    """Define types of battery configuration."""

    BOOLEAN = 1
    NON_BOOLEAN = 2


@dataclass
class CalculatedDataPoint:
    """Define a calculated data point."""

    data_point_key: str
    value: CalculatedValueType
    unit: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    data_type: DataPointType = DataPointType.NON_BOOLEAN


class Calculator:
    """Define a calculator."""

    def __init__(self, config: Config, payload_key: str, data_point_key: str) -> None:
        """Initialize."""
        self._config = config
        self._data_point_key = data_point_key
        self._payload_key = payload_key

    @property
    def default_imperial_unit(self) -> str | None:
        """Get the default unit (imperial)."""
        return None

    @property
    def default_metric_unit(self) -> str | None:
        """Get the default unit (metric)."""
        return None

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        return None

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""

    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""

    def get_calculated_data_point(
        self,
        value: CalculatedValueType,
        *,
        attributes: dict[str, Any] | None = None,
        data_type: DataPointType | None = None,
    ) -> CalculatedDataPoint:
        """Get the output unit for this calculation."""
        output_unit: str | None

        # If the user explicitly sets self.output_unit, use it if it's truthy;
        # otherwise, default to the standard output unit for the unit system:
        if self.output_unit:
            output_unit = self.output_unit
        elif self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            output_unit = self.default_imperial_unit
        else:
            output_unit = self.default_metric_unit

        data_point = CalculatedDataPoint(
            data_point_key=self._data_point_key, value=value, unit=output_unit
        )

        if attributes:
            data_point.attributes = attributes
        if data_type:
            data_point.data_type = data_type

        return data_point

    @staticmethod
    def requires_keys(
        *keys: Iterable[str],
    ) -> Callable[[_CalculateFromPayloadFuncType], _CalculateFromPayloadFuncType]:
        """Define a decorator that requires certain payload keys to exist."""

        def decorator(
            func: _CalculateFromPayloadFuncType,
        ) -> _CalculateFromPayloadFuncType:
            """Decorate."""

            @wraps(func)
            def wrapper(
                calculator: _CalculatorType, payload: dict[str, PreCalculatedValueType]
            ) -> CalculatedDataPoint:
                """Wrap."""
                if not all(k in payload for k in keys):
                    raise CalculationKeysMissingError
                return func(calculator, payload)

            return wrapper

        return decorator


class SimpleCalculator(Calculator):
    """Define a calculator that returns a value as-is (with an added unit)."""

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        return self.get_calculated_data_point(value)
