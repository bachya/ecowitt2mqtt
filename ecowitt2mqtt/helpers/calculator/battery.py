"""Define battery utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.const import (
    DATA_POINT_BATTERY1,
    DATA_POINT_BATTERY2,
    DATA_POINT_BATTERY3,
    DATA_POINT_BATTERY4,
    DATA_POINT_BATTERY5,
    DATA_POINT_BATTERY6,
    DATA_POINT_BATTERY7,
    DATA_POINT_BATTERY8,
    DATA_POINT_CO2_BATT,
    DATA_POINT_LEAKBATT1,
    DATA_POINT_LEAKBATT2,
    DATA_POINT_LEAKBATT3,
    DATA_POINT_LEAKBATT4,
    DATA_POINT_LEAKBATT5,
    DATA_POINT_LEAKBATT6,
    DATA_POINT_LEAKBATT7,
    DATA_POINT_LEAKBATT8,
    DATA_POINT_PM25BATT1,
    DATA_POINT_PM25BATT2,
    DATA_POINT_PM25BATT3,
    DATA_POINT_PM25BATT4,
    DATA_POINT_PM25BATT5,
    DATA_POINT_PM25BATT6,
    DATA_POINT_PM25BATT7,
    DATA_POINT_PM25BATT8,
    DATA_POINT_SOILBATT1,
    DATA_POINT_SOILBATT2,
    DATA_POINT_SOILBATT3,
    DATA_POINT_SOILBATT4,
    DATA_POINT_SOILBATT5,
    DATA_POINT_SOILBATT6,
    DATA_POINT_SOILBATT7,
    DATA_POINT_SOILBATT8,
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
    DATA_POINT_WN34BATT1,
    DATA_POINT_WN34BATT2,
    DATA_POINT_WN34BATT3,
    DATA_POINT_WN34BATT4,
    DATA_POINT_WN34BATT5,
    DATA_POINT_WN34BATT6,
    DATA_POINT_WN34BATT7,
    DATA_POINT_WN34BATT8,
    ELECTRIC_POTENTIAL_VOLT,
    PERCENTAGE,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint

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
    DATA_POINT_BATTERY1: BatteryStrategy.BOOLEAN,
    DATA_POINT_BATTERY2: BatteryStrategy.BOOLEAN,
    DATA_POINT_BATTERY3: BatteryStrategy.BOOLEAN,
    DATA_POINT_BATTERY4: BatteryStrategy.BOOLEAN,
    DATA_POINT_BATTERY5: BatteryStrategy.BOOLEAN,
    DATA_POINT_BATTERY6: BatteryStrategy.BOOLEAN,
    DATA_POINT_BATTERY7: BatteryStrategy.BOOLEAN,
    DATA_POINT_BATTERY8: BatteryStrategy.BOOLEAN,
    DATA_POINT_CO2_BATT: BatteryStrategy.PERCENTAGE,
    DATA_POINT_LEAKBATT1: BatteryStrategy.PERCENTAGE,
    DATA_POINT_LEAKBATT2: BatteryStrategy.PERCENTAGE,
    DATA_POINT_LEAKBATT3: BatteryStrategy.PERCENTAGE,
    DATA_POINT_LEAKBATT4: BatteryStrategy.PERCENTAGE,
    DATA_POINT_LEAKBATT5: BatteryStrategy.PERCENTAGE,
    DATA_POINT_LEAKBATT6: BatteryStrategy.PERCENTAGE,
    DATA_POINT_LEAKBATT7: BatteryStrategy.PERCENTAGE,
    DATA_POINT_LEAKBATT8: BatteryStrategy.PERCENTAGE,
    DATA_POINT_PM25BATT1: BatteryStrategy.PERCENTAGE,
    DATA_POINT_PM25BATT2: BatteryStrategy.PERCENTAGE,
    DATA_POINT_PM25BATT3: BatteryStrategy.PERCENTAGE,
    DATA_POINT_PM25BATT4: BatteryStrategy.PERCENTAGE,
    DATA_POINT_PM25BATT5: BatteryStrategy.PERCENTAGE,
    DATA_POINT_PM25BATT6: BatteryStrategy.PERCENTAGE,
    DATA_POINT_PM25BATT7: BatteryStrategy.PERCENTAGE,
    DATA_POINT_PM25BATT8: BatteryStrategy.PERCENTAGE,
    DATA_POINT_SOILBATT1: BatteryStrategy.NUMERIC,
    DATA_POINT_SOILBATT2: BatteryStrategy.NUMERIC,
    DATA_POINT_SOILBATT3: BatteryStrategy.NUMERIC,
    DATA_POINT_SOILBATT4: BatteryStrategy.NUMERIC,
    DATA_POINT_SOILBATT5: BatteryStrategy.NUMERIC,
    DATA_POINT_SOILBATT6: BatteryStrategy.NUMERIC,
    DATA_POINT_SOILBATT7: BatteryStrategy.NUMERIC,
    DATA_POINT_SOILBATT8: BatteryStrategy.NUMERIC,
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
    DATA_POINT_WN34BATT1: BatteryStrategy.NUMERIC,
    DATA_POINT_WN34BATT2: BatteryStrategy.NUMERIC,
    DATA_POINT_WN34BATT3: BatteryStrategy.NUMERIC,
    DATA_POINT_WN34BATT4: BatteryStrategy.NUMERIC,
    DATA_POINT_WN34BATT5: BatteryStrategy.NUMERIC,
    DATA_POINT_WN34BATT6: BatteryStrategy.NUMERIC,
    DATA_POINT_WN34BATT7: BatteryStrategy.NUMERIC,
    DATA_POINT_WN34BATT8: BatteryStrategy.NUMERIC,
}


def calculate_battery(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
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
            data_point_key=data_point_key, value=BooleanBatteryState.OFF
        )
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=BooleanBatteryState.ON
    )


def get_battery_strategy(ecowitt: Ecowitt, key: str) -> BatteryStrategy:
    """Get the battery strategy for a particular key."""
    for strategy in (
        ecowitt.config.battery_overrides.get(key),
        BATTERY_STRATEGY_MAP.get(key),
    ):
        # Use a strategy other than the default if:
        #   1. There's a user-provided override
        #   2. We have a static mapping for this particular battery type
        if strategy is not None:
            return strategy

    return ecowitt.config.default_battery_strategy
