"""Define dynamic fixtures."""
import pytest
from typer.testing import CliRunner

from .common import TEST_RAW_JSON


@pytest.fixture(name="config", scope="session")
def config_fixture():
    """Define a fixture to return raw configuration data."""
    return TEST_RAW_JSON


@pytest.fixture(name="config_filepath")
def config_filepath_fixture(config, tmp_path):
    """Define a fixture to return a config filepath."""
    config_filepath = f"{tmp_path}/config.json"
    with open(config_filepath, "w", encoding="utf-8") as config_file:
        config_file.write(config)
    return config_filepath


@pytest.fixture(name="runner")
def runner_fixture():
    """Define a fixture to return a Typer CLI test runner."""
    return CliRunner()
