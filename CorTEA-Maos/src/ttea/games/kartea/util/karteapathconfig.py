# karteapathconfig.py
import configparser
from pathlib import Path
from typing import Dict, List, Optional

from PySide6.QtCore import QDir, QDirIterator, QFile, QIODevice

from ttea.games.kartea.resources import resourceskartea_rc
from ttea.util import PathConfig


class KarteaPathConfig(PathConfig):
    """
    Configuração de caminhos específicos para o jogo KarTEA.

    Herda toda a lógica do PathConfig.
    """

    KARTEA_CONFIG_FILENAME = "kartea.ini"

    # ===================================================================
    # Diretórios específicos do KarTEA
    # ===================================================================
    KARTEA_DIR = PathConfig.EXERGAME_DIR / "kartea"
    KARTEA_RESOURCES_DIR = KARTEA_DIR / "resources"
    KARTEA_IMAGES_DIR = KARTEA_RESOURCES_DIR / "images"
    KARTEA_SOUNDS_DIR = KARTEA_RESOURCES_DIR / "sounds"
    KARTEA_PHASES_DIR = KARTEA_RESOURCES_DIR / "phases"
    KARTEA_PLAYER_DIR = KARTEA_DIR / "players"

    # Arquivo de configuração específico
    KARTEA_CONFIG_FILE = KARTEA_DIR / KARTEA_CONFIG_FILENAME

    # ===================================================================
    # Garantia de estrutura
    # ===================================================================
    @classmethod
    def ensure_kartea_dirs(cls) -> None:
        """Cria todas as pastas necessárias do KarTEA."""
        cls.ensure_dirs()  # método do PathConfig
        for directory in [
            cls.KARTEA_DIR,
            cls.KARTEA_RESOURCES_DIR,
            cls.KARTEA_IMAGES_DIR,
            cls.KARTEA_SOUNDS_DIR,
            cls.KARTEA_PHASES_DIR,
            cls.KARTEA_PLAYER_DIR,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        cls.create_default_ini()

    # ===================================================================
    # Recursos embutidos (Qt)
    # ===================================================================
    @staticmethod
    def kartea_resource(path: str = "") -> str:
        return f":/kartea/{path}".rstrip("/")

    @staticmethod
    def _find_resource(base_path: str, name: str) -> str:
        """Auxiliar para buscar recursos embutidos."""
        it = QDirIterator(
            base_path, [name], QDir.Files, QDirIterator.Subdirectories
        )
        return it.next() if it.hasNext() else ""

    @staticmethod
    def game_builtin_image(name: str) -> str:
        return KarteaPathConfig._find_resource(":/images", name)

    @staticmethod
    def game_builtin_sound(name: str) -> str:
        return KarteaPathConfig._find_resource(":/sounds", name)

    # ===================================================================
    # Fases
    # ===================================================================
    @classmethod
    def get_phase_source(cls, phase_id: int) -> Dict[str, str]:
        user_file = cls.KARTEA_PHASES_DIR / f"{phase_id}.csv"
        if user_file.exists():
            return {"type": "file", "path": str(user_file)}
        return {"type": "resource", "path": f":/phases/{phase_id}"}

    @classmethod
    def read_phase_data(cls, phase_id: int) -> Optional[str]:
        source = cls.get_phase_source(phase_id)

        if source["type"] == "file":
            try:
                return Path(source["path"]).read_text(encoding="utf-8-sig")
            except Exception:
                return None

        qfile = QFile(source["path"])
        if qfile.open(QIODevice.ReadOnly | QIODevice.Text):
            content = bytes(qfile.readAll()).decode("utf-8")
            qfile.close()
            return content
        return None

    # ===================================================================
    # Métodos de dados do usuário
    # ===================================================================
    @classmethod
    def player(cls, filename: str) -> str:
        cls.ensure_kartea_dirs()
        return str(cls.KARTEA_PLAYER_DIR / filename)

    @classmethod
    def phase(cls, filename: str) -> str:
        cls.ensure_kartea_dirs()
        return str(cls.KARTEA_PHASES_DIR / filename)

    @classmethod
    def kartea_config(cls, filename: str = KARTEA_CONFIG_FILENAME) -> str:
        cls.ensure_kartea_dirs()
        return str(cls.KARTEA_DIR / filename)

    @classmethod
    def game_image(cls, filename: str) -> str:
        cls.ensure_kartea_dirs()
        return str(cls.KARTEA_IMAGES_DIR / filename)

    @classmethod
    def game_sound(cls, filename: str) -> str:
        cls.ensure_kartea_dirs()
        return str(cls.KARTEA_SOUNDS_DIR / filename)

    # ===================================================================
    # Configuração INI
    # ===================================================================
    @classmethod
    def kartea_config_file_exists(
        cls, filename: str = KARTEA_CONFIG_FILENAME
    ) -> bool:
        return Path(cls.kartea_config(filename)).exists()

    @classmethod
    def read_config(cls) -> Dict[str, Dict[str, str]]:
        cls.ensure_kartea_dirs()
        config = configparser.ConfigParser()
        config.read(cls.KARTEA_CONFIG_FILE)
        return {
            section: dict(config[section]) for section in config.sections()
        }

    @classmethod
    def create_default_ini(cls) -> None:
        """Cria o arquivo kartea.ini com valores padrão (apenas se não existir)."""
        if cls.KARTEA_CONFIG_FILE.exists():
            return

        config = configparser.ConfigParser(allow_no_value=True)

        config["game_settings"] = {
            "phase_default": "1",
            "level_default": "1",
            "level_time_default": "120",
        }
        config["visual_resources"] = {
            "vehicle_image_default": "defaultvehicle",
            "environment_image_default": "defaultenvironment",
            "target_image_default": "defaultstar",
            "obstacle_image_default": "defaultobstacle",
        }
        config["visual_feedback"] = {
            "positive_feedback_image_default": "positive",
            "neutral_feedback_image_default": "neutral",
            "negative_feedback_image_default": "negative",
        }
        config["sound_feedback"] = {
            "positive_feedback_sound_default": "hit",
            "neutral_feedback_sound_default": "miss",
            "negative_feedback_sound_default": "error",
        }
        config["interface_settings"] = {
            "palette_default": "0",
            "hud_default": "true",
            "sound_default": "true",
        }

        with open(cls.KARTEA_CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)

    # ===================================================================
    # Listagens
    # ===================================================================
    @classmethod
    def list_images(cls) -> List[str]:
        cls.ensure_kartea_dirs()
        exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}
        return sorted(
            f.name
            for f in cls.KARTEA_IMAGES_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in exts
        )

    @classmethod
    def list_sounds(cls) -> List[str]:
        cls.ensure_kartea_dirs()
        exts = {".wav", ".mp3", ".ogg", ".flac", ".aac"}
        return sorted(
            f.name
            for f in cls.KARTEA_SOUNDS_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in exts
        )

    # ===================================================================
    # Recursos embutidos (Builtin)
    # ===================================================================
    @staticmethod
    def _list_builtin_resources(base_path: str) -> List[tuple[str, str]]:
        result = []
        it = QDirIterator(base_path, QDir.Files, QDirIterator.Subdirectories)
        while it.hasNext():
            path = it.next()
            name = it.fileName()
            result.append((name, path))
        return sorted(result)

    @classmethod
    def list_builtin_vehicle_images(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/images/vehicle")

    @classmethod
    def list_builtin_environment_images(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/images/environment")

    @classmethod
    def list_builtin_obstacle_images(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/images/obstacle")

    @classmethod
    def list_builtin_target_images(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/images/target")

    @classmethod
    def list_builtin_feedback_positive_images(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/images/feedback/positive")

    @classmethod
    def list_builtin_feedback_neutral_images(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/images/feedback/neutral")

    @classmethod
    def list_builtin_feedback_negative_images(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/images/feedback/negative")

    @classmethod
    def list_builtin_feedback_positive_sounds(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/sounds/feedback/positive")

    @classmethod
    def list_builtin_feedback_neutral_sounds(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/sounds/feedback/neutral")

    @classmethod
    def list_builtin_feedback_negative_sounds(cls) -> List[tuple[str, str]]:
        return cls._list_builtin_resources(":/sounds/feedback/negative")
