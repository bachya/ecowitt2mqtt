"""Define tests for BGT and WBGT data points."""

from __future__ import annotations

from typing import Any

import pytest

from ecowitt2mqtt.const import (
    CONF_OUTPUT_UNIT_SYSTEM,
    CONF_OUTPUT_UNIT_TEMPERATURE,
    UnitOfTemperature,
    UnitSystem,
)
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, DataPointType
from tests.common import TEST_CONFIG_JSON


@pytest.mark.parametrize("device_data_filename", ["payload_gw3000b_bgt.json"])
@pytest.mark.parametrize(
    "config",
    [
        TEST_CONFIG_JSON | {CONF_OUTPUT_UNIT_TEMPERATURE: UnitOfTemperature.CELSIUS},
    ],
)
def test_bgt_wbgt_metric_output(device_data: dict[str, Any], ecowitt: Ecowitt) -> None:
    """Test that BGT and WBGT values are converted from Fahrenheit to Celsius."""
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)

    assert processed_data.output["bgt"] == CalculatedDataPoint(
        "bgt",
        35.0,
        unit=UnitOfTemperature.CELSIUS,
        attributes={},
        data_type=DataPointType.NON_BOOLEAN,
    )
    assert processed_data.output["wbgt"] == CalculatedDataPoint(
        "wbgt",
        28.000000000000004,
        unit=UnitOfTemperature.CELSIUS,
        attributes={},
        data_type=DataPointType.NON_BOOLEAN,
    )


@pytest.mark.parametrize("device_data_filename", ["payload_gw3000b_bgt.json"])
@pytest.mark.parametrize("config", [TEST_CONFIG_JSON])
def test_bgt_wbgt_imperial_output(
    device_data: dict[str, Any], ecowitt: Ecowitt
) -> None:
    """Test that BGT and WBGT values pass through as Fahrenheit when imperial."""
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)

    assert processed_data.output["bgt"] == CalculatedDataPoint(
        "bgt",
        95.0,
        unit=UnitOfTemperature.FAHRENHEIT,
        attributes={},
        data_type=DataPointType.NON_BOOLEAN,
    )
    assert processed_data.output["wbgt"] == CalculatedDataPoint(
        "wbgt",
        82.4,
        unit=UnitOfTemperature.FAHRENHEIT,
        attributes={},
        data_type=DataPointType.NON_BOOLEAN,
    )


@pytest.mark.parametrize("device_data_filename", ["payload_gw3000b_bgt.json"])
@pytest.mark.parametrize(
    "config",
    [
        TEST_CONFIG_JSON | {CONF_OUTPUT_UNIT_SYSTEM: UnitSystem.METRIC},
    ],
)
def test_bgt_wbgt_metric_unit_system(
    device_data: dict[str, Any], ecowitt: Ecowitt
) -> None:
    """Test that BGT and WBGT convert correctly with metric unit system."""
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)

    assert processed_data.output["bgt"] == CalculatedDataPoint(
        "bgt",
        35.0,
        unit=UnitOfTemperature.CELSIUS,
        attributes={},
        data_type=DataPointType.NON_BOOLEAN,
    )
    assert processed_data.output["wbgt"] == CalculatedDataPoint(
        "wbgt",
        28.000000000000004,
        unit=UnitOfTemperature.CELSIUS,
        attributes={},
        data_type=DataPointType.NON_BOOLEAN,
    )


@pytest.mark.parametrize("device_data_filename", ["payload_gw3000b_bgt.json"])
@pytest.mark.parametrize("config", [TEST_CONFIG_JSON])
def test_bgtbatt_handled(device_data: dict[str, Any], ecowitt: Ecowitt) -> None:
    """Test that bgtbatt is recognized as a battery data point."""
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)

    assert "bgtbatt" in processed_data.output
    assert processed_data.output["bgtbatt"].data_type == DataPointType.BOOLEAN
