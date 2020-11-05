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


class DataProcessor:
    """Define an object to process Ecowitt data."""

    def __init__(self, data: dict) -> None:
        """Initialize."""
        self._data = {k: v for k, v in data.items() if k not in KEYS_TO_IGNORE}
        self.unique_id = data.pop("PASSKEY", DEFAULT_UNIQUE_ID)

    @property
    def data(self) -> dict:
        """Return the data payload."""
        return {
            **self._data,
            **{
                DATA_POINT_HUMIDITY: self.humidity,
                DATA_POINT_TEMPF: self.temperature_f,
                DATA_POINT_WINDSPEEDMPH: self.wind_speed,
                DATA_POINT_DEWPOINT: self.dew_point,
                DATA_POINT_HEATINDEX: self.heat_index,
                DATA_POINT_WINDCHILL: self.wind_chill,
                DATA_POINT_FEELSLIKEF: self.feels_like_f,
            },
        }

    @property
    def dew_point(self) -> Optional[float]:
        """Return the dew point in fahrenheit (if it exists)."""
        if not self.temperature_f or not self.humidity:
            return None

        dew_point = meteocalc.dew_point(self.temperature_f, self.humidity)
        return round(dew_point.f, 2)

    @property
    def feels_like_f(self) -> Optional[float]:
        """Return the "feels like" temperature in fahrenheit (if it exists)."""
        if not self.temperature_f or not self.humidity or not self.wind_speed:
            return None

        feels_like_f = meteocalc.feels_like(
            self.temperature_f, self.humidity, self.wind_speed
        )
        return round(feels_like_f.f, 2)

    @property
    def heat_index(self) -> Optional[float]:
        """Return the heat index in fahrenheit (if it exists)."""
        if not self.temperature_f or not self.humidity:
            return None

        heat_index = meteocalc.heat_index(self.temperature_f, self.humidity)
        return round(heat_index.f, 2)

    @property
    def humidity(self) -> Optional[int]:
        """Return the humidity percentage (if it exists)."""
        if DATA_POINT_HUMIDITY not in self._data:
            return None
        return round(float(self._data[DATA_POINT_HUMIDITY]))

    @property
    def temperature_f(self) -> Optional[float]:
        """Return the temperature in fahrenheit (if it exists)."""
        if DATA_POINT_TEMPF not in self._data:
            return None

        temperature = meteocalc.Temp(self._data[DATA_POINT_TEMPF], "f")
        return round(temperature.f, 2)

    @property
    def wind_chill(self) -> Optional[float]:
        """Return the wind chill (if it exists)."""
        if not self.temperature_f or not self.wind_speed:
            return None

        try:
            wind_chill = meteocalc.wind_chill(self.temperature_f, self.wind_speed)
        except ValueError as err:
            LOGGER.debug(
                "%s (temperature: %s, wind speed: %s)",
                err,
                self.temperature_f,
                self.wind_speed,
            )
            return None

        return round(wind_chill.f, 2)

    @property
    def wind_speed(self) -> Optional[float]:
        """Return the wind speed (if it exists)."""
        if DATA_POINT_WINDSPEEDMPH not in self._data:
            return None
        return round(float(self._data[DATA_POINT_WINDSPEEDMPH]))
