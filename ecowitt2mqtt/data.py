"""Define data processing."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import (
    DATA_POINT_BEAUFORT_SCALE,
    DATA_POINT_CO2,
    DATA_POINT_CO2_24H,
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_FROST_POINT,
    DATA_POINT_FROST_RISK,
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_BATT,
    DATA_POINT_GLOB_GAIN_PIEZO,
    DATA_POINT_GLOB_GUST,
    DATA_POINT_GLOB_HUMIDITY,
    DATA_POINT_GLOB_LEAK,
    DATA_POINT_GLOB_MOISTURE,
    DATA_POINT_GLOB_PM10,
    DATA_POINT_GLOB_PM25,
    DATA_POINT_GLOB_R_RAIN,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_RAIN_PIEZO,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_TF,
    DATA_POINT_GLOB_VOLT,
    DATA_POINT_GLOB_WETNESS,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_GLOB_WINDDIR,
    DATA_POINT_HEAP,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HUMI_CO2,
    DATA_POINT_HUMIDEX,
    DATA_POINT_HUMIDEX_PERCEPTION,
    DATA_POINT_HUMIDITY,
    DATA_POINT_HUMIDITY_ABS,
    DATA_POINT_HUMIDITY_ABS_IN,
    DATA_POINT_INTERVAL,
    DATA_POINT_LIGHTNING,
    DATA_POINT_LIGHTNING_NUM,
    DATA_POINT_LIGHTNING_TIME,
    DATA_POINT_R_RAIN_PIEZO,
    DATA_POINT_RAIN_RATE,
    DATA_POINT_RELATIVE_STRAIN_INDEX,
    DATA_POINT_RELATIVE_STRAIN_INDEX_PERCEPTION,
    DATA_POINT_RUNTIME,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6,
    DATA_POINT_SIMMER_INDEX,
    DATA_POINT_SIMMER_ZONE,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_SOLARRADIATION_PERCEIVED,
    DATA_POINT_TF_CO2,
    DATA_POINT_THERMAL_PERCEPTION,
    DATA_POINT_UV,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDDIR_NAME,
    LOGGER,
)
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    CalculationFailedError,
    CalculationKeysMissingError,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.calculator.battery import BatteryCalculator
from ecowitt2mqtt.helpers.calculator.heap import HeapCalculator
from ecowitt2mqtt.helpers.calculator.humidity import (
    AbsoluteHumidityCalculator,
    IndoorAbsoluteHumidityCalculator,
    RelativeHumidityCalculator,
)
from ecowitt2mqtt.helpers.calculator.illuminance import (
    IlluminanceCalculator,
    PerceivedIlluminanceCalculator,
)
from ecowitt2mqtt.helpers.calculator.leak import LeakCalculator
from ecowitt2mqtt.helpers.calculator.lightning import (
    LightningStrikeCountCalculator,
    LightningStrikeDistanceCalculator,
)
from ecowitt2mqtt.helpers.calculator.pollution import PollutantCalculator
from ecowitt2mqtt.helpers.calculator.precipitation import (
    AccumulatedPrecipitationCalculator,
    PrecipitationRateCalculator,
)
from ecowitt2mqtt.helpers.calculator.pressure import PressureCalculator
from ecowitt2mqtt.helpers.calculator.temperature import (
    DewPointCalculator,
    FeelsLikeCalculator,
    FrostPointCalculator,
    FrostRiskCalculator,
    HeatIndexCalculator,
    HumidexCalculator,
    HumidexPerceptionCalculator,
    RsiCalculator,
    RsiPerceptionCalculator,
    SimmerIndexCalculator,
    SimmerZoneCalculator,
    TemperatureCalculator,
    ThermalPerceptionCalculator,
    WindChillCalculator,
)
from ecowitt2mqtt.helpers.calculator.time import (
    EpochCalculator,
    RuntimeCalculator,
    UpdateIntervalCalculator,
)
from ecowitt2mqtt.helpers.calculator.uv import SafeExposureCalculator, UVIndexCalculator
from ecowitt2mqtt.helpers.calculator.wind import (
    BeaufortScaleCalculator,
    WindDirCalculator,
    WindDirNameCalculator,
    WindSpeedCalculator,
)
from ecowitt2mqtt.helpers.device import Device, get_device_from_raw_payload
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util import glob_search

CALCULATOR_MAP: dict[str, type[Calculator]] = {
    DATA_POINT_BEAUFORT_SCALE: BeaufortScaleCalculator,
    DATA_POINT_CO2: PollutantCalculator,
    DATA_POINT_CO2_24H: PollutantCalculator,
    DATA_POINT_DEWPOINT: DewPointCalculator,
    DATA_POINT_FEELSLIKE: FeelsLikeCalculator,
    DATA_POINT_FROST_POINT: FrostPointCalculator,
    DATA_POINT_FROST_RISK: FrostRiskCalculator,
    DATA_POINT_GLOB_BAROM: PressureCalculator,
    DATA_POINT_GLOB_BATT: BatteryCalculator,
    DATA_POINT_GLOB_GAIN_PIEZO: SimpleCalculator,
    DATA_POINT_GLOB_GUST: WindSpeedCalculator,
    DATA_POINT_GLOB_HUMIDITY: RelativeHumidityCalculator,
    DATA_POINT_GLOB_LEAK: LeakCalculator,
    DATA_POINT_GLOB_MOISTURE: RelativeHumidityCalculator,
    DATA_POINT_GLOB_PM10: PollutantCalculator,
    DATA_POINT_GLOB_PM25: PollutantCalculator,
    DATA_POINT_GLOB_RAIN: AccumulatedPrecipitationCalculator,
    DATA_POINT_GLOB_RAIN_PIEZO: AccumulatedPrecipitationCalculator,
    DATA_POINT_GLOB_R_RAIN: PrecipitationRateCalculator,
    DATA_POINT_GLOB_TEMP: TemperatureCalculator,
    DATA_POINT_GLOB_TF: TemperatureCalculator,
    DATA_POINT_GLOB_VOLT: BatteryCalculator,
    DATA_POINT_GLOB_WETNESS: RelativeHumidityCalculator,
    DATA_POINT_GLOB_WIND: WindSpeedCalculator,
    DATA_POINT_GLOB_WINDDIR: WindDirCalculator,
    DATA_POINT_HEAP: HeapCalculator,
    DATA_POINT_HEATINDEX: HeatIndexCalculator,
    DATA_POINT_HUMIDEX: HumidexCalculator,
    DATA_POINT_HUMIDEX_PERCEPTION: HumidexPerceptionCalculator,
    DATA_POINT_HUMIDITY: RelativeHumidityCalculator,
    DATA_POINT_HUMIDITY_ABS: AbsoluteHumidityCalculator,
    DATA_POINT_HUMIDITY_ABS_IN: IndoorAbsoluteHumidityCalculator,
    DATA_POINT_HUMI_CO2: RelativeHumidityCalculator,
    DATA_POINT_INTERVAL: UpdateIntervalCalculator,
    DATA_POINT_LIGHTNING: LightningStrikeDistanceCalculator,
    DATA_POINT_LIGHTNING_NUM: LightningStrikeCountCalculator,
    DATA_POINT_LIGHTNING_TIME: EpochCalculator,
    DATA_POINT_RAIN_RATE: PrecipitationRateCalculator,
    DATA_POINT_RELATIVE_STRAIN_INDEX: RsiCalculator,
    DATA_POINT_RELATIVE_STRAIN_INDEX_PERCEPTION: RsiPerceptionCalculator,
    DATA_POINT_RUNTIME: RuntimeCalculator,
    DATA_POINT_R_RAIN_PIEZO: PrecipitationRateCalculator,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1: SafeExposureCalculator,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2: SafeExposureCalculator,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3: SafeExposureCalculator,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4: SafeExposureCalculator,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5: SafeExposureCalculator,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6: SafeExposureCalculator,
    DATA_POINT_SIMMER_INDEX: SimmerIndexCalculator,
    DATA_POINT_SIMMER_ZONE: SimmerZoneCalculator,
    DATA_POINT_SOLARRADIATION: IlluminanceCalculator,
    DATA_POINT_SOLARRADIATION_PERCEIVED: PerceivedIlluminanceCalculator,
    DATA_POINT_TF_CO2: TemperatureCalculator,
    DATA_POINT_THERMAL_PERCEPTION: ThermalPerceptionCalculator,
    DATA_POINT_UV: UVIndexCalculator,
    DATA_POINT_WINDCHILL: WindChillCalculator,
    DATA_POINT_WINDDIR_NAME: WindDirNameCalculator,
}

DEFAULT_KEYS_TO_IGNORE = [
    "PASSKEY",
    "dateutc",
    "freq",
    "model",
    "stationtype",
]

# Map which data points tend to come with keys embedded at their end:
UNIT_SUFFIX_MAP = {
    DATA_POINT_GLOB_BAROM: "in",
    DATA_POINT_GLOB_GUST: "mph",
    DATA_POINT_GLOB_RAIN: "in",
    DATA_POINT_GLOB_TEMP: "f",
    DATA_POINT_GLOB_WIND: "mph",
    DATA_POINT_RAIN_RATE: "in",
    DATA_POINT_WINDCHILL: "f",
}


def get_calculator_instance(config: Config, payload_key: str) -> Calculator | None:
    """Get the appropriate calculator for a payload key.

    Args:
        config: A Config object.
        payload_key: The Ecowitt payload key.

    Returns:
        A parsed Calculator object (if it exists).
    """
    data_point_key, calculator_class = glob_search(CALCULATOR_MAP, payload_key)
    if not data_point_key or not calculator_class:
        return None
    return calculator_class(config, payload_key, data_point_key)


def get_typed_value(value: float | int | str) -> float | str:
    """Take a string and return its properly typed counterpart (if possible).

    Args:
        value: An input value.

    Returns:
        An appropriuately typed value.
    """
    try:
        return float(value)
    except ValueError:
        return str(value)


def remove_unit_from_key(key: str) -> str:
    """Remove a unit from the end of a key.

    Args:
        key: An Ecowitt payload key.

    Returns:
        A de-unit'd key.
    """
    data_point, _ = glob_search(CALCULATOR_MAP, key)

    if not data_point:
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

    CALCULATED_DATA_POINTS = (
        DATA_POINT_BEAUFORT_SCALE,
        DATA_POINT_DEWPOINT,
        DATA_POINT_FEELSLIKE,
        DATA_POINT_FROST_POINT,
        DATA_POINT_FROST_RISK,
        DATA_POINT_HEATINDEX,
        DATA_POINT_HUMIDEX,
        DATA_POINT_HUMIDEX_PERCEPTION,
        DATA_POINT_HUMIDITY_ABS,
        DATA_POINT_HUMIDITY_ABS_IN,
        DATA_POINT_RELATIVE_STRAIN_INDEX,
        DATA_POINT_RELATIVE_STRAIN_INDEX_PERCEPTION,
        DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1,
        DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2,
        DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3,
        DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4,
        DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5,
        DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6,
        DATA_POINT_SIMMER_INDEX,
        DATA_POINT_SIMMER_ZONE,
        DATA_POINT_SOLARRADIATION_PERCEIVED,
        DATA_POINT_THERMAL_PERCEPTION,
        DATA_POINT_WINDCHILL,
        DATA_POINT_WINDDIR_NAME,
    )

    config: Config
    data: dict[str, Any]
    device: Device = field(init=False)
    output: dict[str, CalculatedDataPoint] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize."""
        object.__setattr__(self, "device", get_device_from_raw_payload(self.data))

        normalized_payload = {
            remove_unit_from_key(payload_key): get_typed_value(value)
            for payload_key, value in self.data.items()
            if payload_key not in DEFAULT_KEYS_TO_IGNORE
        }

        self._process_raw_data_points(normalized_payload)
        if not self.config.disable_calculated_data:
            self._process_calculated_data_points(normalized_payload)

    def _process_calculated_data_points(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> None:
        """Process "from-scratch" data points that can be calculated from others.

        Unlike raw data points, if a calculator doesn't exist for some reason or the
        keys necessary to calculate the data point don't exist, we silently move on.

        Args:
            payload: A dictionary of keys to PreCalculatedValueType objects.
        """
        for key in self.CALCULATED_DATA_POINTS:
            if calculator := get_calculator_instance(self.config, key):
                try:
                    self.output[key] = calculator.calculate_from_payload(payload)
                except CalculationKeysMissingError:
                    LOGGER.debug("Cannot calculate %s due to missing keys", key)

    def _process_raw_data_points(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> None:
        """Process data points for which raw data was provided.

        Args:
            payload: A dictionary of keys to PreCalculatedValueType objects.
        """
        for key, value in payload.items():
            if (
                not self.config.disable_calculated_data
                and key in self.CALCULATED_DATA_POINTS
            ):
                LOGGER.debug("Skipping processing of calculated data point: %s", key)
                continue
            if (calculator := get_calculator_instance(self.config, key)) is None:
                LOGGER.debug("No calculator found for %s", key)
                self.output[key] = CalculatedDataPoint(data_point_key=key, value=value)
                continue

            LOGGER.debug(
                "Calculator found for %s: %s (key: %s, value: %s)",
                key,
                calculator,
                key,
                value,
            )

            try:
                self.output[key] = calculator.calculate_from_value(value)
            except CalculationFailedError as err:
                LOGGER.debug("Cannot calculate %s (raw value: %s): %s", key, value, err)
