import os
import re
from dataclasses import fields
from datetime import datetime
from typing import Dict, List, Optional, Union

# Local module import
from ttea.dao import DAO
from ttea.games.kartea.dao import PlayerKarteaSessionCsvDAO
from ttea.games.kartea.model import (PlayerKarteaSession,
                                     PlayerKarteaSessionDetail)
from ttea.games.kartea.util import KarteaPathConfig
from ttea.model import Player
from ttea.util import CSVHandler


class PlayerKarteaSessionDetailCsvDAO(DAO):
    """Data Access Object for managing PlayerKarteaSessionDetail data
    in CSV files.

    Implements the DAO interface for CRUD operations on
    PlayerKarteaSessionDetail objects, storing all details of a player
    in a single CSV file named '{player_id}_{sanitized_name}_kartea_session_
    detail.csv'. Each row represents a session detail. Maintains an
    in-memory cache and maps player IDs to filenames. Generates incremental
    IDs for new session details.

    Attributes
    ----------
    csv_handler : CSVHandler
        Utility for reading and writing CSV files.
    details : Dict[int, PlayerKarteaSessionDetail]
        Cache of PlayerKarteaSessionDetail objects, keyed by detail ID.
    file_map : Dict[int, str]
        Maps player IDs to their CSV file paths.
    session_dao : PlayerKarteaSessionCsvDAO
        DAO for accessing PlayerKarteaSession objects.
    next_detail_id : int
        Tracks the next available ID for new session details.
    int_properties : List[str]
        List of property names that should be converted to int from CSV.

    Methods
    -------
    __init__()
        Initializes the DAO and loads existing session details from CSV files.
    sanitize_filename(name: str) -> str
        Sanitizes a player name for safe file naming.
    get_filename(detail: PlayerKarteaSessionDetail) -> str
        Generates a filename for a player's session details.
    load_all_details() -> None
        Loads all session detail data from CSV files into memory.
    insert(obj: PlayerKarteaSessionDetail) -> Optional[Union[int, str, bool]]
        Inserts a new session detail by appending to the player's CSV file.
    update(obj: PlayerKarteaSessionDetail) -> Optional[Union[int, bool]]
        Updates a session detail in the player's CSV file.
    delete(obj_id: int) -> Optional[Union[int, bool]]
        Deletes a session detail from the player's CSV file.
    select(obj_id: int) -> Optional[PlayerKarteaSessionDetail]
        Retrieves a session detail by its ID.
    list() -> List[PlayerKarteaSessionDetail]
        Returns a list of all session details.
    """

    def __init__(self) -> None:
        """Initialize the PlayerKarteaSessionDetailDAO.

        Sets up the CSV handler, initializes the details dictionary, and loads
        existing session detail data from CSV files into memory.

        Returns
        -------
        None

        Notes
        -----
        Creates necessary directories if they do not exist. Initializes
        next_detail_id for incremental ID generation. Infers int_properties
        from PlayerKarteaSessionDetail dataclass fields.
        """
        self.csv_handler = CSVHandler()
        self.details: Dict[int, PlayerKarteaSessionDetail] = {}
        self.file_map: Dict[int, str] = {}  # Maps player_id to filename
        self.session_dao = PlayerKarteaSessionCsvDAO()
        self.next_detail_id: int = 1

        # Infer int properties dynamically from dataclass fields
        self.int_properties = [
            field.name
            for field in fields(PlayerKarteaSessionDetail)
            if field.type == int
        ]

        self.load_all_details()

    def sanitize_filename(self, name: str) -> str:
        """Sanitize player name for safe file naming.

        Parameters
        ----------
        name : str
            The player's name to be sanitized.

        Returns
        -------
        str
            A sanitized version of the name suitable for file naming.

        Notes
        -----
        Removes non-alphanumeric characters and converts to lowercase.
        """
        return re.sub(r"[^\w\-]", "_", name.lower().strip())

    def get_filename(self, detail: PlayerKarteaSessionDetail) -> str:
        """Generate filename using player ID and name.

        Parameters
        ----------
        detail : PlayerKarteaSessionDetail
            The session detail object for which to generate a filename.

        Returns
        -------
        str
            The full path to the player's session details CSV file.

        Notes
        -----
        Uses player ID and sanitized name with '_kartea_session_detail.csv'
        suffix. Uses KarteaPathConfig.players_dir.
        """
        sanitized_name = self.sanitize_filename(detail.session.player.name)
        filename = (
            f"{detail.session.player.id}_{sanitized_name}_"
            f"kartea_session_detail.csv"
        )
        return str(KarteaPathConfig.players_dir / filename)

    def load_all_details(self) -> None:
        """Load all session detail CSV files into memory.

        Iterates through CSV files in the players directory matching the
        pattern, reads their data, and populates the details dictionary.
        Updates next_detail_id based on the highest detail ID found.

        Notes
        -----
        Assumes CSV files follow the naming convention
        '{player_id}_{sanitized_name}_kartea_session_detail.csv' with multiple
        rows. Extracts player_id from filename. Loads session via
        PlayerKarteaSessionDAO, with fallback if session not found.
        """
        KarteaPathConfig.create_directories()
        for file_path in KarteaPathConfig.players_dir.glob(
            "*_*_kartea_session_detail.csv"
        ):
            # Extract player_id from filename
            filename = file_path.stem
            player_id = int(filename.split("_")[0])

            detail_data = self.csv_handler.read_csv(
                str(file_path), as_dict=True
            )
            if not detail_data:
                continue

            for row in detail_data:
                detail_id = int(row["id"])
                # Update next_detail_id
                self.next_detail_id = max(self.next_detail_id, detail_id + 1)

                # Extract session_id from row
                session_id = int(row["session"])

                # Load session via PlayerKarteaSessionDAO
                session = self.session_dao.select(session_id)
                if session is None:
                    # Fallback if session not found
                    session = PlayerKarteaSession(
                        id=session_id,
                        player=Player(
                            id=player_id,
                            name="Unknown",
                            birth_date=datetime.now(),
                            observation="",
                        ),
                        date="",
                        start_time="",
                        end_time="",
                        phase_reached=0,
                        level_reached=0,
                        general_score=0,
                        q_movement=0,
                        q_collided_target=0,
                        q_avoided_target=0,
                        q_collided_obstacle=0,
                        q_avoided_obstacle=0,
                    )

                # Ensure data types are converted appropriately
                detail_kwargs = {
                    prop: (
                        int(row[prop])
                        if prop in self.int_properties
                        else row[prop]
                    )
                    for prop in PlayerKarteaSessionDetail.PROPERTIES
                    if prop != "session" and prop in row
                }

                detail = PlayerKarteaSessionDetail(
                    id=detail_id, session=session, **detail_kwargs
                )
                self.details[detail_id] = detail
                self.file_map[player_id] = str(file_path)

    def insert(
        self, obj: PlayerKarteaSessionDetail
    ) -> Optional[Union[int, str, bool]]:
        """Insert a new session detail by appending to the player's CSV file.

        Parameters
        ----------
        obj : PlayerKarteaSessionDetail
            The session detail object to be inserted, with session as
            PlayerKarteaSession.

        Returns
        -------
        Optional[Union[int, str, bool]]
            The assigned detail ID if successful, False if invalid.

        Notes
        -----
        Assigns an incremental ID to the session detail. Appends a new row
        to the player's CSV file. Uses PROPERTIES for serialization, storing
        session.id for 'session'.
        """
        if (
            not obj.session
            or not obj.session.player
            or not obj.session.player.is_valid()
        ):
            return False

        # Assign incremental ID
        detail_id = self.next_detail_id
        self.next_detail_id += 1
        obj.id = detail_id  # Update object with new ID

        filename = self.get_filename(obj)
        self.file_map[obj.session.player.id] = filename

        # Prepare data using PROPERTIES, storing session.id for 'session'
        detail_data_list = [
            {
                prop: (
                    getattr(obj, prop) if prop != "session" else obj.session.id
                )
                for prop in PlayerKarteaSessionDetail.PROPERTIES
            }
        ]

        # Append to CSV (or create if not exists)
        if os.path.exists(filename):
            existing_data = self.csv_handler.read_csv(filename, as_dict=True)
            detail_data_list = existing_data + detail_data_list
        self.csv_handler.write_csv(
            filename,
            detail_data_list,
            headers=PlayerKarteaSessionDetail.PROPERTIES,
        )

        # Update cache
        self.details[detail_id] = obj
        return detail_id

    def update(
        self, obj: PlayerKarteaSessionDetail
    ) -> Optional[Union[int, bool]]:
        """Update a session detail in the player's CSV file.

        Parameters
        ----------
        obj : PlayerKarteaSessionDetail
            The session detail object with updated data, with session as
            PlayerKarteaSession.

        Returns
        -------
        Optional[Union[int, bool]]
            True if update is successful, False if invalid or not found.

        Notes
        -----
        Uses data from file as base, updates the specific row for obj.id.
        Renames the file if player name changed. Uses PROPERTIES for
        serialization, storing session.id for 'session'.
        """
        if obj.id not in self.details:
            return False

        # Validate session
        if (
            not obj.session
            or not obj.session.player
            or not obj.session.player.is_valid()
        ):
            return False

        old_filename = self.file_map.get(obj.session.player.id)
        new_filename = self.get_filename(obj)

        # If player name changed, rename the file
        if old_filename and old_filename != new_filename:
            if os.path.exists(old_filename):
                os.rename(old_filename, new_filename)
            self.file_map[obj.session.player.id] = new_filename

        # Update cache first
        self.details[obj.id] = obj

        # Load existing data from file (base)
        filename = new_filename or self.get_filename(obj)
        if os.path.exists(filename):
            all_data = self.csv_handler.read_csv(filename, as_dict=True)
        else:
            all_data = []

        # Prepare updated row for obj.id
        updated_row = {
            prop: (getattr(obj, prop) if prop != "session" else obj.session.id)
            for prop in PlayerKarteaSessionDetail.PROPERTIES
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
            headers=PlayerKarteaSessionDetail.PROPERTIES,
        )
        return True

    def delete(self, obj_id: int) -> Optional[Union[int, bool]]:
        """Delete a session detail from the player's CSV file.

        Parameters
        ----------
        obj_id : int
            The ID of the session detail to delete.

        Returns
        -------
        Optional[Union[int, bool]]
            True if deletion is successful, False if detail not found.

        Notes
        -----
        Rewrites the player's CSV file excluding the session detail row.
        Removes the file if it becomes empty.
        """
        if obj_id not in self.details:
            return False

        player_id = self.details[obj_id].session.player.id
        filename = self.file_map.get(player_id)
        if not filename:
            return False

        # Remove from cache
        del self.details[obj_id]

        # Load existing details and exclude the deleted one
        detail_data = []
        if os.path.exists(filename):
            detail_data = [
                row
                for row in self.csv_handler.read_csv(filename, as_dict=True)
                if int(row["id"]) != obj_id
            ]

        # If no details remain, delete the file
        if not detail_data:
            if os.path.exists(filename):
                os.remove(filename)
            if player_id in self.file_map:
                del self.file_map[player_id]
            return True

        # Write remaining details to CSV
        self.csv_handler.write_csv(
            filename,
            detail_data,
            headers=PlayerKarteaSessionDetail.PROPERTIES,
        )
        return True

    def select(self, obj_id: int) -> Optional[PlayerKarteaSessionDetail]:
        """Retrieve a session detail by ID.

        Parameters
        ----------
        obj_id : int
            The ID of the session detail to retrieve.

        Returns
        -------
        Optional[PlayerKarteaSessionDetail]
            The PlayerKarteaSessionDetail object if found, None otherwise.

        Notes
        -----
        Retrieves from the in-memory cache.
        """
        return self.details.get(obj_id)

    def list(self) -> List[PlayerKarteaSessionDetail]:
        """List all session details.

        Returns
        -------
        List[PlayerKarteaSessionDetail]
            A list containing all PlayerKarteaSessionDetail objects
            in the cache.

        Notes
        -----
        Returns a list of all session details currently loaded in memory.
        """
        return list(self.details.values())
