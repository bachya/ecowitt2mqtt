"""Define helpers to process data from an Ecowitt device."""
import argparse
from functools import partial
import inspect
from typing import Any, Callable, Dict, Optional, Union

from ecowitt2mqtt.const import (
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_BATT,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HUMIDITY,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_SOLARRADIATION_LUX,
    DATA_POINT_SOLARRADIATION_PERCEIVED,
    DATA_POINT_TEMPF,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDSPEEDMPH,
)
from ecowitt2mqtt.device import get_device_from_raw_payload
from ecowitt2mqtt.util.battery import calculate_battery
from ecowitt2mqtt.util.meteo import (
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

DEFAULT_KEYS_TO_IGNORE = ["PASSKEY", "dateutc", "freq", "model", "stationtype"]

CALCULATOR_FUNCTION_MAP: Dict[str, Callable] = {
    DATA_POINT_DEWPOINT: calculate_dew_point,
    DATA_POINT_FEELSLIKE: calculate_feels_like,
    DATA_POINT_GLOB_BAROM: calculate_pressure,
    DATA_POINT_GLOB_BATT: calculate_battery,
    DATA_POINT_GLOB_RAIN: calculate_rain_volume,
    DATA_POINT_GLOB_TEMP: calculate_temperature,
    DATA_POINT_GLOB_WIND: calculate_wind_speed,
    DATA_POINT_HEATINDEX: calculate_heat_index,
    DATA_POINT_SOLARRADIATION_LUX: calculate_illuminance_wm2_to_lux,
    DATA_POINT_SOLARRADIATION_PERCEIVED: calculate_illuminance_wm2_to_perceived,
    DATA_POINT_WINDCHILL: calculate_wind_chill,
}

DEW_POINT_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY)
FEELS_LIKE_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY, DATA_POINT_WINDSPEEDMPH)
HEAT_INDEX_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY)
WIND_CHILL_KEYS = (DATA_POINT_TEMPF, DATA_POINT_WINDSPEEDMPH)
ILLUMINANCE_KEYS = (DATA_POINT_SOLARRADIATION,)


def de_unit_key(key: str) -> str:
    """Remove the unit from a key."""
    if key.endswith("f"):
        return key[:-1]
    if key.endswith("in"):
        return key[:-2]
    if key.endswith("mph"):
        return key[:-3]
    return key


def get_data_type(key: str) -> Optional[str]:
    """Get the data "type" (if it exists) for a specific data key."""
    if key in CALCULATOR_FUNCTION_MAP:
        return key

    matches = [k for k in CALCULATOR_FUNCTION_MAP if k in key]
    if matches:
        return matches[0]

    return None


def get_typed_value(value: str) -> Union[float, int, str]:
    """Take a string and return its properly typed counterpart."""
    if value.isdigit():
        # Integer:
        return int(value)

    try:
        # Float:
        return float(value)
    except ValueError:
        # String:
        return value


class DataProcessor:  # pylint: disable=too-few-public-methods
    """Define an object that holds processed payload data from the device."""

    def __init__(self, payload: Dict[str, Any], args: argparse.Namespace) -> None:
        """Initialize."""
        self._args = args
        self._input_unit_system = args.input_unit_system
        self._output_unit_system = args.output_unit_system

        self._payload: Dict[str, Union[float, str]] = {}
        for key, value in payload.items():
            self._payload[key] = get_typed_value(value)

        self.device = get_device_from_raw_payload(payload)

    def _get_calculator_func(
        self, key: str, *args: Union[float, str], **kwargs: str
    ) -> Optional[Callable]:
        """Get a data calculator function for a particular data key."""
        data_type = get_data_type(key)

        if not data_type:
            return None

        func = CALCULATOR_FUNCTION_MAP[data_type]

        func_params = inspect.signature(func).parameters
        if "input_unit_system" in func_params:
            kwargs["input_unit_system"] = self._input_unit_system
        if "output_unit_system" in func_params:
            kwargs["output_unit_system"] = self._output_unit_system

        return partial(func, *args, **kwargs)

    def generate_data(self) -> Dict[str, Union[float, str]]:
        """Generate a parsed data payload."""
        data: Dict[str, Any] = {}

        for target_key, value in self._payload.items():
            if target_key in DEFAULT_KEYS_TO_IGNORE:
                continue

            calculate = self._get_calculator_func(target_key, value)

            if self._args.raw_data or not calculate:
                data[target_key] = value
                continue

            output = calculate()
            target_key = de_unit_key(target_key)
            data[target_key] = output

        for target_key, input_keys in [
            (DATA_POINT_DEWPOINT, DEW_POINT_KEYS),
            (DATA_POINT_FEELSLIKE, FEELS_LIKE_KEYS),
            (DATA_POINT_HEATINDEX, HEAT_INDEX_KEYS),
            (DATA_POINT_SOLARRADIATION_LUX, ILLUMINANCE_KEYS),
            (DATA_POINT_SOLARRADIATION_PERCEIVED, ILLUMINANCE_KEYS),
            (DATA_POINT_WINDCHILL, WIND_CHILL_KEYS),
        ]:
            if not all(k in self._payload for k in input_keys):
                continue

            calculate = self._get_calculator_func(
                target_key, *[self._payload[k] for k in input_keys]
            )

            if not calculate:
                continue

            output = calculate()
            data[target_key] = output

        return data
