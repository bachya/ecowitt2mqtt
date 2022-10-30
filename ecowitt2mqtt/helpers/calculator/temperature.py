"""Define temperature calculators."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import cast

import meteocalc

from ecowitt2mqtt.const import (
    CONF_OUTPUT_UNIT_TEMPERATURE,
    DATA_POINT_HUMIDITY,
    DATA_POINT_TEMP,
    DATA_POINT_WINDSPEED,
    LOGGER,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, Calculator
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.meteo import (
    get_absolute_humidity_in_metric,
    get_dew_point_meteocalc_object,
    get_feels_like_meteocalc_object,
    get_frost_point_meteocalc_object,
    get_heat_index_meteocalc_object,
    get_simmer_index_meteocalc_object,
    get_temperature_meteocalc_object,
    get_wind_chill_meteocalc_object,
)
from ecowitt2mqtt.util.unit_conversion import TemperatureConverter

FROST_RISK_HUMIDITY_ABS_THRESHOLD = 2.8

IMPERIAL_HIGH_THRESHOLD = 110.0
IMPERIAL_LOW_THRESHOLD = -10.0


class FrostRisk(str, Enum):
    """Define types of frost risk."""

    NO_RISK = "No risk"
    PROBABLE = "Probable"
    UNLIKELY = "Unlikely"
    VERY_PROBABLE = "Very probable"


class SimmerZone(str, Enum):
    """Define types of simmer zone."""

    CAUTION_HEAT_EXHAUSTION = "Caution: Heat exhaustion"
    CIRCULATORY_COLLAPSE_IMMINENT = "Circulatory collapse imminent"
    COMFORTABLE = "Comfortable"
    DANGER_OF_HEATSTROKE = "Danger of heatstroke"
    EXTREME_DANGER_OF_HEATSTROKE = "Extreme danger of heatstroke"
    INCREASED_DISCOMFORT = "Increased discomfort"
    SLIGHTLY_COOL = "Slightly cool"
    SLIGHTLY_WARM = "Slightly warm"


@dataclass
class SimmerZoneRating:
    """Define a dataclass to store a simmer zone rating."""

    zone: SimmerZone
    minimum_f: float | None = None
    maximum_f: float | None = None


SIMMER_ZONE_RATINGS: list[SimmerZoneRating] = [
    SimmerZoneRating(
        zone=SimmerZone.SLIGHTLY_COOL,
        minimum_f=70.0,
        maximum_f=77.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.COMFORTABLE,
        minimum_f=77.0,
        maximum_f=83.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.SLIGHTLY_WARM,
        minimum_f=83.0,
        maximum_f=91.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.INCREASED_DISCOMFORT,
        minimum_f=91.0,
        maximum_f=100.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.CAUTION_HEAT_EXHAUSTION,
        minimum_f=100.0,
        maximum_f=112.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.DANGER_OF_HEATSTROKE,
        minimum_f=112.0,
        maximum_f=125.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.EXTREME_DANGER_OF_HEATSTROKE,
        minimum_f=125.0,
        maximum_f=150.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.CIRCULATORY_COLLAPSE_IMMINENT,
        minimum_f=150.0,
        maximum_f=200.0,
    ),
]


class ThermalPerception(str, Enum):
    """Define types of thermal perception."""

    COMFORTABLE = "Comfortable"
    DRY = "Dry"
    EXTREMELY_UNCOMFORTABLE = "Extremely uncomfortable"
    OK_BUT_HUMID = "OK for most"
    QUITE_UNCOMFORTABLE = "Quite uncomfortable"
    SEVERELY_HIGH = "Severely high"
    SOMEWHAT_UNCOMFORTABLE = "Somewhat uncomfortable"
    VERY_COMFORTABLE = "Very comfortable"


@dataclass
class ThermalPerceptionRating:
    """Define a dataclass to store a thermal perception rating."""

    perception: ThermalPerception
    minimum_c: float
    maximum_c: float


THERMAL_PERCEPTION_RATINGS: list[ThermalPerceptionRating] = [
    ThermalPerceptionRating(
        perception=ThermalPerception.SEVERELY_HIGH,
        minimum_c=26.0,
        maximum_c=100.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.EXTREMELY_UNCOMFORTABLE,
        minimum_c=24.0,
        maximum_c=26.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.QUITE_UNCOMFORTABLE,
        minimum_c=21.0,
        maximum_c=24.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.SOMEWHAT_UNCOMFORTABLE,
        minimum_c=18.0,
        maximum_c=21.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.OK_BUT_HUMID,
        minimum_c=16.0,
        maximum_c=18.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.COMFORTABLE,
        minimum_c=12.0,
        maximum_c=16.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.VERY_COMFORTABLE,
        minimum_c=10.0,
        maximum_c=12.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.DRY,
        minimum_c=-100.0,
        maximum_c=10.0,
    ),
]


class BaseTemperatureCalculator(Calculator):
    """Define a base temperature calculator."""

    DEFAULT_INPUT_UNIT = TEMP_FAHRENHEIT
    UNIT_OVERRIDE_CONFIG_OPTION = CONF_OUTPUT_UNIT_TEMPERATURE

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial).

        Returns:
            A unit string.
        """
        return TEMP_FAHRENHEIT

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric).

        Returns:
            A unit string.
        """
        return TEMP_CELSIUS


class DewPointCalculator(BaseTemperatureCalculator):
    """Define a dew point calculator."""

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])

        dew_point_obj = get_dew_point_meteocalc_object(
            temp, humidity, self._config.input_unit_system
        )

        return self.get_calculated_data_point(
            dew_point_obj.f, unit_converter=TemperatureConverter
        )


class FeelsLikeCalculator(BaseTemperatureCalculator):
    """Define a "feels like" calculator."""

    @Calculator.requires_keys(
        DATA_POINT_TEMP, DATA_POINT_HUMIDITY, DATA_POINT_WINDSPEED
    )
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])
        wind_speed = cast(float, payload[DATA_POINT_WINDSPEED])

        feels_like_obj = get_feels_like_meteocalc_object(
            temp, humidity, wind_speed, self._config.input_unit_system
        )

        return self.get_calculated_data_point(
            feels_like_obj.f, unit_converter=TemperatureConverter
        )


class FrostPointCalculator(BaseTemperatureCalculator):
    """Define a frost point calculator."""

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])

        temp_obj = get_temperature_meteocalc_object(
            temp, self._config.input_unit_system
        )
        frost_point_obj = get_frost_point_meteocalc_object(temp_obj, humidity)

        return self.get_calculated_data_point(
            frost_point_obj.f, unit_converter=TemperatureConverter
        )


class FrostRiskCalculator(Calculator):
    """Define a frost risk calculator."""

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])

        temp_obj = get_temperature_meteocalc_object(
            temp, self._config.input_unit_system
        )
        absolute_humidity = get_absolute_humidity_in_metric(temp_obj, humidity)
        frost_point_obj = get_frost_point_meteocalc_object(temp_obj, humidity)

        if temp_obj.c <= 1.0 and frost_point_obj.c <= 0:
            if absolute_humidity <= FROST_RISK_HUMIDITY_ABS_THRESHOLD:
                value = FrostRisk.UNLIKELY
            else:
                value = FrostRisk.VERY_PROBABLE
        elif (
            temp_obj.c <= 4.0
            and frost_point_obj.c <= 0.5
            and absolute_humidity > FROST_RISK_HUMIDITY_ABS_THRESHOLD
        ):
            value = FrostRisk.PROBABLE
        else:
            value = FrostRisk.NO_RISK

        return self.get_calculated_data_point(value)


class HeatIndexCalculator(BaseTemperatureCalculator):
    """Define a heat index calculator."""

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])

        heat_index_obj = get_heat_index_meteocalc_object(
            temp, humidity, self._config.input_unit_system
        )

        return self.get_calculated_data_point(
            heat_index_obj.f, unit_converter=TemperatureConverter
        )


class SimmerIndexCalculator(BaseTemperatureCalculator):
    """Define a simmer index calculator."""

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])

        temp_obj = get_temperature_meteocalc_object(
            temp, self._config.input_unit_system
        )
        try:
            simmer_obj = get_simmer_index_meteocalc_object(
                temp_obj, humidity, self._config.input_unit_system
            )
        except ValueError as err:
            LOGGER.debug("%s (temperature: %s)", err, temp_obj)
            return self.get_calculated_data_point(None)
        else:
            simmer_obj = cast(meteocalc.Temp, simmer_obj)

        return self.get_calculated_data_point(
            simmer_obj.f, unit_converter=TemperatureConverter
        )


class SimmerZoneCalculator(Calculator):
    """Define a simmer zone calculator."""

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])

        temp_obj = get_temperature_meteocalc_object(
            temp, self._config.input_unit_system
        )
        try:
            simmer_obj = get_simmer_index_meteocalc_object(
                temp_obj, humidity, self._config.input_unit_system
            )
        except ValueError as err:
            LOGGER.debug("%s (temperature: %s)", err, temp_obj)
            return self.get_calculated_data_point(None)
        else:
            simmer_obj = cast(meteocalc.Temp, simmer_obj)

        [rating] = [
            r for r in SIMMER_ZONE_RATINGS if r.minimum_f <= simmer_obj.f < r.maximum_f
        ]
        return self.get_calculated_data_point(rating.zone)


class TemperatureCalculator(BaseTemperatureCalculator):
    """Define a temperature calculator."""

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            value: calculated value.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        float_value = cast(float, value)

        temp_obj = get_temperature_meteocalc_object(
            float_value, self._config.input_unit_system
        )

        if temp_obj.f < IMPERIAL_LOW_THRESHOLD or temp_obj.f > IMPERIAL_HIGH_THRESHOLD:
            LOGGER.warning(
                'Value of "%s" (%s) with input unit system "%s" seems suspicious',
                self._payload_key,
                float_value,
                self._config.input_unit_system,
            )

        return self.get_calculated_data_point(
            temp_obj.f, unit_converter=TemperatureConverter
        )


class ThermalPerceptionCalculator(Calculator):
    """Define a thermal perception calculator."""

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])

        dew_point_obj = get_dew_point_meteocalc_object(
            temp, humidity, self._config.input_unit_system
        )

        [rating] = [
            r
            for r in THERMAL_PERCEPTION_RATINGS
            if r.minimum_c <= dew_point_obj.c < r.maximum_c
        ]
        return self.get_calculated_data_point(rating.perception)


class WindChillCalculator(BaseTemperatureCalculator):
    """Define a wind chill calculator."""

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_WINDSPEED)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        wind_speed = cast(float, payload[DATA_POINT_WINDSPEED])

        try:
            wind_chill_obj = get_wind_chill_meteocalc_object(
                temp, wind_speed, self._config.input_unit_system
            )
        except ValueError as err:
            LOGGER.debug(
                "%s (current temperature: %s, current wind speed: %s)",
                err,
                temp,
                wind_speed,
            )
            return self.get_calculated_data_point(None)

        return self.get_calculated_data_point(
            wind_chill_obj.f, unit_converter=TemperatureConverter
        )
