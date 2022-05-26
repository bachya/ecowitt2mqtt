"""Define package errors."""


class EcowittError(Exception):
    """Define a base exception."""

    pass


class ConfigError(EcowittError):
    """Define an error related to bad configuration."""

    pass
