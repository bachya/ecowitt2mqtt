"""Define tests for configuration management."""
import pytest
from typer.testing import CliRunner

from ecowitt2mqtt.main import APP


@pytest.mark.parametrize(
    "args,missing_args_str",
    [
        ([], "--mqtt-broker"),
        (["-b", "127.0.0.1"], "--mqtt-topic or --hass-discovery"),
    ],
)
def test_missing_required_options(args, caplog, missing_args_str, runner):
    """Test that missing required options are handled."""
    runner.invoke(APP, args)
    assert caplog.messages[0] == f"Missing required option: {missing_args_str}"
