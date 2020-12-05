"""Define helpers to process data from an Ecowitt device."""
from dataclasses import dataclass, field
from typing import Optional

import meteocalc

from ecowitt2mqtt.const import (
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKEF,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HUMIDITY,
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
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDSPEEDMPH,
    LOGGER,
    UNIT_SYSTEM_METRIC,
)

DEFAULT_UNIQUE_ID = "default"

KEYS_TO_IGNORE = ["dateutc", "freq", "model", "stationtype"]


@dataclass(frozen=True)
class DataProcessor:  # pylint: disable=too-many-instance-attributes
    """Define a dataclass that holds processed payload data from the device."""

    _input: dict = field(repr=False)
    _unit_system: str = field(repr=False)

    _dew_point_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _feels_like_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _heat_index_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _humidity: Optional[int] = field(default=None, repr=False)
    _temperature_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _wind_chill_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _wind_speed: Optional[float] = field(default=None, repr=False)

    _data: dict = field(init=False, repr=False)
    unique_id: str = field(init=False)

    def __post_init__(self):
        """Set up some additional attributes from passed-in data."""
        object.__setattr__(
            self, "unique_id", self._input.pop("PASSKEY", DEFAULT_UNIQUE_ID)
        )

        # Only store data keys that we explicitly care about:
        object.__setattr__(
            self,
            "_data",
            {k: v for k, v in self._input.items() if k not in KEYS_TO_IGNORE},
        )

        # Determine properties necessary for the calculated properties:
        if DATA_POINT_TEMPF in self._data:
            object.__setattr__(
                self,
                "_temperature_obj",
                meteocalc.Temp(self._data[DATA_POINT_TEMPF], "f"),
            )
        if DATA_POINT_HUMIDITY in self._data:
            object.__setattr__(
                self, "_humidity", round(float(self._data[DATA_POINT_HUMIDITY]))
            )
        if DATA_POINT_WINDSPEEDMPH in self._data:
            object.__setattr__(
                self, "_wind_speed", round(float(self._data[DATA_POINT_WINDSPEEDMPH]))
            )

        # Determine calculated properties:
        if self._temperature_obj and self._humidity:
            object.__setattr__(
                self,
                "_dew_point_obj",
                meteocalc.dew_point(self._temperature_obj, self._humidity),
            )
            object.__setattr__(
                self,
                "_heat_index_obj",
                meteocalc.heat_index(self._temperature_obj, self._humidity),
            )
        if self._temperature_obj and self._wind_speed:
            if self._humidity:
                object.__setattr__(
                    self,
                    "_feels_like_obj",
                    meteocalc.feels_like(
                        self._temperature_obj, self._humidity, self._wind_speed
                    ),
                )

            try:
                object.__setattr__(
                    self,
                    "_wind_chill_obj",
                    meteocalc.wind_chill(self._temperature_obj, self._wind_speed),
                )
            except ValueError as err:
                LOGGER.debug(
                    "%s (temperature: %s, wind speed: %s)",
                    err,
                    self._temperature_obj,
                    self._wind_speed,
                )

    def _generate_temperature_data(self) -> dict:
        """Return temperature data."""
        data = {}

        # Outdoor temperature (which we've already calculated):
        if self._temperature_obj:
            if self._unit_system == UNIT_SYSTEM_METRIC:
                self._data.pop(DATA_POINT_TEMPF)
                data[DATA_POINT_TEMP] = round(self._temperature_obj.c, 1)
            else:
                data[DATA_POINT_TEMP] = round(self._temperature_obj.f, 1)

        # Provided temperatures:
        for original_key, new_key in [
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
            (DATA_POINT_TEMPINF, DATA_POINT_TEMPIN),
        ]:
            if original_key not in self._data:
                continue

            temp_obj = meteocalc.Temp(self._data[original_key], "f")

            if self._unit_system == UNIT_SYSTEM_METRIC:
                data[new_key] = round(temp_obj.c, 1)
            else:
                data[new_key] = round(temp_obj.f, 1)

        # Calculated temperatures:
        for key, obj_property in [
            (DATA_POINT_DEWPOINT, self._dew_point_obj),
            (DATA_POINT_FEELSLIKEF, self._feels_like_obj),
            (DATA_POINT_HEATINDEX, self._heat_index_obj),
            (DATA_POINT_WINDCHILL, self._wind_chill_obj),
        ]:
            if obj_property:
                if self._unit_system == UNIT_SYSTEM_METRIC:
                    data[key] = round(obj_property.c, 1)
                else:
                    data[key] = round(obj_property.f, 1)
            else:
                data[key] = None

        return data

    def generate_data(self) -> dict:
        """Return the final data payload."""
        temperature_data = self._generate_temperature_data()

        # Clean out any existing old keys that we have better data for:
        for key in [
            DATA_POINT_SOILTEMP10F,
            DATA_POINT_SOILTEMP1F,
            DATA_POINT_SOILTEMP2F,
            DATA_POINT_SOILTEMP3F,
            DATA_POINT_SOILTEMP4F,
            DATA_POINT_SOILTEMP5F,
            DATA_POINT_SOILTEMP6F,
            DATA_POINT_SOILTEMP7F,
            DATA_POINT_SOILTEMP8F,
            DATA_POINT_SOILTEMP9F,
            DATA_POINT_TEMP10F,
            DATA_POINT_TEMP1F,
            DATA_POINT_TEMP2F,
            DATA_POINT_TEMP3F,
            DATA_POINT_TEMP4F,
            DATA_POINT_TEMP5F,
            DATA_POINT_TEMP6F,
            DATA_POINT_TEMP7F,
            DATA_POINT_TEMP8F,
            DATA_POINT_TEMP9F,
            DATA_POINT_TEMPINF,
        ]:
            self._data.pop(key, None)

        return {**self._data, **temperature_data}
