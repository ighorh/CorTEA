"""
controller

A Python package for controllers in Kartea Game.

This package provides the controller classes for managing game logic and user interactions.

Attributes
----------
__version__ : str
    The current version of the package.
__date__ : str
    The release date of this version.
__author__ : str
    The development team.
__license__ : str
    The license under which the package is distributed.

See Also
--------
PlayerKarteaConfigCsvDAO
    Data Access Object for managing player kartea configuration data in CSV format.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/larva-udesc/udesc_ttea_view
"""

# Define the __all__ variable
__all__ = [
    "PlayerKarteaConfigEditController",
    "PlayerKarteaConfigListController",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .playerkarteaconfigeditcontroller import PlayerKarteaConfigEditController
from .playerkarteaconfiglistcontroller import PlayerKarteaConfigListController
