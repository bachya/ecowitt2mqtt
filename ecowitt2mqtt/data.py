"""Define data processing."""
from __future__ import annotations

from functools import partial
import inspect
from typing import TYPE_CHECKING, Any, Callable

from ecowitt2mqtt.const import (
    CONF_INPUT_UNIT_SYSTEM,
    CONF_OUTPUT_UNIT_SYSTEM,
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
    UNIT_SYSTEM_METRIC,
)
from ecowitt2mqtt.helpers.typing import DataValueType
from ecowitt2mqtt.util.calculator import calculate_noop
from ecowitt2mqtt.util.calculator.distance import calculate_distance
from ecowitt2mqtt.util.calculator.meteo import (
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
from ecowitt2mqtt.util.calculator.time import calculate_dt_from_epoch

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_KEYS_TO_IGNORE = ["PASSKEY", "dateutc", "freq", "model", "stationtype"]

# Map which data calculator functions should apply to various data points:
CALCULATOR_FUNCTION_MAP: dict[str, Callable[..., DataValueType]] = {
    DATA_POINT_DEWPOINT: calculate_dew_point,
    DATA_POINT_FEELSLIKE: calculate_feels_like,
    DATA_POINT_GLOB_BAROM: calculate_pressure,
    # DATA_POINT_GLOB_BATT: calculate_battery,
    DATA_POINT_GLOB_RAIN: calculate_rain_volume,
    DATA_POINT_GLOB_TEMP: calculate_temperature,
    DATA_POINT_GLOB_WIND: calculate_wind_speed,
    DATA_POINT_HEATINDEX: calculate_heat_index,
    # Lightning strike distance always gives values in metric:
    DATA_POINT_LIGHTNING: lambda val: calculate_distance(
        val, input_unit_system=UNIT_SYSTEM_METRIC
    ),
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


def _get_calculator_function(
    ecowitt: Ecowitt, key: str, *args: float | str, **kwargs: str
) -> Callable[..., DataValueType] | None:
    """Get a data calculator function for a particular data key (if it exists)."""
    data_type = _get_data_point(key)

    if not data_type:
        return None

    func = CALCULATOR_FUNCTION_MAP[data_type]

    func_params = inspect.signature(func).parameters
    if CONF_INPUT_UNIT_SYSTEM in func_params:
        kwargs[CONF_INPUT_UNIT_SYSTEM] = ecowitt.config.input_unit_system
    if CONF_OUTPUT_UNIT_SYSTEM in func_params:
        kwargs[CONF_OUTPUT_UNIT_SYSTEM] = ecowitt.config.output_unit_system

    return partial(func, *args, **kwargs)


def _get_data_point(key: str) -> str | None:
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


def _get_typed_value(value: str) -> float:
    """Take a string and return its properly typed counterpart."""
    return float(value)


def _remove_unit_from_key(key: str) -> str:
    """Remove a unit from the end of a key."""
    data_point = _get_data_point(key)

    if not data_point:
        return key

    if (suffix := UNIT_SUFFIX_MAP.get(data_point)) is None or not key.endswith(suffix):
        # Return the key as-is if:
        #   1. This isn't a key we're monitoring.
        #   2. The key doesn't end with the unit.
        return key

    suffix_length = len(suffix)
    return key[:-suffix_length]


def process_data(ecowitt: Ecowitt, data: dict[str, Any]) -> dict[str, Any]:
    """Return processed data."""
    processed_data: dict[str, DataValueType] = {}

    # Process all of the data points for which raw data was provided:
    for target_key, target_value in data.items():
        if target_key in DEFAULT_KEYS_TO_IGNORE or not target_value:
            continue

        key = _remove_unit_from_key(target_key)
        value = _get_typed_value(target_value)

        if (
            ecowitt.config.raw_data
            or (calc := _get_calculator_function(ecowitt, target_key, value)) is None
        ):
            processed_data[key] = value
        else:
            processed_data[key] = calc()

    # Process any from-scratch data points that can be calculated from others:
    for target_key, input_keys in (
        (DATA_POINT_DEWPOINT, DEW_POINT_KEYS),
        (DATA_POINT_FEELSLIKE, FEELS_LIKE_KEYS),
        (DATA_POINT_HEATINDEX, HEAT_INDEX_KEYS),
        (DATA_POINT_SOLARRADIATION_LUX, ILLUMINANCE_KEYS),
        (DATA_POINT_SOLARRADIATION_PERCEIVED, ILLUMINANCE_KEYS),
        (DATA_POINT_WINDCHILL, WIND_CHILL_KEYS),
    ):
        if not all(k in data for k in input_keys):
            continue

        calc = _get_calculator_function(
            ecowitt, target_key, *[_get_typed_value(data[k]) for k in input_keys]
        )
        # We know that calculated data points will always have a calculator:
        assert calc

        processed_data[target_key] = calc()

    return processed_data
