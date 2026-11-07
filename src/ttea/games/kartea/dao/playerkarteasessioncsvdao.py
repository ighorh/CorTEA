import os
import re
from dataclasses import fields
from datetime import datetime
from typing import Dict, List, Optional, Union

# Local module import
from ttea.dao import DAO, PlayerCsvDAO
from ttea.games.kartea.model import PlayerKarteaSession
from ttea.games.kartea.util import KarteaPathConfig
from ttea.model import Player
from ttea.util import CSVHandler


class PlayerKarteaSessionCsvDAO(DAO):
    """Data Access Object for managing PlayerKarteaSession data in CSV files.

    Implements the DAO interface for CRUD operations on PlayerKarteaSession
    objects, storing all sessions of a player in a single CSV file named
    '{player_id}_{sanitized_name}_kartea_session.csv'. Each row represents
    a session. Maintains an in-memory cache and maps player IDs to filenames.
    Generates incremental IDs for new sessions.

    Attributes
    ----------
    csv_handler : CSVHandler
        Utility for reading and writing CSV files.
    sessions : Dict[int, PlayerKarteaSession]
        Cache of PlayerKarteaSession objects, keyed by session ID.
    file_map : Dict[int, str]
        Maps player IDs to their CSV file paths.
    player_dao : PlayerCsvDAO
        DAO for accessing Player objects.
    next_session_id : int
        Tracks the next available ID for new sessions.
    int_properties : List[str]
        List of property names that should be converted to int from CSV.

    Methods
    -------
    __init__()
        Initializes the DAO and loads existing sessions from CSV files.
    sanitize_filename(name: str) -> str
        Sanitizes a player name for safe file naming.
    get_filename(session: PlayerKarteaSession) -> str
        Generates a filename for a player's sessions.
    load_all_sessions() -> None
        Loads all session data from CSV files into memory.
    insert(obj: PlayerKarteaSession) -> Optional[Union[int, str, bool]]
        Inserts a new session by appending to the player's CSV file.
    update(obj: PlayerKarteaSession) -> Optional[Union[int, bool]]
        Updates a session in the player's CSV file.
    delete(obj_id: int) -> Optional[Union[int, bool]]
        Deletes a session from the player's CSV file.
    select(obj_id: int) -> Optional[PlayerKarteaSession]
        Retrieves a session by its ID.
    list() -> List[PlayerKarteaSession]
        Returns a list of all sessions.
    """

    def __init__(self) -> None:
        """Initialize the PlayerKarteaSessionDAO.

        Sets up the CSV handler, initializes the sessions dictionary, and
        loads existing session data from CSV files into memory.

        Returns
        -------
        None

        Notes
        -----
        Creates necessary directories if they do not exist. Initializes
        next_session_id for incremental ID generation. Infers int_properties
        from PlayerKarteaSession dataclass fields.
        """
        self.csv_handler = CSVHandler()
        self.sessions: Dict[int, PlayerKarteaSession] = {}
        self.file_map: Dict[int, str] = {}  # Maps player_id to filename
        self.player_dao = PlayerCsvDAO()
        self.next_session_id: int = 1

        # Infer int properties dynamically from dataclass fields
        self.int_properties = [
            field.name
            for field in fields(PlayerKarteaSession)
            if field.type == int
        ]

        self.load_all_sessions()

    def sanitize_filename(self, name: str) -> str:
        """Sanitize player name for safe file naming.

        Parameters
        ----------
        name : str
            The player's name to be sanitized.

        Returns
        -------
        str
            A sanitized version of the name for file naming.

        Notes
        -----
        Removes non-alphanumeric characters and converts to lowercase.
        """
        return re.sub(r"[^\w\-]", "_", name.lower().strip())

    def get_filename(self, session: PlayerKarteaSession) -> str:
        """Generate filename using player ID and name.

        Parameters
        ----------
        session : PlayerKarteaSession
            The session object for which to generate a filename.

        Returns
        -------
        str
            The full path to the player's sessions CSV file.

        Notes
        -----
        Uses player ID and sanitized name with '_kartea_session.csv'
        suffix. Uses KarteaPathConfig.players_dir.
        """
        sanitized_name = self.sanitize_filename(session.player.name)
        filename = f"{session.player.id}_{sanitized_name}_kartea_session.csv"
        return str(KarteaPathConfig.players_dir / filename)

    def load_all_sessions(self) -> None:
        """Load all session CSV files into memory.

        Iterates through CSV files in the players directory matching the
        pattern, reads their data, and populates the sessions dictionary.
        Updates next_session_id based on the highest session ID found.

        Notes
        -----
        Assumes CSV files follow the naming convention
        '{player_id}_{sanitized_name}_kartea_session.csv' with multiple
        rows. Extracts player_id from filename.
        """
        KarteaPathConfig.ensure_kartea_dirs()
        for file_path in KarteaPathConfig.KARTEA_PLAYER_DIR.glob(
            "*_*_kartea_session.csv"
        ):
            # Extract player_id from filename
            filename = file_path.stem
            player_id = int(filename.split("_")[0])

            session_data = self.csv_handler.read_csv(
                str(file_path), as_dict=True
            )
            if not session_data:
                continue

            # if not session_data:
            #    session_data = [["id", "1"]]

            # Load full player
            player = self.player_dao.select(player_id)
            if player is None or not player.is_valid():
                player = Player(
                    id=player_id,
                    name="Unknown",
                    birth_date=datetime.now(),
                    observation="",
                )

            for row in session_data:
                session_id = int(row["id"])
                # Update next_session_id
                self.next_session_id = max(
                    self.next_session_id, session_id + 1
                )

                # Ensure data types are converted appropriately
                session_kwargs = {
                    prop: (
                        int(row[prop])
                        if prop in self.int_properties
                        else row[prop]
                    )
                    for prop in PlayerKarteaSession.PROPERTIES
                    if prop != "player" and prop in row
                }

                session = PlayerKarteaSession(
                    id=session_id, player=player, **session_kwargs
                )
                self.sessions[session_id] = session
                self.file_map[player_id] = str(file_path)

    def insert(
        self, obj: PlayerKarteaSession
    ) -> Optional[Union[int, str, bool]]:
        """Insert a new session by appending to the player's CSV file.

        Parameters
        ----------
        obj : PlayerKarteaSession
            The session object to be inserted, with player as Player.

        Returns
        -------
        Optional[Union[int, str, bool]]
            The assigned session ID if successful, False if invalid.

        Notes
        -----
        Assigns an incremental ID to the session. Appends a new row to
        the player's CSV file. Uses PROPERTIES for serialization, storing
        player.id for 'player'.
        """
        if not obj.player or not obj.player.is_valid():
            return False

        # Assign incremental ID
        session_id = self.next_session_id
        self.next_session_id += 1
        obj.id = session_id

        filename = self.get_filename(obj)
        self.file_map[obj.player.id] = filename

        # Prepare data, storing player.id for 'player'
        session_data = [
            {
                prop: getattr(obj, prop) if prop != "player" else obj.player.id
                for prop in PlayerKarteaSession.PROPERTIES
            }
        ]

        # Append to CSV (or create if not exists)
        if os.path.exists(filename):
            existing_data = self.csv_handler.read_csv(filename, as_dict=True)
            session_data = existing_data + session_data
        self.csv_handler.write_csv(
            filename,
            session_data,
            headers=PlayerKarteaSession.PROPERTIES,
        )

        # Update cache
        self.sessions[session_id] = obj
        return session_id

    def update(self, obj: PlayerKarteaSession) -> Optional[Union[int, bool]]:
        """Update a session in the player's CSV file.

        Parameters
        ----------
        obj : PlayerKarteaSession
            The session object with updated data, with player as Player.

        Returns
        -------
        Optional[Union[int, bool]]
            True if update is successful, False if invalid or not found.

        Notes
        -----
        Uses data from file as base, updates the specific row for obj.id.
        Renames the file if player name changed. Uses PROPERTIES for
        serialization, storing player.id for 'player'.
        """
        if obj.id not in self.sessions:
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

        # Update cache first
        self.sessions[obj.id] = obj

        # Load existing data from file (base)
        filename = new_filename or self.get_filename(obj)
        if os.path.exists(filename):
            all_data = self.csv_handler.read_csv(filename, as_dict=True)
        else:
            all_data = []

        # Prepare updated row for obj.id
        updated_row = {
            prop: getattr(obj, prop) if prop != "player" else obj.player.id
            for prop in PlayerKarteaSession.PROPERTIES
        }

        # Update or add the row in all_data
        updated = False
        for i, row in enumerate(all_data):
            if int(row.get("id", 0)) == obj.id:
                all_data[i] = updated_row
                updated = True
                break
        if not updated:
            all_data.append(updated_row)

        # Write updated data to CSV
        self.csv_handler.write_csv(
            filename,
            all_data,
            headers=PlayerKarteaSession.PROPERTIES,
        )
        return True

    def delete(self, obj_id: int) -> Optional[Union[int, bool]]:
        """Delete a session from the player's CSV file.

        Parameters
        ----------
        obj_id : int
            The ID of the session to delete.

        Returns
        -------
        Optional[Union[int, bool]]
            True if deletion is successful, False if session not found.

        Notes
        -----
        Rewrites the player's CSV file excluding the session row.
        Removes the file if it becomes empty.
        """
        if obj_id not in self.sessions:
            return False

        player_id = self.sessions[obj_id].player.id
        filename = self.file_map.get(player_id)
        if not filename:
            return False

        # Remove from cache
        del self.sessions[obj_id]

        # Load existing sessions and exclude the deleted one
        session_data = []
        if os.path.exists(filename):
            session_data = [
                row
                for row in self.csv_handler.read_csv(filename, as_dict=True)
                if int(row["id"]) != obj_id
            ]

        # If no sessions remain, delete the file
        if not session_data:
            if os.path.exists(filename):
                os.remove(filename)
            if player_id in self.file_map:
                del self.file_map[player_id]
            return True

        # Write remaining sessions to CSV
        self.csv_handler.write_csv(
            filename,
            session_data,
            headers=PlayerKarteaSession.PROPERTIES,
        )
        return True

    def select(self, obj_id: int) -> Optional[PlayerKarteaSession]:
        """Retrieve a session by ID.

        Parameters
        ----------
        obj_id : int
            The ID of the session to retrieve.

        Returns
        -------
        Optional[PlayerKarteaSession]
            The PlayerKarteaSession object if found, None otherwise.

        Notes
        -----
        Retrieves from the in-memory cache.
        """
        return self.sessions.get(obj_id)

    def list(self) -> List[PlayerKarteaSession]:
        """List all sessions.

        Returns
        -------
        List[PlayerKarteaSession]
            A list of all PlayerKarteaSession objects in the cache.

        Notes
        -----
        Returns a list of all sessions currently loaded in memory.
        """
        return list(self.sessions.values())
