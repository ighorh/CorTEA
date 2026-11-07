import os
import re
from dataclasses import fields
from typing import Dict, List, Optional, Union

# Local module imports
from ttea.dao import DAO
from ttea.dao.playercsvdao import PlayerCsvDAO
from ttea.games.kartea.model import (KarteaPhase, KarteaPhaseLevel,
                                     PlayerKarteaConfig)
from ttea.games.kartea.util.karteapathconfig import KarteaPathConfig
from ttea.util import CSVHandler


class PlayerKarteaConfigCsvDAO(DAO):
    """Data Access Object for managing PlayerKarteaConfig data in CSV files.

    Implements the DAO interface to handle CRUD operations for PlayerKarteaConfig
    objects, storing data in CSV files per player. Each configuration has a
    separate CSV file named '{player_id}_{sanitized_name}_kartea_config.csv'.
    Uses auxiliary DAOs to manage Player, PlayerKarteaSession, KarteaPhase, and
    KarteaPhaseLevel objects, maintaining caches for efficient access.

    Attributes
    ----------
    csv_handler : CSVHandler
        Utility for reading and writing CSV files.
    configs : Dict[int, PlayerKarteaConfig]
        In-memory cache of PlayerKarteaConfig objects, keyed by player ID.
    file_map : Dict[int, str]
        Maps player IDs to their corresponding CSV file paths.
    player_dao : PlayerCsvDAO
        DAO for accessing Player objects.
    session_dao : PlayerKarteaSessionCsvDAO
        DAO for accessing PlayerKarteaSession objects.
    phase_dao : KarteaPhaseCsvDAO
        DAO for accessing KarteaPhase objects.
    level_dao : KarteaPhaseLevelCsvDAO
        DAO for accessing KarteaPhaseLevel objects.
    phases : Dict[int, KarteaPhase]
        Cache of KarteaPhase objects, keyed by phase ID.
    levels : Dict[int, KarteaPhaseLevel]
        Cache of KarteaPhaseLevel objects, keyed by level ID.
    int_properties : List[str]
        List of property names that should be converted to int from CSV.
    bool_properties : List[str]
        List of property names that should be converted to bool from CSV.
    """

    def __init__(self) -> None:
        """Initialize the PlayerKarteaConfigCsvDAO.

        Sets up the CSV handler, initializes caches, and loads all existing
        configuration data and phase/level data using auxiliary DAOs.

        Returns
        -------
        None

        Notes
        -----
        Creates necessary directories if they do not exist. Infers int and bool
        properties dynamically from PlayerKarteaConfig dataclass fields.
        """
        from ttea.games.kartea.dao import (KarteaPhaseCsvDAO,
                                           KarteaPhaseLevelCsvDAO,
                                           PlayerKarteaSessionCsvDAO)

        self.csv_handler = CSVHandler()
        self.configs: Dict[int, PlayerKarteaConfig] = {}
        self.file_map: Dict[int, str] = {}
        self.player_dao = PlayerCsvDAO()
        self.session_dao = PlayerKarteaSessionCsvDAO()
        self.phase_dao = KarteaPhaseCsvDAO()
        self.level_dao = KarteaPhaseLevelCsvDAO()
        self.phases: Dict[int, KarteaPhase] = {}
        self.levels: Dict[int, KarteaPhaseLevel] = {}

        # Infer int and bool properties dynamically from dataclass fields
        self.int_properties = [
            field.name
            for field in fields(PlayerKarteaConfig)
            if field.type == int
        ]
        self.bool_properties = [
            field.name
            for field in fields(PlayerKarteaConfig)
            if field.type == bool
        ]

        self.load_phases_and_levels()
        self.load_all_configs()

    def sanitize_filename(self, name: str) -> str:
        """Sanitize name for safe file naming.

        Parameters
        ----------
        name : str
            The name to be sanitized.

        Returns
        -------
        str
            A sanitized version of the name suitable for file naming.

        Notes
        -----
        Removes non-alphanumeric characters and converts to lowercase.
        """
        return re.sub(r"[^\w\-]", "_", name.lower().strip())

    def get_filename(self, config: PlayerKarteaConfig) -> str:
        """Generate filename using player ID and name.

        Parameters
        ----------
        config : PlayerKarteaConfig
            The configuration object for which to generate a filename.

        Returns
        -------
        str
            The full path to the player's configuration CSV file.

        Notes
        -----
        Uses player ID and sanitized name with '_kartea_config.csv' suffix.
        Uses KarteaPathConfig.players_dir.
        """
        sanitized_name = self.sanitize_filename(config.player.name)
        filename = f"{config.player.id}_{sanitized_name}_kartea_config.csv"
        return str(KarteaPathConfig.KARTEA_PLAYER_DIR / filename)

    def load_phases_and_levels(self) -> None:
        """Load all KarteaPhase and KarteaPhaseLevel objects using phase_dao and level_dao.

        Populates the phases and levels caches from CSV files in kartea_phases_dir.

        Notes
        -----
        Uses phase_dao.list() to load all phases and their associated levels.
        Populates levels cache by iterating through each phase's level list.
        """
        KarteaPathConfig.ensure_kartea_dirs()
        self.phases = {phase.id: phase for phase in self.phase_dao.list()}
        self.levels = {}
        for phase in self.phases.values():
            for level in phase.level_list:
                self.levels[level.id] = level

    def get_phase(self, phase_id: int) -> Optional[KarteaPhase]:
        """Retrieve a KarteaPhase by its ID using phase_dao.

        Parameters
        ----------
        phase_id : int
            The ID of the phase to retrieve.

        Returns
        -------
        Optional[KarteaPhase]
            The KarteaPhase object if found, None otherwise.
        """
        return self.phase_dao.select(phase_id)

    def get_level(
        self, phase_id: int, level_id: int
    ) -> Optional[KarteaPhaseLevel]:
        """Retrieve a KarteaPhaseLevel by its ID using level_dao.

        Parameters
        ----------
        level_id : int
            The ID of the level to retrieve.

        Returns
        -------
        Optional[KarteaPhaseLevel]
            The KarteaPhaseLevel object if found, None otherwise.
        """
        return self.level_dao.select(phase_id, level_id)

    def load_all_configs(self) -> None:
        """Load all configuration CSV files into memory.

        Iterates through CSV files in the players directory matching the pattern,
        reads their data, reconstructs references using auxiliary DAOs, and
        populates the configs dictionary.

        Notes
        -----
        Assumes CSV files follow the naming convention
        '{player_id}_{sanitized_name}_kartea_config.csv'. Extracts player_id
        from filename. Uses player_dao, session_dao, phase_dao, and level_dao
        to reconstruct references.
        """
        KarteaPathConfig.ensure_kartea_dirs()
        for file_path in KarteaPathConfig.KARTEA_PLAYER_DIR.glob(
            "*_*_kartea_config.csv"
        ):
            # Extract player_id from filename
            filename = file_path.stem
            player_id = int(filename.split("_")[0])

            config_data = self.csv_handler.read_csv(
                str(file_path), as_dict=True
            )
            if not config_data:
                continue

            row = config_data[0]  # Single row per file

            # Load full player
            player = self.player_dao.select(player_id)
            if not player:
                continue

            # Get session
            session = None
            if "session" in row and row["session"]:
                session_id = (
                    int(row["session"]) if row["session"].isdigit() else None
                )
                if session_id:
                    session = self.session_dao.select(session_id)

            # Get phase and level
            phase = None
            level = None
            if "phase" in row and row["phase"]:
                phase_id = (
                    int(row["phase"]) if row["phase"].isdigit() else None
                )
                if phase_id:
                    phase = self.get_phase(phase_id)
                    if "level" in row and row["level"]:
                        level_id = (
                            int(row["level"])
                            if row["level"].isdigit()
                            else None
                        )
                        if level_id:
                            level = self.get_level(phase_id, level_id)
                            if level and level.phase.id != phase.id:
                                level = None  # Ensure level belongs to phase

            # Build config kwargs
            config_kwargs = {}
            for prop in PlayerKarteaConfig.PROPERTIES:
                if prop == "id":
                    config_kwargs[prop] = player_id
                elif prop == "player":
                    config_kwargs[prop] = player
                elif prop == "session":
                    config_kwargs[prop] = session
                elif prop == "phase":
                    config_kwargs[prop] = phase
                elif prop == "level":
                    config_kwargs[prop] = level
                elif prop in row:
                    # Convert based on property type
                    if prop in self.int_properties:
                        config_kwargs[prop] = (
                            int(row[prop]) if row[prop].isdigit() else 0
                        )
                    elif prop in self.bool_properties:
                        config_kwargs[prop] = row[prop].lower() == "true"
                    else:
                        config_kwargs[prop] = row[prop]

            config = PlayerKarteaConfig(**config_kwargs)
            self.configs[player_id] = config
            self.file_map[player_id] = str(file_path)

    def insert(
        self, obj: PlayerKarteaConfig
    ) -> Optional[Union[int, str, bool]]:
        """Insert a new configuration by creating or updating the player's CSV file.

        Parameters
        ----------
        obj : PlayerKarteaConfig
            The configuration object to be inserted.

        Returns
        -------
        Optional[Union[int, str, bool]]
            The player ID if successful, False if invalid.

        Notes
        -----
        Creates or overwrites the player's CSV file with a single row.
        Uses PROPERTIES for serialization, storing IDs for references.
        """
        if not obj.player or not obj.player.is_valid():
            return False

        config_id = obj.player.id  # Use player ID as config ID
        filename = self.get_filename(obj)
        self.file_map[config_id] = filename

        # Prepare data using PROPERTIES, storing IDs for references
        data = {
            prop: (
                getattr(obj, prop).id
                if prop in ["player", "session", "phase", "level"]
                and getattr(obj, prop)
                else getattr(obj, prop)
            )
            for prop in PlayerKarteaConfig.PROPERTIES
        }

        # Write to CSV (single row per player)
        self.csv_handler.write_csv(
            filename, [data], headers=PlayerKarteaConfig.PROPERTIES
        )

        # Update cache
        self.configs[config_id] = obj
        return config_id

    def update(self, obj: PlayerKarteaConfig) -> Optional[Union[int, bool]]:
        """Update configuration in the player's CSV file.

        Parameters
        ----------
        obj : PlayerKarteaConfig
            The configuration object with updated data.

        Returns
        -------
        Optional[Union[int, bool]]
            True if update is successful, False if invalid or not found.

        Notes
        -----
        Overwrites the player's CSV file with the updated configuration.
        Renames the file if player name changed. Uses PROPERTIES for
        serialization, storing IDs for references.
        """
        if obj.player.id not in self.configs:
            return False

        if not obj.player or not obj.player.is_valid():
            return False

        old_filename = self.file_map.get(obj.player.id)
        new_filename = self.get_filename(obj)

        # If player name changed, rename the file
        if old_filename and old_filename != new_filename:
            if os.path.exists(old_filename):
                os.rename(old_filename, new_filename)
            self.file_map[obj.player.id] = new_filename

        # Update cache
        self.configs[obj.player.id] = obj

        # Prepare updated row using PROPERTIES
        updated_row = {
            prop: (
                getattr(obj, prop).id
                if prop in ["player", "session", "phase", "level"]
                and getattr(obj, prop)
                else getattr(obj, prop)
            )
            for prop in PlayerKarteaConfig.PROPERTIES
        }

        # Write updated data to CSV
        self.csv_handler.write_csv(
            new_filename, [updated_row], headers=PlayerKarteaConfig.PROPERTIES
        )
        return True

    def delete(self, obj_id: int) -> Optional[Union[int, bool]]:
        """Delete configuration from memory and remove its CSV file.

        Parameters
        ----------
        obj_id : int
            The ID of the configuration to delete (player ID).

        Returns
        -------
        Optional[Union[int, bool]]
            True if deletion is successful, False if configuration not found.
        """
        if obj_id not in self.configs:
            return False
        filename = self.file_map.get(obj_id)
        del self.configs[obj_id]
        del self.file_map[obj_id]
        if filename and os.path.exists(filename):
            os.remove(filename)
            return True
        return False

    def select(self, obj_id: int) -> Optional[PlayerKarteaConfig]:
        """Retrieve a configuration by ID.

        Parameters
        ----------
        obj_id : int
            The ID of the configuration to retrieve (player ID).

        Returns
        -------
        Optional[PlayerKarteaConfig]
            The PlayerKarteaConfig object if found, None otherwise.
        """
        return self.configs.get(obj_id)

    def list(self) -> List[PlayerKarteaConfig]:
        """List all configurations.

        Returns
        -------
        List[PlayerKarteaConfig]
            A list containing all PlayerKarteaConfig objects in the cache.
        """
        return list(self.configs.values())

    def get_all_phases(self) -> List[KarteaPhase]:
        """Retrieve a list of all available KarteaPhase objects.

        Returns
        -------
        List[KarteaPhase]
            Sorted list of KarteaPhase objects by ID, retrieved from phase_dao.
        """
        return self.phase_dao.list()

    def get_levels_for_phase(
        self, phase: Union[int, KarteaPhase]
    ) -> List[KarteaPhaseLevel]:
        """Retrieve the list of KarteaPhaseLevel objects for a specific phase.

        Parameters
        ----------
        phase : Union[int, KarteaPhase]
            The phase ID or KarteaPhase object to retrieve levels for.

        Returns
        -------
        List[KarteaPhaseLevel]
            List of KarteaPhaseLevel objects for the phase, or empty list if not found.
        """
        if isinstance(phase, int):
            phase = self.get_phase(phase)
        if not phase:
            return []
        return phase.level_list
