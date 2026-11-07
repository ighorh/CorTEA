"""
A Python package for CorTEA Game utilities.

This package provides settings, states, texts and CSV recording for CorTEA game.

Attributes
----------
__version__ : str
    The current version of the package.
__date__ : str
    The release date of this version.

See Also
--------
GameSettings
    GameSettings.
GameState
    GameState.
GerenciadorCSV
    GerenciadorCSV.
"""

# Define the __all__ variable
__all__ = [
    "GameSettings",
    "GameState",
    "GerenciadorCSV",
    "formatar_tempo",
    "t",
]

__version__ = "2.0.0"
__date__ = "2026-10-06"

# Import the submodules (ordem importa: gerenciadorcsv usa gamemodel, que usa
# GameSettings)
from .gamesettings import ConfigFase, GameSettings
from .gamestate import GameState
from .textos import formatar_tempo, t
from .gerenciadorcsv import GerenciadorCSV  # noqa: E402
