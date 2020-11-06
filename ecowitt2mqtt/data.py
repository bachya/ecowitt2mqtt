"""Define helpers to process data from an Ecowitt device."""
from typing import Optional

import meteocalc

from ecowitt2mqtt.const import (
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKEF,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HUMIDITY,
    DATA_POINT_TEMPF,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDSPEEDMPH,
    LOGGER,
)

DEFAULT_UNIQUE_ID = "default"

KEYS_TO_IGNORE = ["dateutc", "freq", "model", "stationtype"]


class DataProcessor:  # pylint: disable=too-few-public-methods
    """Define an object to process Ecowitt data."""

    def __init__(self, data: dict) -> None:
        """Initialize."""
        self._data = {k: v for k, v in data.items() if k not in KEYS_TO_IGNORE}
        self.unique_id = data.pop("PASSKEY", DEFAULT_UNIQUE_ID)

    @property
    def _dew_point_obj(self) -> Optional[meteocalc.Temp]:
        """Return the dew point meteocalc object (if it exists)."""
        if not self._temperature_obj or not self.humidity:
            return None
        return meteocalc.dew_point(self._temperature_obj, self.humidity)

    @property
    def _feels_like_obj(self) -> Optional[meteocalc.Temp]:
        """Return the "feels like" meteocalc object (if it exists)."""
        if not self._temperature_obj or not self.humidity or not self.wind_speed:
            return None
        return meteocalc.feels_like(
            self._temperature_obj, self.humidity, self.wind_speed
        )

    @property
    def _heat_index_obj(self) -> Optional[meteocalc.Temp]:
        """Return the heat index meteocalc object (if it exists)."""
        if not self._temperature_obj or not self.humidity:
            return None
        return meteocalc.heat_index(self._temperature_obj, self.humidity)

    @property
    def _temperature_obj(self) -> Optional[meteocalc.Temp]:
        """Return the temperature meteocalc object (if it exists)."""
        if DATA_POINT_TEMPF not in self._data:
            return None
        return meteocalc.Temp(self._data[DATA_POINT_TEMPF], "f")

    @property
    def _wind_chill_obj(self) -> Optional[meteocalc.Temp]:
        """Return the wind chill (if it exists)."""
        if not self._temperature_obj or not self.wind_speed:
            return None

        try:
            return meteocalc.wind_chill(self._temperature_obj, self.wind_speed)
        except ValueError as err:
            LOGGER.debug(
                "%s (temperature: %s, wind speed: %s)",
                err,
                self._temperature_obj,
                self.wind_speed,
            )
            return None

    @property
    def dew_point(self) -> Optional[int]:
        """Return the dew point (if it exists)."""
        if not self._dew_point_obj:
            return None
        return self._dew_point_obj.f

    @property
    def feels_like(self) -> Optional[int]:
        """Return the "feels like" temperature (if it exists)."""
        if not self._feels_like_obj:
            return None
        return self._feels_like_obj.f

    @property
    def heat_index(self) -> Optional[int]:
        """Return the heat index (if it exists)."""
        if not self._heat_index_obj:
            return None
        return self._heat_index_obj.f

    @property
    def humidity(self) -> Optional[int]:
        """Return the humidity percentage (if it exists)."""
        if DATA_POINT_HUMIDITY not in self._data:
            return None
        return round(float(self._data[DATA_POINT_HUMIDITY]))

    @property
    def wind_chill(self) -> Optional[int]:
        """Return the wind chill (if it exists)."""
        if not self._wind_chill_obj:
            return None
        return self._wind_chill_obj.f

    @property
    def wind_speed(self) -> Optional[float]:
        """Return the wind speed (if it exists)."""
        if DATA_POINT_WINDSPEEDMPH not in self._data:
            return None
        return round(float(self._data[DATA_POINT_WINDSPEEDMPH]))

    @property
    def data(self) -> dict:
        """Return the data payload (original + calculated values)."""
        return {
            **self._data,
            **{
                DATA_POINT_DEWPOINT: self.dew_point,
                DATA_POINT_HEATINDEX: self.heat_index,
                DATA_POINT_WINDCHILL: self.wind_chill,
                DATA_POINT_FEELSLIKEF: self.feels_like,
            },
        }
