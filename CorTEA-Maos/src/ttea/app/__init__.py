"""Package for application configuration and startup support in the
T-TEA platform.

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
AppConfig
    Manages application configuration settings.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development.

Contributions and bug reports are welcome at:
https://github.com/larvattea/ttea
"""

# Define the __all__ variable
__all__ = [
    "AppConfig",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .appconfig import AppConfig
