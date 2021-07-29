"""Define helpers to process data from an Ecowitt device."""
from typing import Any, Dict, List, Tuple, Union, cast

from ecowitt2mqtt.const import (
    DATA_POINT_24HOURRAIN,
    DATA_POINT_24HOURRAININ,
    DATA_POINT_BAROMABS,
    DATA_POINT_BAROMABSIN,
    DATA_POINT_BAROMREL,
    DATA_POINT_BAROMRELIN,
    DATA_POINT_DAILYRAIN,
    DATA_POINT_DAILYRAININ,
    DATA_POINT_DEWPOINT,
    DATA_POINT_EVENTRAIN,
    DATA_POINT_EVENTRAININ,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HOURLYRAIN,
    DATA_POINT_HOURLYRAININ,
    DATA_POINT_HUMIDITY,
    DATA_POINT_LASTRAIN,
    DATA_POINT_MAXDAILYGUST,
    DATA_POINT_MONTHLYRAIN,
    DATA_POINT_MONTHLYRAININ,
    DATA_POINT_RAINRATE,
    DATA_POINT_RAINRATEIN,
    DATA_POINT_SOILTEMP1,
    DATA_POINT_SOILTEMP1F,
    DATA_POINT_SOILTEMP2,
    DATA_POINT_SOILTEMP2F,
    DATA_POINT_SOILTEMP3,
    DATA_POINT_SOILTEMP3F,
    DATA_POINT_SOILTEMP4,
    DATA_POINT_SOILTEMP4F,
    DATA_POINT_SOILTEMP5,
    DATA_POINT_SOILTEMP5F,
    DATA_POINT_SOILTEMP6,
    DATA_POINT_SOILTEMP6F,
    DATA_POINT_SOILTEMP7,
    DATA_POINT_SOILTEMP7F,
    DATA_POINT_SOILTEMP8,
    DATA_POINT_SOILTEMP8F,
    DATA_POINT_SOILTEMP9,
    DATA_POINT_SOILTEMP9F,
    DATA_POINT_SOILTEMP10,
    DATA_POINT_SOILTEMP10F,
    DATA_POINT_TEMP,
    DATA_POINT_TEMP1,
    DATA_POINT_TEMP1F,
    DATA_POINT_TEMP2,
    DATA_POINT_TEMP2F,
    DATA_POINT_TEMP3,
    DATA_POINT_TEMP3F,
    DATA_POINT_TEMP4,
    DATA_POINT_TEMP4F,
    DATA_POINT_TEMP5,
    DATA_POINT_TEMP5F,
    DATA_POINT_TEMP6,
    DATA_POINT_TEMP6F,
    DATA_POINT_TEMP7,
    DATA_POINT_TEMP7F,
    DATA_POINT_TEMP8,
    DATA_POINT_TEMP8F,
    DATA_POINT_TEMP9,
    DATA_POINT_TEMP9F,
    DATA_POINT_TEMP10,
    DATA_POINT_TEMP10F,
    DATA_POINT_TEMPF,
    DATA_POINT_TEMPIN,
    DATA_POINT_TEMPINF,
    DATA_POINT_TOTALRAIN,
    DATA_POINT_TOTALRAININ,
    DATA_POINT_WEEKLYRAIN,
    DATA_POINT_WEEKLYRAININ,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDGUST,
    DATA_POINT_WINDGUSTMPH,
    DATA_POINT_WINDSPD_AVG2M,
    DATA_POINT_WINDSPD_AVG10M,
    DATA_POINT_WINDSPDMPH_AVG2M,
    DATA_POINT_WINDSPDMPH_AVG10M,
    DATA_POINT_WINDSPEED,
    DATA_POINT_WINDSPEEDMPH,
    DATA_POINT_YEARLYRAIN,
    DATA_POINT_YEARLYRAININ,
    LOGGER,
    UNIT_SYSTEM_IMPERIAL,
)
from ecowitt2mqtt.helpers.converter import Converter
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

    # Define key sets for translated data points:
    PRESSURE_KEYS: List[Tuple[str, str]] = [
        (DATA_POINT_BAROMABSIN, DATA_POINT_BAROMABS),
        (DATA_POINT_BAROMRELIN, DATA_POINT_BAROMREL),
    ]
    RAIN_KEYS: List[Tuple[str, str]] = [
        (DATA_POINT_24HOURRAININ, DATA_POINT_24HOURRAIN),
        (DATA_POINT_DAILYRAININ, DATA_POINT_DAILYRAIN),
        (DATA_POINT_EVENTRAININ, DATA_POINT_EVENTRAIN),
        (DATA_POINT_HOURLYRAININ, DATA_POINT_HOURLYRAIN),
        (DATA_POINT_LASTRAIN, DATA_POINT_LASTRAIN),
        (DATA_POINT_MONTHLYRAININ, DATA_POINT_MONTHLYRAIN),
        (DATA_POINT_RAINRATEIN, DATA_POINT_RAINRATE),
        (DATA_POINT_TOTALRAININ, DATA_POINT_TOTALRAIN),
        (DATA_POINT_WEEKLYRAININ, DATA_POINT_WEEKLYRAIN),
        (DATA_POINT_YEARLYRAININ, DATA_POINT_YEARLYRAIN),
    ]
    TEMPERATURE_KEYS: List[Tuple[str, str]] = [
        (DATA_POINT_SOILTEMP10F, DATA_POINT_SOILTEMP10),
        (DATA_POINT_SOILTEMP1F, DATA_POINT_SOILTEMP1),
        (DATA_POINT_SOILTEMP2F, DATA_POINT_SOILTEMP2),
        (DATA_POINT_SOILTEMP3F, DATA_POINT_SOILTEMP3),
        (DATA_POINT_SOILTEMP4F, DATA_POINT_SOILTEMP4),
        (DATA_POINT_SOILTEMP5F, DATA_POINT_SOILTEMP5),
        (DATA_POINT_SOILTEMP6F, DATA_POINT_SOILTEMP6),
        (DATA_POINT_SOILTEMP7F, DATA_POINT_SOILTEMP7),
        (DATA_POINT_SOILTEMP8F, DATA_POINT_SOILTEMP8),
        (DATA_POINT_SOILTEMP9F, DATA_POINT_SOILTEMP9),
        (DATA_POINT_TEMP10F, DATA_POINT_TEMP10),
        (DATA_POINT_TEMP1F, DATA_POINT_TEMP1),
        (DATA_POINT_TEMP2F, DATA_POINT_TEMP2),
        (DATA_POINT_TEMP3F, DATA_POINT_TEMP3),
        (DATA_POINT_TEMP4F, DATA_POINT_TEMP4),
        (DATA_POINT_TEMP5F, DATA_POINT_TEMP5),
        (DATA_POINT_TEMP6F, DATA_POINT_TEMP6),
        (DATA_POINT_TEMP7F, DATA_POINT_TEMP7),
        (DATA_POINT_TEMP8F, DATA_POINT_TEMP8),
        (DATA_POINT_TEMP9F, DATA_POINT_TEMP9),
        (DATA_POINT_TEMPF, DATA_POINT_TEMP),
        (DATA_POINT_TEMPINF, DATA_POINT_TEMPIN),
    ]
    WIND_SPEED_KEYS: List[Tuple[str, str]] = [
        (DATA_POINT_MAXDAILYGUST, DATA_POINT_MAXDAILYGUST),
        (DATA_POINT_WINDGUSTMPH, DATA_POINT_WINDGUST),
        (DATA_POINT_WINDSPDMPH_AVG10M, DATA_POINT_WINDSPD_AVG10M),
        (DATA_POINT_WINDSPDMPH_AVG2M, DATA_POINT_WINDSPD_AVG2M),
        (DATA_POINT_WINDSPEEDMPH, DATA_POINT_WINDSPEED),
    ]

    def __init__(
        self,
        payload: Dict[str, Any],
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        self._data = {}

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

    def _generate_calculated_data(self) -> Dict[str, Union[float, str]]:
        """Generate calculated data points (i.e., those that didn't exists before)."""
        data: Dict[str, Union[float, str]] = {}

        for converter_class, target_key, input_keys in [
            (DewPointConverter, DATA_POINT_DEWPOINT, self.DEW_POINT_KEYS),
            (FeelsLikeConverter, DATA_POINT_FEELSLIKE, self.FEELS_LIKE_KEYS),
            (HeatIndexConverter, DATA_POINT_HEATINDEX, self.HEAT_INDEX_KEYS),
            (WindChillConverter, DATA_POINT_WINDCHILL, self.WIND_CHILL_KEYS),
        ]:
            if not all(k in self._data for k in input_keys):
                continue

            if target_key == DATA_POINT_DEWPOINT:
                LOGGER.debug(
                    "Sending data: %s", [self._data[key] for key in input_keys]
                )

            converter = cast(
                Converter,
                converter_class(
                    *[self._data[key] for key in input_keys],
                    input_unit_system=self._input_unit_system,
                    output_unit_system=self._output_unit_system
                ),
            )
            data[target_key] = converter.parse()

        return data

    def _generate_translated_data(self) -> Dict[str, Union[float, str]]:
        """Generate a version of the original payload with translated data."""
        data: Dict[str, Union[float, str]] = {}

        for converter_class, input_keys in [
            (PressureConverter, self.PRESSURE_KEYS),
            (RainConverter, self.RAIN_KEYS),
            (TemperatureConverter, self.TEMPERATURE_KEYS),
            (WindSpeedConverter, self.WIND_SPEED_KEYS),
        ]:
            for old_key, new_key in input_keys:
                if old_key not in self._data:
                    continue

                value = self._data.pop(old_key)
                converter = cast(
                    Converter,
                    converter_class(
                        value,
                        input_unit_system=self._input_unit_system,
                        output_unit_system=self._output_unit_system,
                    ),
                )
                data[new_key] = converter.parse()

        return {**self._data, **data}

    def generate_data(self) -> Dict[str, Union[float, str]]:
        """Generate a parsed data payload."""
        calculated_data = self._generate_calculated_data()
        translated_data = self._generate_translated_data()
        return {**calculated_data, **translated_data}
