"""Factory package for creating and managing application views.

This package provides view factory classes used to create and configure
application views consistently across the T-TEA platform.

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
ViewFactory
    Creates view instances for the application.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development.

Contributions and bug reports are welcome at:
https://github.com/larvattea/ttea
"""

# Define the __all__ variable
__all__ = [
    "AppViewFactory",
    "ViewFactory",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .appviewfactory import AppViewFactory
from .viewfactory import ViewFactory
