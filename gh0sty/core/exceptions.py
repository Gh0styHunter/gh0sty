"""Custom exceptions for the gh0sty framework."""


class Gh0styException(Exception):
    """Base exception for all gh0sty framework errors."""

    pass


class ConfigError(Gh0styException):
    """Exception raised for configuration loading or updating errors."""

    pass


class ScanError(Gh0styException):
    """Exception raised during scanning/inventory operations."""

    pass


class ValidationError(Gh0styException):
    """Exception raised for target or value validations."""

    pass


class ReportError(Gh0styException):
    """Exception raised for report generation issues."""

    pass
