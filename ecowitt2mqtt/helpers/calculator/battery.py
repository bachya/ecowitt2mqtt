"""Define battery utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING

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
    ELECTRIC_POTENTIAL_VOLT,
    PERCENTAGE,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, DataPointType
from ecowitt2mqtt.util import glob_search

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


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


def calculate_battery(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate a battery value."""
    strategy = get_battery_strategy(ecowitt, payload_key)

    if strategy == BatteryStrategy.NUMERIC:
        return CalculatedDataPoint(
            data_point_key=data_point_key, value=value, unit=ELECTRIC_POTENTIAL_VOLT
        )
    if strategy == BatteryStrategy.PERCENTAGE:
        # Percentage batteries occur in "steps":
        #   * 1 = 20%
        #   * 2 = 40%
        #   * 3 = 60%
        #   * 4 = 80%
        #   * 5 = 100%
        #   * 6 = 120% (plugged into mains voltage)
        return CalculatedDataPoint(
            data_point_key=data_point_key, value=value * 20, unit=PERCENTAGE
        )
    if value == 0.0:
        return CalculatedDataPoint(
            data_point_key=data_point_key,
            value=BooleanBatteryState.OFF,
            data_type=DataPointType.BOOLEAN,
        )
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=BooleanBatteryState.ON,
        data_type=DataPointType.BOOLEAN,
    )


def get_battery_strategy(ecowitt: Ecowitt, key: str) -> BatteryStrategy:
    """Get the battery strategy for a particular key."""
    strategies = [ecowitt.config.battery_overrides.get(key)]

    data_point, strategy = glob_search(BATTERY_STRATEGY_MAP, key)
    if data_point:
        strategies.append(strategy)

    for strategy in strategies:
        # Use a strategy other than the default if:
        #   1. There's a user-provided override
        #   2. We have a static mapping for this particular battery type
        if strategy is not None:
            return strategy

    return ecowitt.config.default_battery_strategy
