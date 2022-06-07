"""Define nox actions."""
import tempfile
from typing import Any

import nox


def install_with_constraints(session: nox.sessions.Session, *args: str, **kwargs: Any):
    """Install PyPI packages based on pyproject.toml constraints."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session
def coverage(session: nox.sessions.Session) -> None:
    """Report test coverage."""
    args = session.posargs or [
        "-s",
        "--cov=ecowitt2mqtt",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "tests/",
    ]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, "aiohttp", "pytest", "pytest-asyncio", "pytest-cov"
    )
    session.run("pytest", *args)


@nox.session
def tests(session: nox.sessions.Session) -> None:
    """Run all tests."""
    args = session.posargs or ["-s", "tests/"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "aiohttp", "pytest", "pytest-asyncio")
    session.run("pytest", *args)
