import os
import re
from dataclasses import fields
from datetime import datetime
from typing import Dict, List, Optional

import portalocker

# Local module import
from ttea.dao import DAO
from ttea.model import Player
from ttea.util import CSVHandler, PathConfig


class PlayerCsvDAO(DAO[Player]):
    """Specialized DAO for Player entities using CSV files
    with in-memory cache.

    Persists each Player in an individual CSV file named after its ID and
    sanitized name. Keeps all players loaded in memory for fast access and
    uses file locking to prevent concurrent write issues.

    Attributes
    ----------
    csv_handler : CSVHandler
        Utility for reading/writing CSV data.
    players : Dict[int, Player]
        In-memory cache mapping player IDs to Player instances.
    file_map : Dict[int, str]
        Maps player IDs to their corresponding CSV file paths.
    int_properties : List[str]
        Names of Player fields that are integers.
    bool_properties : List[str]
        Names of Player fields that are booleans.

    Methods
    -------
    __init__()
        Initializes the DAO and loads all existing players from disk.
    insert(obj)
        Persists a new player and returns its assigned ID.
    update(obj)
        Updates an existing player, handling filename changes if needed.
    delete(obj_id)
        Removes a player and its associated CSV file.
    select(obj_id)
        Retrieves a player by ID from the in-memory cache.
    list()
        Returns all players currently loaded.
    """

    def __init__(self) -> None:
        """Initialize the DAO and load all players from CSV files."""
        self.csv_handler = CSVHandler()
        self.players: Dict[int, Player] = {}
        self.file_map: Dict[int, str] = {}
        self.int_properties = [f.name for f in fields(Player) if f.type == int]
        self.bool_properties = [
            f.name for f in fields(Player) if f.type == bool
        ]
        self.load_all_players()

    def generate_next_id(self) -> int:
        """Generate the next available player ID.

        Returns
        -------
        int
            The next unused ID (1 if no players exist).
        """
        if not self.players:
            return 1
        return max(self.players.keys()) + 1

    def write_with_lock(
        self, filepath: str, data: List[Dict], headers: List[str]
    ):
        """Write data to a CSV file with exclusive file locking.

        Parameters
        ----------
        filepath : str
            Full path to the target CSV file.
        data : List[Dict]
            List of dictionaries representing rows to write.
        headers : List[str]
            Ordered list of column names.
        """
        PathConfig.ensure_dirs()
        with portalocker.Lock(filepath, mode="w", timeout=10) as f:
            self.csv_handler.write_csv(f, data, headers)

    def insert(self, obj: Player) -> int:
        """Insert a new player into persistent storage.

        Parameters
        ----------
        obj : Player
            The player instance to persist.

        Returns
        -------
        int
            The assigned player ID on success, 0 on failure (invalid player
            or ID already exists).
        """
        if not obj.is_valid():
            return 0

        # Generate ID if not set
        if obj.id <= 0:
            obj.id = self.generate_next_id()

        if obj.id in self.players:
            return 0

        self.players[obj.id] = obj
        filename = self.get_filename(obj)
        self.file_map[obj.id] = filename
        self.write_with_lock(filename, obj.get_data(), Player.PROPERTIES)
        return obj.id

    def update(self, obj: Player) -> bool:
        """Update an existing player in persistent storage.

        Renames the file if the player's name changed.

        Parameters
        ----------
        obj : Player
            The player with updated values.

        Returns
        -------
        bool
            True if updated successfully, False otherwise.
        """
        if not obj.is_valid() or obj.id not in self.players:
            return False

        old_filename = self.file_map.get(obj.id)
        new_filename = self.get_filename(obj)

        if old_filename != new_filename and os.path.exists(old_filename):
            os.rename(old_filename, new_filename)

        self.players[obj.id] = obj
        self.file_map[obj.id] = new_filename
        self.write_with_lock(new_filename, obj.get_data(), Player.PROPERTIES)
        return True

    def delete(self, obj_id: int) -> bool:
        """Delete a player and remove its CSV file.

        Parameters
        ----------
        obj_id : int
            ID of the player to delete.

        Returns
        -------
        bool
            True if deleted, False if the player was not found.
        """
        if obj_id not in self.players:
            return False

        filename = self.file_map.pop(obj_id, None)
        self.players.pop(obj_id, None)

        if filename and os.path.exists(filename):
            os.remove(filename)
        return True

    def select(self, obj_id: int) -> Optional[Player]:
        """Retrieve a player by ID from the in-memory cache.

        Parameters
        ----------
        obj_id : int
            The player ID to look up.

        Returns
        -------
        Optional[Player]
            The Player instance if found, None otherwise.
        """
        return self.players.get(obj_id)

    def list(self) -> List[Player]:
        """Return all loaded players.

        Returns
        -------
        List[Player]
            A list of all Player instances currently in memory.
        """
        return list(self.players.values())

    def sanitize_filename(self, name: str) -> str:
        """Sanitize a player name for safe use in filenames.

        Parameters
        ----------
        name : str
            Original player name.

        Returns
        -------
        str
            Sanitized name (lowercase, non-alphanumeric replaced by '_').
        """
        return re.sub(r"[^\w\-]", "_", name.lower().strip())

    def get_filename(self, player: Player) -> str:
        """Generate the full path for a player's CSV file.

        Parameters
        ----------
        player : Player
            The player object.

        Returns
        -------
        str
            Complete file path using pattern: <id>_<sanitized_name>_player.csv
        """
        sanitized_name = self.sanitize_filename(player.name)
        filename = f"{player.id}_{sanitized_name}_player.csv"
        return PathConfig.player(filename)

    def load_all_players(self) -> None:
        """Load every player CSV file from disk into memory.

        Scans the players directory, parses each matching CSV file,
        converts data types appropriately, and populates the cache.
        """
        PathConfig.ensure_dirs()
        for file_path in PathConfig.PLAYERS_DIR.glob("*_player.csv"):
            player_data = self.csv_handler.read_csv(
                str(file_path), as_dict=True
            )
            if not player_data:
                continue

            row = player_data[0]
            # Build player kwargs with type conversions
            player_kwargs = {}
            for prop in Player.PROPERTIES:
                if prop in row:
                    if prop == "birth_date" and row[prop]:
                        player_kwargs[prop] = datetime.fromisoformat(row[prop])
                    elif prop in self.int_properties:
                        player_kwargs[prop] = (
                            int(row[prop]) if row[prop].isdigit() else 0
                        )
                    elif prop in self.bool_properties:
                        player_kwargs[prop] = row[prop].lower() == "true"
                    else:
                        player_kwargs[prop] = row[prop]

            player = Player(**player_kwargs)
            self.players[player.id] = player
            self.file_map[player.id] = str(file_path)

    def search_players(self, query: str = "") -> List[Player]:
        """Retorna a lista de jogadores, opcionalmente filtrada."""
        all_players = list(self.players.values())

        if not query.strip():
            return all_players

        q = query.lower().strip()
        return [
            p for p in all_players if q in str(p.id) or q in p.name.lower()
        ]
