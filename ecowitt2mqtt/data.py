"""Define helpers to process data from an Ecowitt device."""
from dataclasses import dataclass, field
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


@dataclass(frozen=True)
class DataProcessor:  # pylint: disable=too-many-instance-attributes
    """Define a dataclass that holds processed payload data from the device."""

    _input: dict = field(repr=False)
    _data: dict = field(init=False, repr=False)

    _dew_point_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _feels_like_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _heat_index_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _humidity: Optional[int] = field(default=None, repr=False)
    _temperature_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _wind_chill_obj: Optional[meteocalc.Temp] = field(default=None, repr=False)
    _wind_speed: Optional[float] = field(default=None, repr=False)

    unique_id: str = field(init=False)
    generated_data: dict = field(init=False)

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

        # Calculate the final data payload:
        generated_data = {**self._data}
        for key, obj_property in [
            (DATA_POINT_DEWPOINT, self._dew_point_obj),
            (DATA_POINT_FEELSLIKEF, self._feels_like_obj),
            (DATA_POINT_HEATINDEX, self._heat_index_obj),
            (DATA_POINT_WINDCHILL, self._wind_chill_obj),
        ]:
            if obj_property:
                generated_data[key] = obj_property.f
            else:
                generated_data[key] = None

        object.__setattr__(self, "generated_data", generated_data)
