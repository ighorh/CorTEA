import os
import re
from dataclasses import fields
from typing import Dict, List, Optional

import portalocker

# Local module import
from ttea.dao import DAO
from ttea.model import InstitutionFacility
from ttea.util import CSVHandler, PathConfig


class InstitutionFacilityCsvDAO(DAO[InstitutionFacility]):
    """Specialized DAO for institutionfacility entities using CSV files
    with in-memory cache.
    """

    def __init__(self) -> None:
        """Initialize the DAO and load all institutionfacilities
        from CSV files."""
        self.csv_handler = CSVHandler()
        self.institutionfacilities: Dict[int, InstitutionFacility] = {}
        self.file_map: Dict[int, str] = {}
        self.int_properties = [
            f.name for f in fields(InstitutionFacility) if f.type == int
        ]
        self.bool_properties = [
            f.name for f in fields(InstitutionFacility) if f.type == bool
        ]
        self.load_all_institutionfacilities()

    def generate_next_id(self) -> int:
        """Generate the next available InstitutionFacility ID.

        Returns
        -------
        int
            The next unused ID (1 if no InstitutionFacility exist).
        """
        if not self.institutionfacilities:
            return 1
        return max(self.institutionfacilities.keys()) + 1

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

    def insert(self, obj: InstitutionFacility) -> int:
        """Insert a new institutionfacility into persistent storage.

        Parameters
        ----------
        obj : InstitutionFacility
            The InstitutionFacility instance to persist.

        Returns
        -------
        int
            The assigned institutionfacility ID on success,
            0 on failure (invalid institutionfacility or ID already exists).
        """
        if not obj.is_valid():
            return 0

        # Generate ID if not set
        if obj.id <= 0:
            obj.id = self.generate_next_id()

        if obj.id in self.institutionfacilities:
            return 0

        self.institutionfacilities[obj.id] = obj
        filename = self.get_filename(obj)
        self.file_map[obj.id] = filename
        self.write_with_lock(
            filename, obj.get_data(), InstitutionFacility.PROPERTIES
        )
        return obj.id

    def update(self, obj: InstitutionFacility) -> bool:
        """Update an existing institutionfacility in persistent storage.

        Renames the file if the institutionfacility's name changed.

        Parameters
        ----------
        obj : InstitutionFacility
            The institutionfacility with updated values.

        Returns
        -------
        bool
            True if updated successfully, False otherwise.
        """
        if not obj.is_valid() or obj.id not in self.institutionfacilities:
            return False

        old_filename = self.file_map.get(obj.id)
        new_filename = self.get_filename(obj)

        if old_filename != new_filename and os.path.exists(old_filename):
            os.rename(old_filename, new_filename)

        self.institutionfacilities[obj.id] = obj
        self.file_map[obj.id] = new_filename
        self.write_with_lock(
            new_filename, obj.get_data(), InstitutionFacility.PROPERTIES
        )
        return True

    def delete(self, obj_id: int) -> bool:
        """Delete a institutionfacility and remove its CSV file.

        Parameters
        ----------
        obj_id : int
            ID of the institutionfacility to delete.

        Returns
        -------
        bool
            True if deleted, False if the institutionfacility was not found.
        """
        if obj_id not in self.institutionfacilities:
            return False

        filename = self.file_map.pop(obj_id, None)
        self.institutionfacilities.pop(obj_id, None)

        if filename and os.path.exists(filename):
            os.remove(filename)
        return True

    def select(self, obj_id: int) -> Optional[InstitutionFacility]:
        """Retrieve a institutionfacility by ID from the in-memory cache.

        Parameters
        ----------
        obj_id : int
            The institutionfacility ID to look up.

        Returns
        -------
        Optional[Player]
            The Player instance if found, None otherwise.
        """
        return self.institutionfacilities.get(obj_id)

    def list(self) -> List[InstitutionFacility]:
        """Return all loaded institutionfacilities.

        Returns
        -------
        List[InstitutionFacility]
            A list of all InstitutionFacility instances currently in memory.
        """
        return list(self.institutionfacilities.values())

    def sanitize_filename(self, name: str) -> str:
        """Sanitize a institutionfacility name for safe use in filenames.

        Parameters
        ----------
        name : str
            Original institutionfacility name.

        Returns
        -------
        str
            Sanitized name (lowercase, non-alphanumeric replaced by '_').
        """
        return re.sub(r"[^\w\-]", "_", name.lower().strip())

    def get_filename(self, institutionfacility: InstitutionFacility) -> str:
        """Generate the full path for a institutionfacility's CSV file.

        Parameters
        ----------
        institutionfacility : InstitutionFacility
            The institutionfacility object.

        Returns
        -------
        str
            Complete file path using pattern:
            <id>_<sanitized_name>_institutionfacility.csv
        """
        sanitized_name = self.sanitize_filename(institutionfacility.name)
        filename = f"{institutionfacility.id}_{sanitized_name}_institutionfacility.csv"
        return PathConfig.institutionfacility(filename)

    def load_all_institutionfacilities(self) -> None:
        """Load every institutionfacility CSV file from disk into memory.

        Scans the institutionfacilities directory, parses each
        matching CSV file, converts data types appropriately,
        and populates the cache.
        """
        PathConfig.ensure_dirs()
        for file_path in PathConfig.INSTITUTIONFACILITY_DIR.glob(
            "*_institutionfacility.csv"
        ):
            institutionfacility_data = self.csv_handler.read_csv(
                str(file_path), as_dict=True
            )
            if not institutionfacility_data:
                continue

            row = institutionfacility_data[0]
            # Build institutionfacility kwargs with type conversions
            institutionfacility_kwargs = {}
            for prop in InstitutionFacility.PROPERTIES:
                if prop in row:
                    if prop in self.int_properties:
                        institutionfacility_kwargs[prop] = (
                            int(row[prop]) if row[prop].isdigit() else 0
                        )
                    elif prop in self.bool_properties:
                        institutionfacility_kwargs[prop] = (
                            row[prop].lower() == "true"
                        )
                    else:
                        institutionfacility_kwargs[prop] = row[prop]

            institutionfacility = InstitutionFacility(
                **institutionfacility_kwargs
            )
            self.institutionfacilities[institutionfacility.id] = (
                institutionfacility
            )
            self.file_map[institutionfacility.id] = str(file_path)

    def search_institutionfacilities(
        self, query: str = ""
    ) -> List[InstitutionFacility]:
        """Retorna a lista de instituições, opcionalmente filtrada."""
        all_institutionfacilities = list(self.institutionfacilities.values())

        if not query.strip():
            return all_institutionfacilities

        q = query.lower().strip()
        return [
            p
            for p in all_institutionfacilities
            if q in str(p.id) or q in p.name.lower()
        ]
