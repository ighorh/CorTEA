"""Exception package for the T-TEA platform.

A Python package for customized exceptions from the T-TEA platform.
Developed by the Larva UDESC team.

This package provides custom exception classes for the T-TEA platform,
enabling structured error handling with support for error codes and
contextual details.

Attributes
----------
__version__ : str
    Current package version.
__date__ : str
    Release date of the package version.
__author__ : str
    Package author or team.
__license__ : str
    Package license.

See Also
--------
BusinessRuleException
    Custom exception for business rule violations.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development.

Contributions and bug reports are welcome at:
https://github.com/larvattea/ttea
"""

# Define the __all__ variable
__all__ = [
    "BusinessRuleException",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .businessruleexception import BusinessRuleException
