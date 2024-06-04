"""Define wind calculators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from ecowitt2mqtt.const import (
    CONF_OUTPUT_UNIT_SPEED,
    DATA_POINT_GLOB_WINDDIR,
    DATA_POINT_WINDSPEED,
    DEGREE,
    UnitOfSpeed,
    UnitSystem,
)
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.unit_conversion import SpeedConverter

WIND_DIR_NAMES = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
    "N",
]


@dataclass
class BeaufortScaleRating:  # pylint: disable=too-many-instance-attributes
    """Define a dataclass to store a Beaufort scale rating."""

    number: int
    minimum_kmh: float
    maximum_kmh: float
    minimum_mph: float
    maximum_mph: float
    description: str
    sea_conditions: str
    land_conditions: str


BEAUFORT_SCALE_RATINGS: list[BeaufortScaleRating] = [
    BeaufortScaleRating(
        number=0,
        minimum_kmh=0.0,
        maximum_kmh=2.0,
        minimum_mph=0.0,
        maximum_mph=1.0,
        description="Calm",
        sea_conditions="Sea like a mirror",
        land_conditions="Smoke rises vertically",
    ),
    BeaufortScaleRating(
        number=1,
        minimum_kmh=2.0,
        maximum_kmh=6.0,
        minimum_mph=1.0,
        maximum_mph=4.0,
        description="Light air",
        sea_conditions=(
            "Ripples with appearance of scales are formed, without foam crests"
        ),
        land_conditions="Direction shown by smoke drift but not by wind vanes",
    ),
    BeaufortScaleRating(
        number=2,
        minimum_kmh=6.0,
        maximum_kmh=12.0,
        minimum_mph=4.0,
        maximum_mph=8.0,
        description="Light breeze",
        sea_conditions=(
            "Small wavelets still short but more pronounced; crests have a glassy "
            "appearance but do not break"
        ),
        land_conditions="Wind felt on face; leaves rustle; wind vane moved by wind",
    ),
    BeaufortScaleRating(
        number=3,
        minimum_kmh=12.0,
        maximum_kmh=20.0,
        minimum_mph=8.0,
        maximum_mph=13.0,
        description="Gentle breeze",
        sea_conditions=(
            "Large wavelets; crests begin to break; foam of glassy appearance; perhaps "
            "scattered white horses"
        ),
        land_conditions=(
            "Leaves and small twigs in constant motion; light flags extended"
        ),
    ),
    BeaufortScaleRating(
        number=4,
        minimum_kmh=20.0,
        maximum_kmh=29.0,
        minimum_mph=13.0,
        maximum_mph=19.0,
        description="Moderate breeze",
        sea_conditions="Small waves becoming longer; fairly frequent white horses",
        land_conditions="Raises dust and loose paper; small branches moved",
    ),
    BeaufortScaleRating(
        number=5,
        minimum_kmh=29.0,
        maximum_kmh=39.0,
        minimum_mph=19.0,
        maximum_mph=25.0,
        description="Fresh breeze",
        sea_conditions=(
            "Moderate waves taking a more pronounced long form; many white horses are "
            "formed; chance of some spray"
        ),
        land_conditions=(
            "Small trees in leaf begin to sway; crested wavelets form on inland waters"
        ),
    ),
    BeaufortScaleRating(
        number=6,
        minimum_kmh=39.0,
        maximum_kmh=50.0,
        minimum_mph=25.0,
        maximum_mph=32.0,
        description="Strong breeze",
        sea_conditions=(
            "Large waves begin to form; the white foam crests are more "
            "extensive everywhere; probably some spray"
        ),
        land_conditions=(
            "Large branches in motion; whistling heard in telegraph wires; "
            "umbrellas used with difficulty"
        ),
    ),
    BeaufortScaleRating(
        number=7,
        minimum_kmh=50.0,
        maximum_kmh=62.0,
        minimum_mph=32.0,
        maximum_mph=39.0,
        description="High wind, moderate gale, near gale",
        sea_conditions=(
            "Sea heaps up and white foam from breaking waves begins to be "
            "blown in streaks along the direction of the wind; spindrift begins to be "
            "seen"
        ),
        land_conditions=(
            "Whole trees in motion; inconvenience felt when walking against the wind"
        ),
    ),
    BeaufortScaleRating(
        number=8,
        minimum_kmh=62.0,
        maximum_kmh=75.0,
        minimum_mph=39.0,
        maximum_mph=47.0,
        description="Gale, fresh gale",
        sea_conditions=(
            "Moderately high waves of greater length; edges of crests break into "
            "spindrift; foam is blown in well-marked streaks along the direction of "
            "the wind"
        ),
        land_conditions=("Twigs break off trees; generally impedes progress"),
    ),
    BeaufortScaleRating(
        number=9,
        minimum_kmh=75.0,
        maximum_kmh=89.0,
        minimum_mph=47.0,
        maximum_mph=55.0,
        description="Strong/severe gale",
        sea_conditions=(
            "High waves; dense streaks of foam along the direction of the "
            "wind; sea begins to roll; spray affects visibility"
        ),
        land_conditions="Slight structural damage (chimney pots and slates removed)",
    ),
    BeaufortScaleRating(
        number=10,
        minimum_kmh=89.0,
        maximum_kmh=103.0,
        minimum_mph=55.0,
        maximum_mph=64.0,
        description="Storm, whole gale",
        sea_conditions=(
            "Very high waves with long overhanging crests; resulting foam in great "
            "patches is blown in dense white streaks along the direction of the wind; "
            "on the whole the surface of the sea takes on a white appearance; rolling "
            "of the sea becomes heavy; visibility affected"
        ),
        land_conditions=(
            "Seldom experienced inland; trees uprooted; considerable structural damage"
        ),
    ),
    BeaufortScaleRating(
        number=11,
        minimum_kmh=103.0,
        maximum_kmh=118.0,
        minimum_mph=64.0,
        maximum_mph=73.0,
        description="Violent storm",
        sea_conditions=(
            "Exceptionally high waves; small- and medium-sized ships might be for a "
            "long time lost to view behind the waves; sea is covered with long white "
            "patches of foam; everywhere the edges of the wave crests are blown into "
            "foam; visibility affected"
        ),
        land_conditions="Very rarely experienced; accompanied by widespread damage",
    ),
    BeaufortScaleRating(
        number=12,
        minimum_kmh=118.0,
        maximum_kmh=300.0,
        minimum_mph=73.0,
        maximum_mph=200.0,
        description="Hurricane force",
        sea_conditions=(
            "The air is filled with foam and spray; sea is completely white with "
            "driving spray; visibility very seriously affected"
        ),
        land_conditions="Devastation",
    ),
]


class BeaufortScaleCalculator(Calculator):
    """Define a Beaufort Scale calculator."""

    @Calculator.requires_keys(DATA_POINT_WINDSPEED)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        wind_speed = cast(float, payload[DATA_POINT_WINDSPEED])

        rating = next(
            r
            for r in BEAUFORT_SCALE_RATINGS
            if (
                self._config.input_unit_system == UnitSystem.IMPERIAL
                and r.minimum_mph <= wind_speed < r.maximum_mph
            )
            or (
                self._config.input_unit_system == UnitSystem.METRIC
                and r.minimum_kmh <= wind_speed < r.maximum_kmh
            )
        )

        return self.get_calculated_data_point(
            rating.number,
            attributes={
                "description": rating.description,
                "sea_conditions": rating.sea_conditions,
                "land_conditions": rating.land_conditions,
            },
        )


class WindDirCalculator(SimpleCalculator):
    """Define a wind direction calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return DEGREE


class WindDirNameCalculator(Calculator):
    """Define a wind direction name calculator."""

    @Calculator.requires_keys(DATA_POINT_GLOB_WINDDIR)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        wind_dir = float(payload[DATA_POINT_GLOB_WINDDIR])
        return self.get_calculated_data_point(
            WIND_DIR_NAMES[int((wind_dir + 11.25) % 360 / 22.5)]
        )


class WindSpeedCalculator(Calculator):
    """Define a wind speed calculator."""

    DEFAULT_INPUT_UNIT = UnitOfSpeed.MILES_PER_HOUR
    UNIT_OVERRIDE_CONFIG_OPTION = CONF_OUTPUT_UNIT_SPEED

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial).

        Returns:
            A unit string.
        """
        return UnitOfSpeed.MILES_PER_HOUR

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric).

        Returns:
            A unit string.
        """
        return UnitOfSpeed.KILOMETERS_PER_HOUR

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
        return self.get_calculated_data_point(
            float_value, unit_converter=SpeedConverter
        )
