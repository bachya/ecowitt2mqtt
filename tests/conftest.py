"""Define dynamic fixtures."""
import pytest
from typer.testing import CliRunner


@pytest.fixture(name="runner")
def runner_fixture():
    """Define a fixture to return a Typer CLI test runner."""
    return CliRunner()
