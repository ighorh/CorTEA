"""
A Python package for CorTEA Game model.

This package provides models for CorTEA game. The class names follow the
class diagram of the CorTEA paper (Atividade, Desempenho, SistemaAjuda,
Sessao, Usuario).

Attributes
----------
__version__ : str
    The current version of the package.
__date__ : str
    The release date of this version.

See Also
--------
Atividade
    Atividade.
Desempenho
    Desempenho.
Feedback
    Feedback.
Grid
    Grid.
Sessao
    Sessao.
SistemaAjuda
    SistemaAjuda.
Usuario
    Usuario.
"""

# Define the __all__ variable
__all__ = [
    "Atividade",
    "Desempenho",
    "Feedback",
    "Grid",
    "Sessao",
    "SistemaAjuda",
    "Usuario",
]

__version__ = "2.0.0"
__date__ = "2026-10-06"

# Import the submodules
from .atividade import Atividade
from .desempenho import Desempenho
from .feedback import Feedback
from .grid import Grid
from .sessao import Sessao, Usuario
from .sistemaajuda import SistemaAjuda
