"""A Python package for service classes from the T-TEA platform,
supporting service logic.
Developed by the Larva UDESC team.

This package provides the service classes for controllers,
for the T-TEA platform.

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
PlayerService
    Manages the service logic and data operations related to player entities.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/larvattea/ttea
"""

# Define the __all__ variable
__all__ = [
    "CalibrationService",
    "CalibrationSettingService",
    "ProfessionalService",
    "InstitutionFacilityService",
    "LanguageService",
    "MainService",
    "PlayerGameLaunchService",
    "PlayerService",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .calibrationservice import CalibrationService
from .calibrationsettingservice import CalibrationSettingService
from .institutionfacilityservice import InstitutionFacilityService
from .languageservice import LanguageService
from .mainservice import MainService
from .playergamelaunchservice import PlayerGameLaunchService
from .playerservice import PlayerService
from .professionalservice import ProfessionalService
