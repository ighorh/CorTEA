from typing import Dict, List

# Local module import
from ttea.util import PathConfig


class Language:
    """Model responsável apenas pelos dados estáticos dos idiomas suportados.

    Attributes
    ----------
    LANGUAGES : List[Dict[str, str]]
        Lista de idiomas disponíveis na aplicação.
    DEFAULT_LANGUAGE : str
        Idioma padrão em caso de falha.
    """

    LANGUAGES = [
        {
            "code": "pt_BR",
            "description": "Português",
            "flag": PathConfig.flag("brazil"),
        },
        {
            "code": "es_ES",
            "description": "Español",
            "flag": PathConfig.flag("spain"),
        },
        {
            "code": "en_US",
            "description": "English",
            "flag": PathConfig.flag("usa"),
        },
    ]

    DEFAULT_LANGUAGE = "pt_BR"

    def get_languages(self) -> List[Dict[str, str]]:
        """Retorna a lista de idiomas disponíveis."""
        return self.LANGUAGES
