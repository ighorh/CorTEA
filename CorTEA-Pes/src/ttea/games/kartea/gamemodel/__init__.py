"""
A Python package for KarTEA Game model. Developed by the Larva UDESC team.

This package provides models for KarTEA game.

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
Background
    Background.
Car
    Car.
Image
    Image.
KarTEATheme
    KarTEATheme.
Line
    Line.
Obstacle
    Obstacle.
Target
    Target.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/larva-udesc/udesc_ttea_view
"""

# Define the __all__ variable
__all__ = [
    "Background",
    "Car",
    "Image",
    "Line",
    "Obstacle",
    "Target",
    "World",
]

__version__ = "1.0.0"
__date__ = "2025-12-25"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .background import Background
from .car import Car
from .image import Image
from .line import Line
from .obstacle import Obstacle
from .target import Target
