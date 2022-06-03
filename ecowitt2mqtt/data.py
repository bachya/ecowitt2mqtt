"""Define data processing."""
from __future__ import annotations

from dataclasses import dataclass, field
import traceback
from typing import TYPE_CHECKING, Any, Callable, TypeVar

# from ecowitt2mqtt.helpers.calculator.battery import calculate_battery
from ecowitt2mqtt.const import (
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_GUST,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HUMIDITY,
    DATA_POINT_LIGHTNING,
    DATA_POINT_LIGHTNING_NUM,
    DATA_POINT_LIGHTNING_TIME,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_SOLARRADIATION_LUX,
    DATA_POINT_SOLARRADIATION_PERCEIVED,
    DATA_POINT_TEMPF,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDDIR,
    DATA_POINT_WINDSPEEDMPH,
    LOGGER,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, calculate_noop
from ecowitt2mqtt.helpers.calculator.distance import calculate_distance
from ecowitt2mqtt.helpers.calculator.meteo import (
    calculate_dew_point,
    calculate_feels_like,
    calculate_heat_index,
    calculate_illuminance_wm2_to_lux,
    calculate_illuminance_wm2_to_perceived,
    calculate_pressure,
    calculate_rain_volume,
    calculate_temperature,
    calculate_wind_chill,
    calculate_wind_speed,
)
from ecowitt2mqtt.helpers.calculator.time import calculate_dt_from_epoch
from ecowitt2mqtt.helpers.device import Device, get_device_from_raw_payload

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_KEYS_TO_IGNORE = ["PASSKEY", "dateutc", "freq", "model", "stationtype"]

# Map which data calculator functions should apply to various data points:
CALCULATOR_FUNCTION_MAP: dict[str, Callable[..., CalculatedDataPoint]] = {
    DATA_POINT_DEWPOINT: calculate_dew_point,
    DATA_POINT_FEELSLIKE: calculate_feels_like,
    DATA_POINT_GLOB_BAROM: calculate_pressure,
    # DATA_POINT_GLOB_BATT: calculate_battery,
    DATA_POINT_GLOB_RAIN: calculate_rain_volume,
    DATA_POINT_GLOB_TEMP: calculate_temperature,
    DATA_POINT_GLOB_WIND: calculate_wind_speed,
    DATA_POINT_HEATINDEX: calculate_heat_index,
    DATA_POINT_LIGHTNING: calculate_distance,
    # Prevent LIGHTNING_NUM from being treated like LIGHTNING:
    DATA_POINT_LIGHTNING_NUM: calculate_noop,
    DATA_POINT_LIGHTNING_TIME: calculate_dt_from_epoch,
    DATA_POINT_SOLARRADIATION_LUX: calculate_illuminance_wm2_to_lux,
    DATA_POINT_SOLARRADIATION_PERCEIVED: calculate_illuminance_wm2_to_perceived,
    DATA_POINT_WINDCHILL: calculate_wind_chill,
    # Prevent WINDDIR being converted by GLOB_WIND:
    DATA_POINT_WINDDIR: calculate_noop,
}

# Map which data points tend to come with keys embedded at their end:
UNIT_SUFFIX_MAP = {
    DATA_POINT_GLOB_BAROM: "in",
    DATA_POINT_GLOB_GUST: "mph",
    DATA_POINT_GLOB_RAIN: "in",
    DATA_POINT_GLOB_TEMP: "f",
    DATA_POINT_GLOB_WIND: "mph",
}

DEW_POINT_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY)
FEELS_LIKE_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY, DATA_POINT_WINDSPEEDMPH)
HEAT_INDEX_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY)
WIND_CHILL_KEYS = (DATA_POINT_TEMPF, DATA_POINT_WINDSPEEDMPH)
ILLUMINANCE_KEYS = (DATA_POINT_SOLARRADIATION,)

T = TypeVar("T")


def get_calculator_function(
    ecowitt: Ecowitt, key: str
) -> Callable[..., CalculatedDataPoint] | None:
    """Get a data calculator function for a particular data key (if it exists)."""
    if (data_type := get_data_point_from_key(key)) is None:
        return None
    return CALCULATOR_FUNCTION_MAP[data_type]


def get_data_point_from_key(key: str) -> str | None:
    """Get the data point "type" (if it exists) for a specific data key.

    1. If there is a data type that equals the provided key, use it.
    2. If there is a data glob that contains the provided key, use it.
    3. Return None.
    """
    if key in CALCULATOR_FUNCTION_MAP:
        return key

    try:
        [match] = [k for k in CALCULATOR_FUNCTION_MAP if k in key]
    except ValueError:
        return None

    return match


def get_typed_value(value: T) -> float | T:
    """Take a string and return its properly typed counterpart (if possible)."""
    try:
        return float(value)  # type: ignore[arg-type]
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("Couldn' convert value to number: %s", value)
        LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))
        return value


def remove_unit_from_key(key: str) -> str:
    """Remove a unit from the end of a key."""
    data_point = get_data_point_from_key(key)

    if not data_point:
        return key

    if (suffix := UNIT_SUFFIX_MAP.get(data_point)) is None or not key.endswith(suffix):
        # Return the key as-is if:
        #   1. This isn't a key we're monitoring.
        #   2. The key doesn't end with the unit.
        return key

    suffix_length = len(suffix)
    return key[:-suffix_length]


@dataclass(frozen=True)
class ProcessedData:
    """Define a processed data payload."""

    ecowitt: Ecowitt
    data: dict[str, Any]
    device: Device = field(init=False)
    output: dict[str, CalculatedDataPoint] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize."""
        object.__setattr__(self, "device", get_device_from_raw_payload(self.data))

        # Process all of the data points for which raw data was provided:
        for target_key, target_value in self.data.items():
            if target_key in DEFAULT_KEYS_TO_IGNORE or not target_value:
                continue

            key = remove_unit_from_key(target_key)
            value = get_typed_value(target_value)

            if calc := get_calculator_function(self.ecowitt, target_key):
                self.output[key] = calc(self.ecowitt, value=value)
            else:
                self.output[key] = CalculatedDataPoint(value, None)

        # Process any from-scratch data points that can be calculated from others:
        for target_key, input_keys in (
            (DATA_POINT_DEWPOINT, DEW_POINT_KEYS),
            (DATA_POINT_FEELSLIKE, FEELS_LIKE_KEYS),
            (DATA_POINT_HEATINDEX, HEAT_INDEX_KEYS),
            (DATA_POINT_SOLARRADIATION_LUX, ILLUMINANCE_KEYS),
            (DATA_POINT_SOLARRADIATION_PERCEIVED, ILLUMINANCE_KEYS),
            (DATA_POINT_WINDCHILL, WIND_CHILL_KEYS),
        ):
            if not all(k in self.data for k in input_keys):
                continue

            if calc := get_calculator_function(self.ecowitt, target_key):
                self.output[target_key] = calc(
                    self.ecowitt,
                    **{
                        remove_unit_from_key(key): get_typed_value(self.data[key])
                        for key in input_keys
                    },
                )
