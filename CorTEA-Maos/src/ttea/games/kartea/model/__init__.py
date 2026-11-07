"""
model

A Python package for model in Kartea Game.

This package provides models for player and session game configuration.

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
PlayerKarteaConfig
    Model for managing player configuration data.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/larva-udesc/udesc_ttea_view
"""

# Define the __all__ variable
__all__ = [
    "KarteaPhase",
    "KarteaPhaseLevel",
    "PlayerKarteaConfig",
    "PlayerKarteaSession",
    "PlayerKarteaSessionDetail",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .karteaphase import KarteaPhase
from .karteaphaselevel import KarteaPhaseLevel
from .playerkarteaconfig import PlayerKarteaConfig
from .playerkarteasession import PlayerKarteaSession
from .playerkarteasessiondetail import PlayerKarteaSessionDetail
