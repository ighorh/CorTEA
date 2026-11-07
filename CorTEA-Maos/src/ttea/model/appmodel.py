from PySide6.QtCore import QSettings

from ttea.app import AppConfig
from ttea.util import PathConfig


class AppModel:
    """Estado global da aplicação (sessão ativa) - Implementação Singleton."""

    _instance = None
    _initialized = False

    def __new__(cls):
        """Garante que apenas uma instância seja criada."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa a instância apenas na primeira criação."""
        if AppModel._initialized:
            return  # Já foi inicializado anteriormente

        from ttea.model import Language

        self.language_model = Language()  # usado apenas no LanguageController

        # === Carrega o idioma atual salvo nas configurações ===
        settings = QSettings(PathConfig.config(), QSettings.IniFormat)
        saved_lang = settings.value(AppConfig.SETTINGS_GERAL_LANGUAGE)

        # Valida se o idioma salvo é um dos suportados
        available_codes = [
            lang["code"] for lang in self.language_model.get_languages()
        ]

        if saved_lang and saved_lang in available_codes:
            self._current_language: str = saved_lang
        else:
            self._current_language: str = Language.DEFAULT_LANGUAGE

        AppModel._initialized = True

    # ------------------------------------------------------------------
    # Property para acesso seguro ao idioma atual
    # ------------------------------------------------------------------
    @property
    def current_language(self) -> str:
        """Retorna o código do idioma atualmente em uso."""
        return self._current_language

    @current_language.setter
    def current_language(self, value: str) -> None:
        """Define o idioma atual, garantindo que seja válido."""
        from ttea.model import Language

        available_codes = [
            lang["code"] for lang in self.language_model.get_languages()
        ]
        if value in available_codes:
            self._current_language = value
        else:
            # Fallback seguro para o idioma padrão
            self._current_language = Language.DEFAULT_LANGUAGE

    # ------------------------------------------------------------------
    # Método auxiliar opcional
    # ------------------------------------------------------------------
    def is_english(self) -> bool:
        """Conveniência para verificar se o idioma atual é inglês."""
        return self.current_language == "en_US"

    @classmethod
    def get_instance(cls) -> "AppModel":
        """Retorna a única instância da classe (útil para chamadas explícitas)."""
        if cls._instance is None:
            cls._instance = cls()  # Isso chamará __new__ e __init__
        return cls._instance
