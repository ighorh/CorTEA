"""
A Python package for CorTEA Game user interface helpers.

This package provides drawing utilities (text, buttons, icons) for CorTEA game.

Attributes
----------
__version__ : str
    The current version of the package.
__date__ : str
    The release date of this version.

See Also
--------
UI
    UI.
"""

# Define the __all__ variable
__all__ = [
    "UI",
]

__version__ = "2.0.0"
__date__ = "2026-10-06"

# Import the submodules
from .ui import UI
