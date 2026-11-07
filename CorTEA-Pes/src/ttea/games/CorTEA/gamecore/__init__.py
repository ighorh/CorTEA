"""
A Python package for CorTEA Game core. Developed by the Larva UDESC team.

This package provides core functionality for CorTEA game: webcam capture,
foot tracking, dwell selection and sound.

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
Camera
    Camera.
JanelaCamera
    JanelaCamera.
Rastreamento
    Rastreamento.
SeletorPermanencia
    SeletorPermanencia.
Sons
    Sons.

Notes
-----
This package is maintained by the Larva UDESC team and is under active
development. Contributions and bug reports are welcome at:
https://github.com/larva-udesc/udesc_ttea_view
"""

# Define the __all__ variable
__all__ = [
    "Camera",
    "JanelaCamera",
    "Rastreamento",
    "SeletorPermanencia",
    "Sons",
]

__version__ = "2.0.0"
__date__ = "2026-10-06"
__author__ = "Larva UDESC"
__license__ = "MIT License"

# Import the submodules
from .audio import Sons
from .camera import Camera
from .janelacamera import JanelaCamera
from .rastreamento import Rastreamento
from .seletor import SeletorPermanencia
