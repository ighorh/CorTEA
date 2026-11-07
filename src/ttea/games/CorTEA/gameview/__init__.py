"""
A Python package for CorTEA Game views.

This package provides the menus and screens of CorTEA game.

Attributes
----------
__version__ : str
    The current version of the package.
__date__ : str
    The release date of this version.

See Also
--------
Menu
    Menu.
"""

# Define the __all__ variable
__all__ = [
    "Menu",
]

__version__ = "2.0.0"
__date__ = "2026-10-06"

# Import the submodules
from .menu import Menu
