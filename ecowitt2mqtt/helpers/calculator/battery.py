"""Define battery calculators."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.const import (
    DATA_POINT_CO2_BATT,
    DATA_POINT_GLOB_LEAFBATT,
    DATA_POINT_GLOB_LEAKBATT,
    DATA_POINT_GLOB_PM25BATT,
    DATA_POINT_GLOB_SOILBATT,
    DATA_POINT_GLOB_TF_BATT,
    DATA_POINT_WH25BATT,
    DATA_POINT_WH26BATT,
    DATA_POINT_WH40BATT,
    DATA_POINT_WH57BATT,
    DATA_POINT_WH65BATT,
    DATA_POINT_WH68BATT,
    DATA_POINT_WH80BATT,
    DATA_POINT_WH90BATT,
    DATA_POINT_WH90BATT_PC,
    DATA_POINT_WH90CAP_VOLT,
    PERCENTAGE,
    UnitOfElectricPotential,
)
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    DataPointType,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util import glob_search

if TYPE_CHECKING:
    from ecowitt2mqtt.config import Config


class BatteryStrategy(StrEnum):
    """Define types of battery configuration."""

    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    PERCENTAGE = "percentage"


class BooleanBatteryState(StrEnum):
    """Define types of battery configuration."""

    OFF = "OFF"
    ON = "ON"


BATTERY_STRATEGY_MAP = {
    DATA_POINT_CO2_BATT: BatteryStrategy.PERCENTAGE,
    DATA_POINT_GLOB_LEAFBATT: BatteryStrategy.NUMERIC,
    DATA_POINT_GLOB_LEAKBATT: BatteryStrategy.PERCENTAGE,
    DATA_POINT_GLOB_PM25BATT: BatteryStrategy.PERCENTAGE,
    DATA_POINT_GLOB_SOILBATT: BatteryStrategy.NUMERIC,
    DATA_POINT_GLOB_TF_BATT: BatteryStrategy.NUMERIC,
    DATA_POINT_WH25BATT: BatteryStrategy.BOOLEAN,
    DATA_POINT_WH26BATT: BatteryStrategy.BOOLEAN,
    DATA_POINT_WH40BATT: BatteryStrategy.NUMERIC,
    DATA_POINT_WH57BATT: BatteryStrategy.PERCENTAGE,
    DATA_POINT_WH65BATT: BatteryStrategy.BOOLEAN,
    DATA_POINT_WH68BATT: BatteryStrategy.NUMERIC,
    DATA_POINT_WH80BATT: BatteryStrategy.NUMERIC,
    DATA_POINT_WH90BATT: BatteryStrategy.NUMERIC,
    DATA_POINT_WH90BATT_PC: BatteryStrategy.PERCENTAGE,
    DATA_POINT_WH90CAP_VOLT: BatteryStrategy.NUMERIC,
}


def get_battery_strategy(config: Config, key: str) -> BatteryStrategy:
    """Get the battery strategy for a particular key.

    Args:
        config: A Config object.
        key: A key from an Ecowitt data payload.

    Returns:
        A parsed BatteryStrategy object.
    """
    strategies = [config.battery_overrides.get(key)]

    data_point, strategy = glob_search(BATTERY_STRATEGY_MAP, key)
    if data_point:
        strategies.append(strategy)

    for strategy in strategies:
        # Use a strategy other than the default if:
        #   1. There's a user-provided override
        #   2. We have a static mapping for this particular battery type
        if strategy is not None:
            return strategy

    return config.default_battery_strategy


class BatteryCalculator(Calculator):
    """Define a battery calculator."""

    def __init__(self, config: Config, payload_key: str, data_point_key: str) -> None:
        """Initialize.

        Args:
            config: A Config object.
            payload_key: The Ecowitt payload key.
            data_point_key: The data point type for this key.
        """
        super().__init__(config, payload_key, data_point_key)

        self._battery_strategy = get_battery_strategy(config, payload_key)

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation.

        Returns:
            An optional string.
        """
        if self._battery_strategy == BatteryStrategy.NUMERIC:
            return UnitOfElectricPotential.VOLT
        if self._battery_strategy == BatteryStrategy.PERCENTAGE:
            return PERCENTAGE
        return None

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            value: A pre-calculated value.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        float_value = cast(float, value)

        if self._battery_strategy == BatteryStrategy.NUMERIC:
            return self.get_calculated_data_point(float_value)

        if self._battery_strategy == BatteryStrategy.PERCENTAGE:
            # Percentage batteries occur in "steps":
            #   * 1 = 20%
            #   * 2 = 40%
            #   * 3 = 60%
            #   * 4 = 80%
            #   * 5 = 100%
            #   * 6 = 120% (plugged into mains voltage)
            return self.get_calculated_data_point(float_value * 20)

        if float_value == self._config.boolean_battery_true_value:
            return self.get_calculated_data_point(
                BooleanBatteryState.ON, data_type=DataPointType.BOOLEAN
            )
        return self.get_calculated_data_point(
            BooleanBatteryState.OFF, data_type=DataPointType.BOOLEAN
        )
