import os
import re
from dataclasses import fields
from typing import TYPE_CHECKING, Dict, List, Optional

import portalocker

# Local module import
from ttea.dao import DAO
from ttea.model import Professional
from ttea.util import CSVHandler, PathConfig

if TYPE_CHECKING:
    from ttea.dao import InstitutionFacilityCsvDAO


class ProfessionalCsvDAO(DAO[Professional]):
    """Specialized DAO for professional entities using CSV files
    with in-memory cache.
    """

    def __init__(
        self, institution_dao: Optional["InstitutionFacilityCsvDAO"] = None
    ) -> None:
        """Initialize the DAO and load all professionals
        from CSV files."""
        from ttea.dao import InstitutionFacilityCsvDAO

        self.csv_handler = CSVHandler()
        self.professionals: Dict[int, Professional] = {}
        self.file_map: Dict[int, str] = {}
        self.int_properties = [
            f.name for f in fields(Professional) if f.type == int
        ]
        self.bool_properties = [
            f.name for f in fields(Professional) if f.type == bool
        ]
        self.institution_dao = institution_dao or InstitutionFacilityCsvDAO()
        self.load_all_professionals()

    def generate_next_id(self) -> int:
        """Generate the next available InstitutionFacility ID.

        Returns
        -------
        int
            The next unused ID (1 if no InstitutionFacility exist).
        """
        if not self.professionals:
            return 1
        return max(self.professionals.keys()) + 1

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

    def insert(self, obj: Professional) -> int:
        """Insert a new professional into persistent storage.

        Parameters
        ----------
        obj : InstitutionFacility
            The InstitutionFacility instance to persist.

        Returns
        -------
        int
            The assigned professional ID on success,
            0 on failure (invalid professional or ID already exists).
        """
        if not obj.is_valid():
            return 0

        # Generate ID if not set
        if obj.id <= 0:
            obj.id = self.generate_next_id()

        if obj.id in self.professionals:
            return 0

        self.professionals[obj.id] = obj
        filename = self.get_filename(obj)
        self.file_map[obj.id] = filename
        self.write_with_lock(filename, obj.get_data(), Professional.PROPERTIES)
        return obj.id

    def update(self, obj: Professional) -> bool:
        """Update an existing professional in persistent storage.

        Renames the file if the professional's name changed.

        Parameters
        ----------
        obj : Professional
            The professional with updated values.

        Returns
        -------
        bool
            True if updated successfully, False otherwise.
        """
        if not obj.is_valid() or obj.id not in self.professionals:
            return False

        old_filename = self.file_map.get(obj.id)
        new_filename = self.get_filename(obj)

        if old_filename != new_filename and os.path.exists(old_filename):
            os.rename(old_filename, new_filename)

        self.professionals[obj.id] = obj
        self.file_map[obj.id] = new_filename
        self.write_with_lock(
            new_filename, obj.get_data(), Professional.PROPERTIES
        )
        return True

    def delete(self, obj_id: int) -> bool:
        """Delete a professional and remove its CSV file.

        Parameters
        ----------
        obj_id : int
            ID of the professional to delete.

        Returns
        -------
        bool
            True if deleted, False if the professional was not found.
        """
        if obj_id not in self.professionals:
            return False

        filename = self.file_map.pop(obj_id, None)
        self.professionals.pop(obj_id, None)

        if filename and os.path.exists(filename):
            os.remove(filename)
        return True

    def select(self, obj_id: int) -> Optional[Professional]:
        """Retrieve a professional by ID from the in-memory cache.

        Parameters
        ----------
        obj_id : int
            The professional ID to look up.

        Returns
        -------
        Optional[Professional]
            The Professional instance if found, None otherwise.
        """
        return self.professionals.get(obj_id)

    def list(self) -> List[Professional]:
        """Return all loaded professionals.

        Returns
        -------
        List[InstitutionFacility]
            A list of all InstitutionFacility instances currently in memory.
        """
        return list(self.professionals.values())

    def sanitize_filename(self, name: str) -> str:
        """Sanitize a professional name for safe use in filenames.

        Parameters
        ----------
        name : str
            Original professional name.

        Returns
        -------
        str
            Sanitized name (lowercase, non-alphanumeric replaced by '_').
        """
        return re.sub(r"[^\w\-]", "_", name.lower().strip())

    def get_filename(self, professional: Professional) -> str:
        """Generate the full path for a professional's CSV file.

        Parameters
        ----------
        professional : Professional
            The professional object.

        Returns
        -------
        str
            Complete file path using pattern:
            <id>_<sanitized_name>_professional.csv
        """
        sanitized_name = self.sanitize_filename(professional.name)
        filename = f"{professional.id}_{sanitized_name}_professional.csv"
        return PathConfig.professional(filename)

    def load_all_professionals(self) -> None:
        """Load every professional CSV file from disk into memory.

        Scans the professionals directory, parses each
        matching CSV file, converts data types appropriately,
        and populates the cache.
        """
        PathConfig.ensure_dirs()
        for file_path in PathConfig.PROFESSIONAL_DIR.glob(
            "*_professional.csv"
        ):
            professional_data = self.csv_handler.read_csv(
                str(file_path), as_dict=True
            )
            if not professional_data:
                continue

            row = professional_data[0]
            # Build professional kwargs with type conversions
            professional_kwargs = {}
            for prop in Professional.PROPERTIES:
                if prop in row:
                    # Special handling for institutionfacility to load the full object
                    if prop == "institutionfacility":
                        institution_id = (
                            int(row[prop]) if row[prop].isdigit() else None
                        )
                        if self.institution_dao and institution_id:
                            # Busca o objeto completo da instituição pelo ID
                            professional_kwargs[prop] = (
                                self.institution_dao.select(institution_id)
                            )
                        else:
                            professional_kwargs[prop] = None
                    elif prop in self.int_properties:
                        professional_kwargs[prop] = (
                            int(row[prop]) if row[prop].isdigit() else 0
                        )
                    elif prop in self.bool_properties:
                        professional_kwargs[prop] = row[prop].lower() == "true"
                    else:
                        professional_kwargs[prop] = row[prop]

            professional = Professional(**professional_kwargs)
            self.professionals[professional.id] = professional
            self.file_map[professional.id] = str(file_path)

    def search_professionals(self, query: str = "") -> List[Professional]:
        """Retorna a lista de instituições, opcionalmente filtrada."""
        all_professionals = list(self.professionals.values())

        if not query.strip():
            return all_professionals

        q = query.lower().strip()
        return [
            p
            for p in all_professionals
            if q in str(p.id) or q in p.name.lower()
        ]
