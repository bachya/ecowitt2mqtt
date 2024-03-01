"""Define UV index calculators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from ecowitt2mqtt.const import (
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6,
    DATA_POINT_UV,
    LOGGER,
    UV_INDEX,
    UnitOfTime,
)
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType


@dataclass
class SafeExposureInfo:
    """Define a dataclass to store information about a safe exposure level."""

    constant: float
    typical_features: str
    tanning_ability: str
    ethnicity: str


SAFE_EXPOSURE_INFO_MAP: dict[str, SafeExposureInfo] = {
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1: SafeExposureInfo(
        constant=2.5,
        ethnicity="Scandinavian, Celtic",
        tanning_ability="Always burns, does not tan",
        typical_features=(
            "Very fair skin, white; red or blond hair; light-colored eyes; freckles "
            "likely"
        ),
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2: SafeExposureInfo(
        constant=3.0,
        ethnicity="Northern European (Caucasian)",
        tanning_ability="Burns easily, tans poorly",
        typical_features="Fair skin, white; light eyes; light hair",
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3: SafeExposureInfo(
        constant=4.0,
        ethnicity="Darker Caucasian (Central Europe)",
        tanning_ability="Tans after initial burn",
        typical_features=(
            "Fair skin, cream white; any eye or hair color (very common skin type)"
        ),
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4: SafeExposureInfo(
        constant=5.0,
        ethnicity="Mediterranean, Asian, Hispanic",
        tanning_ability="Burns minimally, tans easily",
        typical_features=(
            "Olive skin, typical Mediterranean Caucasian skin; dark brown hair; medium "
            "to heavy pigmentation"
        ),
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5: SafeExposureInfo(
        constant=8.0,
        ethnicity="Middle eastern, Latin, light-skinned African-American, Indian",
        tanning_ability="Rarely burns, tans darkly easily",
        typical_features=(
            "Brown skin, typical Middle Eastern skin; dark hair; rarely sun sensitive"
        ),
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6: SafeExposureInfo(
        constant=13.0,
        ethnicity="Dark-skinned African American",
        tanning_ability="Never burns, always tans darkly",
        typical_features="Black skin; rarely sun sensitive",
    ),
}


class SafeExposureCalculator(Calculator):
    """Define a safe exposure calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return UnitOfTime.MINUTES

    @Calculator.requires_keys(DATA_POINT_UV)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        uv_index = cast(float, payload[DATA_POINT_UV])
        safe_exposure_info = SAFE_EXPOSURE_INFO_MAP[self._payload_key]

        try:
            value = round(
                (200 * safe_exposure_info.constant) / (3 * uv_index),
                1,
            )
        except ZeroDivisionError:
            LOGGER.debug(
                "Safe exposure only valid for non-zero UV indices (current: %s)",
                payload,
            )
            return self.get_calculated_data_point(None)

        return self.get_calculated_data_point(
            value,
            attributes={
                "ethnicity": safe_exposure_info.ethnicity,
                "tanning_ability": safe_exposure_info.tanning_ability,
                "typical_features": safe_exposure_info.typical_features,
            },
        )


class UVIndexCalculator(SimpleCalculator):
    """Define a UV index calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return UV_INDEX
