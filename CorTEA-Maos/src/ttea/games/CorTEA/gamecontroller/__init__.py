"""
A Python package for CorTEA Game controller.

This package provides the game logic of CorTEA game.

Attributes
----------
__version__ : str
    The current version of the package.
__date__ : str
    The release date of this version.

See Also
--------
GameController
    GameController.
"""

# Define the __all__ variable
__all__ = [
    "GameController",
]

__version__ = "2.0.0"
__date__ = "2026-10-06"

# Import the submodules
from .gamecontroller import GameController
