"""A Python package for Data Access Objects (DAOs) from the T-TEA platform,
supporting data management and persistence. Developed by the Larva UDESC team.

This package provides the DAO classes for the T-TEA platform.

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
DAO
    Data Access Object for managing data persistence and retrieval.
PlayerCsvDAO
    Data Access Object for managing player data in CSV format.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/larvattea/ttea
"""

# Define the __all__ variable
__all__ = [
    "CalibrationIniDAO",
    "CalibrationPointCsvDAO",
    "CalibrationSettingIniDAO",
    "DAO",
    "ProfessionalCsvDAO",
    "InstitutionFacilityCsvDAO",
    "PlayerCsvDAO",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

from .calibrationinidao import CalibrationIniDAO
from .calibrationpointcsvdao import CalibrationPointCsvDAO
from .calibrationsettinginidao import CalibrationSettingIniDAO
from .dao import DAO
from .institutionfacilitycsvdao import InstitutionFacilityCsvDAO
from .playercsvdao import PlayerCsvDAO
from .professionalcsvdao import ProfessionalCsvDAO
