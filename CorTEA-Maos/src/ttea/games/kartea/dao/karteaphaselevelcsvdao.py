from dataclasses import fields
from typing import Any, List, Optional

from PySide6.QtCore import QDir, QDirIterator

from ttea.dao import DAO
from ttea.games.kartea.model.karteaphase import KarteaPhase
from ttea.games.kartea.model.karteaphaselevel import KarteaPhaseLevel
from ttea.games.kartea.util.karteapathconfig import KarteaPathConfig
from ttea.util import CSVHandler


class KarteaPhaseLevelCsvDAO(DAO):
    """Data Access Object for KarteaPhaseLevel, handling query operations
    by reading CSV files physically.

    Attributes
    ----------
    csv_handler : CSVHandler
        Utility for reading and writing CSV files.

    Methods
    -------
    __init__()
        Initializes the DAO with a CSV handler.
    load_levels_from_csv(phase_id: int) -> List[KarteaPhaseLevel]
        Loads all KarteaPhaseLevel for a given phase ID from a CSV file.
    select(obj_id: int) -> Optional[KarteaPhaseLevel]
        Retrieves a single KarteaPhaseLevel by ID.
    list() -> List[KarteaPhaseLevel]
        Retrieves a list of all KarteaPhaseLevel across all phases.
    insert(obj: object) -> Optional[Any]
        Placeholder for insert operation (not implemented).
    update(obj: object) -> Optional[Any]
        Placeholder for update operation (not implemented).
    delete(obj_id: int) -> Optional[Any]
        Placeholder for delete operation (not implemented).
    """

    def __init__(self):
        """Initialize the KarteaPhaseLevelDAO with a CSV handler.

        Returns
        -------
        None

        Notes
        -----
        Creates necessary directories using KarteaPathConfig.
        """
        self.csv_handler = CSVHandler()
        KarteaPathConfig.ensure_kartea_dirs()

    def load_levels_from_csv(self, phase_id: int) -> List[KarteaPhaseLevel]:
        # Abstração via PathConfig para suporte híbrido
        content = KarteaPathConfig.read_phase_data(phase_id)
        if not content:
            return []

        phase_data = self.csv_handler.read_csv(content=content, as_dict=True)
        levels = []
        temp_phase = KarteaPhase(id=phase_id, level_list=[])
        level_fields = {f.name: f.type for f in fields(KarteaPhaseLevel)}

        for row in phase_data:
            if "phase" in row and int(row["phase"]) != phase_id:
                continue

            level_kwargs = {}
            for prop in KarteaPhaseLevel.PROPERTIES:
                if prop == "phase":
                    level_kwargs[prop] = temp_phase
                elif prop == "obj_type" and prop in row:
                    level_kwargs[prop] = [
                        int(x)
                        for x in row.get(prop, "").strip().split()
                        if x.strip().isdigit()
                    ]
                elif prop in row:
                    t = level_fields.get(prop)
                    level_kwargs[prop] = (
                        t(row[prop]) if t in (int, float) else row[prop]
                    )

            if "id" in level_kwargs:
                levels.append(KarteaPhaseLevel(**level_kwargs))
        return levels

    def select(
        self, phase_id: int, level_id: int
    ) -> Optional[KarteaPhaseLevel]:
        levels = self.load_levels_from_csv(phase_id)
        for level in levels:
            if level.id == level_id:
                phase = KarteaPhase(id=phase_id, level_list=levels)
                level.phase = phase
                return level
        return None

    def list(self) -> List[KarteaPhaseLevel]:
        all_levels = []
        # Reutiliza a lógica de IDs únicos do KarteaPhaseCsvDAO
        phase_ids = set()
        for file in KarteaPathConfig.KARTEA_PHASES_DIR.glob("*.csv"):
            if file.stem.isdigit():
                phase_ids.add(int(file.stem))

        it = QDirIterator(":/phases", QDir.Files)
        while it.hasNext():
            it.next()
            name = it.fileName().replace(".csv", "")
            if name.isdigit():
                phase_ids.add(int(name))

        for p_id in sorted(list(phase_ids)):
            levels = self.load_levels_from_csv(p_id)
            if levels:
                phase = KarteaPhase(id=p_id, level_list=levels)
                for level in levels:
                    level.phase = phase
                    all_levels.append(level)
        return all_levels

    def insert(self, obj: object) -> Optional[Any]:
        """Placeholder for insert operation.

        Parameters
        ----------
        obj : object
            The object to insert.

        Returns
        -------
        Optional[Any]
            Not implemented.

        Raises
        ------
        NotImplementedError
            Always raised as the method is not implemented.
        """
        raise NotImplementedError

    def update(self, obj: object) -> Optional[Any]:
        """Placeholder for update operation.

        Parameters
        ----------
        obj : object
            The object to update.

        Returns
        -------
        Optional[Any]
            Not implemented.

        Raises
        ------
        NotImplementedError
            Always raised as the method is not implemented.
        """
        raise NotImplementedError

    def delete(self, obj_id: int) -> Optional[Any]:
        """Placeholder for delete operation.

        Parameters
        ----------
        obj_id : int
            The ID of the object to delete.

        Returns
        -------
        Optional[Any]
            Not implemented.

        Raises
        ------
        NotImplementedError
            Always raised as the method is not implemented.
        """
        raise NotImplementedError
