"""Define various calculators."""

from __future__ import annotations

import locale
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar, cast

from ecowitt2mqtt.const import UnitSystem
from ecowitt2mqtt.errors import EcowittError
from ecowitt2mqtt.helpers.typing import CalculatedValueType, PreCalculatedValueType
from ecowitt2mqtt.util.unit_conversion import BaseUnitConverter

if TYPE_CHECKING:
    from ecowitt2mqtt.config import Config

_CalculatorT = TypeVar("_CalculatorT", bound="Calculator")
_CalculateFromPayloadFuncT = Callable[
    [_CalculatorT, dict[str, PreCalculatedValueType]], "CalculatedDataPoint"
]


class CalculationFailedError(EcowittError):
    """Define an error when calculation fails."""

    pass


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

    DEFAULT_INPUT_UNIT: str
    UNIT_OVERRIDE_CONFIG_OPTION: str | None = None

    def __init__(self, config: Config, payload_key: str, data_point_key: str) -> None:
        """Initialize.

        Args:
            config: A Config object.
            payload_key: The Ecowitt payload key.
            data_point_key: The data point type for this key.
        """
        self._config = config
        self._data_point_key = data_point_key
        self._payload_key = payload_key

    @property
    def output_unit_imperial(self) -> str | None:  # pylint: disable=W9008
        """Get the default unit (imperial).

        Returns:
            A string or None if appropriate.
        """
        return None

    @property
    def output_unit_metric(self) -> str | None:  # pylint: disable=W9008
        """Get the default unit (metric).

        Returns:
            A string or None if appropriate.
        """
        return None

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation.

        Returns:
            A string or None if appropriate.
        """
        if (
            override := getattr(
                self._config, str(self.UNIT_OVERRIDE_CONFIG_OPTION), None
            )
        ) is not None:
            return cast(str, override)
        if self._config.output_unit_system == UnitSystem.IMPERIAL:
            return self.output_unit_imperial
        return self.output_unit_metric

    def calculate_from_value(  # type: ignore[empty-body]
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            value: A pre-calculated value.
        """

    def calculate_from_payload(  # type: ignore[empty-body]
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.
        """

    def get_calculated_data_point(
        self,
        value: CalculatedValueType,
        *,
        unit_converter: type[BaseUnitConverter] | None = None,
        data_type: DataPointType = DataPointType.NON_BOOLEAN,
        attributes: dict[str, Any] | None = None,
    ) -> CalculatedDataPoint:
        """Get the output unit for this calculation.

        Args:
            value: The parsed value to use in a CalculatedDataPoint.
            unit_converter: An option BaseUnitConverter subclass.
            data_type: A DataPointType value.
            attributes: Optional attributes to add to the final CalculatedDataPoint.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        if unit_converter and self.output_unit and isinstance(value, float):
            value = unit_converter.convert(
                value, self.DEFAULT_INPUT_UNIT, self.output_unit
            )

        if self._config.precision:
            if isinstance(value, float):
                value = round(value, self._config.precision)
            else:
                try:
                    value = round(locale.atof(str(value)), self._config.precision)
                except ValueError:
                    # This conversion is in place to see if we have a non-standard float
                    # notation; if we can't parse it as such, leave the value as-is:
                    pass

        data_point = CalculatedDataPoint(
            data_point_key=self._data_point_key,
            value=value,
            unit=self.output_unit,
            data_type=data_type,
        )

        if attributes:
            data_point.attributes = attributes

        return data_point

    @staticmethod
    def requires_keys(
        *keys: Iterable[str],
    ) -> Callable[[_CalculateFromPayloadFuncT], _CalculateFromPayloadFuncT]:
        """Define a decorator that requires certain payload keys to exist.

        Args:
            keys: A series of strings.

        Returns:
            A decorated Callable.
        """

        def decorator(
            func: _CalculateFromPayloadFuncT,
        ) -> _CalculateFromPayloadFuncT:
            """Decorate.

            Args:
                func: The Callable to decorate.

            Returns:
                A decorated Callable.
            """

            @wraps(func)
            def wrapper(
                calculator: _CalculatorT, payload: dict[str, PreCalculatedValueType]
            ) -> CalculatedDataPoint:
                """Wrap.

                Args:
                    calculator: A Calculator subclass.
                    payload: A payload to run the calculator on.

                Returns:
                    A parsed CalculatedDataPoint object.

                Raises:
                    CalculationKeysMissingError: Raised if required keys are missing.
                """
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
        """Perform the calculation.

        Args:
            value: A pre-calculated value.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        return self.get_calculated_data_point(value)
