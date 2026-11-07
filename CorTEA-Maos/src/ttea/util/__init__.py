"""Utility functions for the T-TEA platform, including configuration and
path management.

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
CSVHandler
    Handling CSV files with a custom dialect.
PathConfig
    Manage file paths and directory structures.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development.

Contributions and bug reports are welcome at:
https://github.com/larvattea/ttea
"""

# Define the __all__ variable
__all__ = [
    "CriticalHooks",
    "CSVHandler",
    "Image",
    "MessageService",
    "QtDateFormat",
    "PathConfig",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .criticalhooks import CriticalHooks
from .cvshandler import CSVHandler
from .image import Image
from .messageservice import MessageService
from .pathconfig import PathConfig
from .qtdateformat import QtDateFormat
