"""Define helpers to process data from an Ecowitt device."""
from typing import Any, Dict, List, Optional, Type

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
    DATA_POINT_TEMPF,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDSPEEDMPH,
    UNIT_SYSTEM_IMPERIAL,
)
from ecowitt2mqtt.helpers.converter import Converter
from ecowitt2mqtt.helpers.converter.battery import BinaryBatteryConverter
from ecowitt2mqtt.helpers.converter.meteo import (
    DewPointConverter,
    FeelsLikeConverter,
    HeatIndexConverter,
    PressureConverter,
    RainConverter,
    TemperatureConverter,
    WindChillConverter,
    WindSpeedConverter,
)

DEFAULT_KEYS_TO_IGNORE = ["PASSKEY", "dateutc", "freq", "model", "stationtype"]
DEFAULT_UNIQUE_ID = "default"


def get_converter_class(key: str) -> Optional[Type[Converter]]:
    """Get the proper converter class for a key."""
    converter: Optional[Type[Converter]] = None
    if DATA_POINT_DEWPOINT in key:
        converter = DewPointConverter
    if DATA_POINT_FEELSLIKE in key:
        converter = FeelsLikeConverter
    if DATA_POINT_GLOB_BAROM in key:
        converter = PressureConverter
    if DATA_POINT_GLOB_BATT in key:
        converter = BinaryBatteryConverter
    if DATA_POINT_GLOB_RAIN in key:
        converter = RainConverter
    if DATA_POINT_GLOB_TEMP in key:
        converter = TemperatureConverter
    if DATA_POINT_GLOB_WIND in key:
        converter = WindSpeedConverter
    if DATA_POINT_HEATINDEX in key:
        converter = HeatIndexConverter
    if DATA_POINT_WINDCHILL in key:
        converter = WindChillConverter
    return converter


def de_unit_key(key: str) -> str:
    """Remove the unit from a key."""
    if key.endswith("f"):
        return key[:-1]
    if key.endswith("in"):
        return key[:-2]
    if key.endswith("mph"):
        return key[:-3]
    return key


class DataProcessor:  # pylint: disable=too-few-public-methods
    """Define an object that holds processed payload data from the device."""

    # Define key sets for calculated data points.
    # NOTE: these are lists because the order of the data points matters!
    DEW_POINT_KEYS: List[str] = [DATA_POINT_TEMPF, DATA_POINT_HUMIDITY]
    FEELS_LIKE_KEYS: List[str] = [
        DATA_POINT_TEMPF,
        DATA_POINT_HUMIDITY,
        DATA_POINT_WINDSPEEDMPH,
    ]
    HEAT_INDEX_KEYS: List[str] = [DATA_POINT_TEMPF, DATA_POINT_HUMIDITY]
    WIND_CHILL_KEYS: List[str] = [DATA_POINT_TEMPF, DATA_POINT_WINDSPEEDMPH]

    def __init__(
        self,
        payload: Dict[str, Any],
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        self._data: Dict[str, Any] = {}

        for key, value in payload.items():
            if key in DEFAULT_KEYS_TO_IGNORE:
                continue
            try:
                self._data[key] = float(value)
            except ValueError:
                self._data[key] = value

        self._input_unit_system = input_unit_system
        self._output_unit_system = output_unit_system
        self.unique_id = payload.get("PASSKEY", DEFAULT_UNIQUE_ID)

    def generate_data(self) -> Dict[str, Any]:
        """Generate a parsed data payload."""
        translated_data: Dict[str, Any] = {}
        for key, value in self._data.items():
            converter_class = get_converter_class(key)

            if converter_class:
                converter = converter_class(  # type: ignore
                    value,
                    input_unit_system=self._input_unit_system,
                    output_unit_system=self._output_unit_system,
                )
                target_key = de_unit_key(key)
                translated_data[target_key] = converter.parse()
            else:
                translated_data[key] = value

        calculated_data: Dict[str, Any] = {}
        for target_key, input_keys in [
            (DATA_POINT_DEWPOINT, self.DEW_POINT_KEYS),
            (DATA_POINT_FEELSLIKE, self.FEELS_LIKE_KEYS),
            (DATA_POINT_HEATINDEX, self.HEAT_INDEX_KEYS),
            (DATA_POINT_WINDCHILL, self.WIND_CHILL_KEYS),
        ]:
            if not all(k in self._data for k in input_keys):
                continue

            converter_class = get_converter_class(target_key)

            if converter_class:
                converter = converter_class(
                    *[self._data[key] for key in input_keys],
                    input_unit_system=self._input_unit_system,
                    output_unit_system=self._output_unit_system
                )
                calculated_data[target_key] = converter.parse()

        return {**translated_data, **calculated_data}
