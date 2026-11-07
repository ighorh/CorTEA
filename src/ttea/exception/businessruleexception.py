"""
Exception classes for business rule violations.

This module defines custom exception types used to handle specific
business logic violations in the application, with support for error
codes and additional contextual details.

"""

from typing import Any


class BusinessRuleException(Exception):
    """
    Exception raised when a business rule is violated.

    This exception is designed to handle specific business logic
    violations with optional error codes and additional details for
    error tracking and debugging.

    Attributes
    ----------
    message : str
        The exception message describing the business rule violation.
    code : str or None
        An optional error code to identify the type of violation.
    details : dict[str, Any]
        A dictionary containing additional details about the
        exception.

    Methods
    -------
    __init__(message, *, code=None, details=None)
        Initialize a BusinessRuleException with message, optional
        error code, and additional details.
    __str__()
        Return a string representation of the exception, formatted
        with code prefix if available.
    __repr__()
        Return a detailed string representation containing all
        exception attributes.

    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize a BusinessRuleException.

        Parameters
        ----------
        message : str
            The exception message describing the business rule
            violation.
        code : str, optional
            An optional error code to identify the type of violation.
            Default is None.
        details : dict[str, Any], optional
            A dictionary containing additional details about the
            exception. Default is an empty dictionary.

        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        """
        Return a string representation of the exception.

        Returns
        -------
        str
            If a code is set, returns "[{code}] {message}".
            Otherwise, returns just the message.

        """
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the exception.

        Returns
        -------
        str
            A string containing class name and all exception
            attributes in format "ClassName(message=..., code=...,
            details=...)".

        """
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"code={self.code!r}, "
            f"details={self.details!r})"
        )
