"""Define data processing."""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
import traceback
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from ecowitt2mqtt.const import (
    DATA_POINT_CO2,
    DATA_POINT_CO2_24H,
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_BATT,
    DATA_POINT_GLOB_GUST,
    DATA_POINT_GLOB_HUMIDITY,
    DATA_POINT_GLOB_MOISTURE,
    DATA_POINT_GLOB_PM10,
    DATA_POINT_GLOB_PM25,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_VOLT,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_GLOB_WINDDIR,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HUMI_CO2,
    DATA_POINT_HUMIDITY,
    DATA_POINT_LIGHTNING,
    DATA_POINT_LIGHTNING_NUM,
    DATA_POINT_LIGHTNING_TIME,
    DATA_POINT_RUNTIME,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_SOLARRADIATION_LUX,
    DATA_POINT_SOLARRADIATION_PERCEIVED,
    DATA_POINT_TEMPF,
    DATA_POINT_TF_CO2,
    DATA_POINT_UV,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDSPEEDMPH,
    LOGGER,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint
from ecowitt2mqtt.helpers.calculator.battery import calculate_battery
from ecowitt2mqtt.helpers.calculator.distance import calculate_distance
from ecowitt2mqtt.helpers.calculator.meteo import (
    calculate_co2,
    calculate_dew_point,
    calculate_feels_like,
    calculate_heat_index,
    calculate_humidity,
    calculate_lightning_strikes,
    calculate_moisture,
    calculate_pm10,
    calculate_pm25,
    calculate_pressure,
    calculate_rain_volume,
    calculate_solar_radiation_lux,
    calculate_solar_radiation_perceived,
    calculate_solar_radiation_wm2,
    calculate_temperature,
    calculate_uv_index,
    calculate_wind_chill,
    calculate_wind_dir,
    calculate_wind_speed,
)
from ecowitt2mqtt.helpers.calculator.time import (
    calculate_dt_from_epoch,
    calculate_runtime,
)
from ecowitt2mqtt.helpers.device import Device, get_device_from_raw_payload
from ecowitt2mqtt.util import glob_search

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

# Map which data calculator functions should apply to various data points:
CALCULATOR_FUNCTION_MAP: dict[str, Callable[..., CalculatedDataPoint]] = {
    DATA_POINT_CO2: calculate_co2,
    DATA_POINT_CO2_24H: calculate_co2,
    DATA_POINT_DEWPOINT: calculate_dew_point,
    DATA_POINT_FEELSLIKE: calculate_feels_like,
    DATA_POINT_GLOB_BAROM: calculate_pressure,
    DATA_POINT_GLOB_BATT: calculate_battery,
    DATA_POINT_GLOB_GUST: calculate_wind_speed,
    DATA_POINT_GLOB_HUMIDITY: calculate_humidity,
    DATA_POINT_GLOB_MOISTURE: calculate_moisture,
    DATA_POINT_GLOB_PM10: calculate_pm10,
    DATA_POINT_GLOB_PM25: calculate_pm25,
    DATA_POINT_GLOB_RAIN: calculate_rain_volume,
    DATA_POINT_GLOB_TEMP: calculate_temperature,
    DATA_POINT_GLOB_VOLT: calculate_battery,
    DATA_POINT_GLOB_WIND: calculate_wind_speed,
    DATA_POINT_GLOB_WINDDIR: calculate_wind_dir,
    DATA_POINT_HEATINDEX: calculate_heat_index,
    DATA_POINT_HUMI_CO2: calculate_humidity,
    DATA_POINT_LIGHTNING: calculate_distance,
    DATA_POINT_LIGHTNING_NUM: calculate_lightning_strikes,
    DATA_POINT_LIGHTNING_TIME: calculate_dt_from_epoch,
    DATA_POINT_RUNTIME: calculate_runtime,
    DATA_POINT_SOLARRADIATION: calculate_solar_radiation_wm2,
    DATA_POINT_SOLARRADIATION_LUX: calculate_solar_radiation_lux,
    DATA_POINT_SOLARRADIATION_PERCEIVED: calculate_solar_radiation_perceived,
    DATA_POINT_TF_CO2: calculate_temperature,
    DATA_POINT_UV: calculate_uv_index,
    DATA_POINT_WINDCHILL: calculate_wind_chill,
}

DEFAULT_KEYS_TO_IGNORE = [
    "PASSKEY",
    "dateutc",
    "freq",
    "model",
    "stationtype",
    "ws90_ver",
]

# Map which data points tend to come with keys embedded at their end:
UNIT_SUFFIX_MAP = {
    DATA_POINT_GLOB_BAROM: "in",
    DATA_POINT_GLOB_GUST: "mph",
    DATA_POINT_GLOB_RAIN: "in",
    DATA_POINT_GLOB_TEMP: "f",
    DATA_POINT_GLOB_WIND: "mph",
}

# Map calculated data points to the data points they depend on:
DEW_POINT_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY)
FEELS_LIKE_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY, DATA_POINT_WINDSPEEDMPH)
HEAT_INDEX_KEYS = (DATA_POINT_TEMPF, DATA_POINT_HUMIDITY)
WIND_CHILL_KEYS = (DATA_POINT_TEMPF, DATA_POINT_WINDSPEEDMPH)
ILLUMINANCE_KEYS = (DATA_POINT_SOLARRADIATION,)

T = TypeVar("T")


def get_calculator_function(
    ecowitt: Ecowitt, key: str
) -> partial[CalculatedDataPoint] | None:
    """Get a data calculator function for a particular data key (if it exists)."""
    if (data_point := get_data_point_from_key(key)) is None:
        return None
    return partial(CALCULATOR_FUNCTION_MAP[data_point], ecowitt, key, data_point)


def get_data_point_from_key(key: str) -> str | None:
    """Get a data point from a key."""
    return glob_search(CALCULATOR_FUNCTION_MAP, key)


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
    if (data_point := get_data_point_from_key(key)) is None:
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
        for payload_key, payload_value in self.data.items():
            if payload_key in DEFAULT_KEYS_TO_IGNORE or not payload_value:
                continue

            key = remove_unit_from_key(payload_key)
            value = get_typed_value(payload_value)

            if calculator := get_calculator_function(self.ecowitt, payload_key):
                LOGGER.debug(
                    "Calculator found for %s: %s (key: %s, value: %s)",
                    payload_key,
                    calculator.func.__name__,
                    key,
                    value,
                )
                self.output[key] = calculator(value=value)
            else:
                LOGGER.debug("No calculator found for %s", payload_key)
                self.output[key] = CalculatedDataPoint(data_point_key=key, value=value)

        # Process any from-scratch data points that can be calculated from others:
        for payload_key, input_keys in (
            (DATA_POINT_DEWPOINT, DEW_POINT_KEYS),
            (DATA_POINT_FEELSLIKE, FEELS_LIKE_KEYS),
            (DATA_POINT_HEATINDEX, HEAT_INDEX_KEYS),
            (DATA_POINT_SOLARRADIATION_LUX, ILLUMINANCE_KEYS),
            (DATA_POINT_SOLARRADIATION_PERCEIVED, ILLUMINANCE_KEYS),
            (DATA_POINT_WINDCHILL, WIND_CHILL_KEYS),
        ):
            if not all(k in self.data for k in input_keys):
                continue

            if calculator := get_calculator_function(self.ecowitt, payload_key):
                self.output[payload_key] = calculator(
                    **{
                        remove_unit_from_key(key): get_typed_value(self.data[key])
                        for key in input_keys
                    },
                )
