from dataclasses import fields
from typing import Any, List, Optional, Set

from PySide6.QtCore import QDir, QDirIterator

from ttea.dao import DAO
from ttea.games.kartea.model.karteaphase import KarteaPhase
from ttea.games.kartea.model.karteaphaselevel import KarteaPhaseLevel
from ttea.games.kartea.util.karteapathconfig import KarteaPathConfig
from ttea.util import CSVHandler


class KarteaPhaseCsvDAO(DAO):
    """Data Access Object for KarteaPhase, handling query operations
    by reading CSV files physically.

    Attributes
    ----------
    csv_handler : CSVHandler
        Utility for reading and writing CSV files.

    Methods
    -------
    __init__()
        Initializes the DAO with a CSV handler.
    load_phase_from_csv(kartea_phase_id: int) -> Optional[KarteaPhase]
        Loads a KarteaPhase and its levels from a CSV file using PROPERTIES.
    select(obj_id: int) -> Optional[KarteaPhase]
        Retrieves a single KarteaPhase by ID, including its levels.
    list() -> List[KarteaPhase]
        Retrieves a list of all KarteaPhases, each including its levels.
    insert(obj: object) -> Optional[Any]
        Placeholder for insert operation (not implemented).
    update(obj: object) -> Optional[Any]
        Placeholder for update operation (not implemented).
    delete(obj_id: int) -> Optional[Any]
        Placeholder for delete operation (not implemented).
    """

    def __init__(self):
        """Initialize the KarteaPhaseDAO with a CSV handler.

        Returns
        -------
        None

        Notes
        -----
        Creates necessary directories using KarteaPathConfig.
        """
        self.csv_handler = CSVHandler()
        KarteaPathConfig.ensure_kartea_dirs()

    def load_phase_from_csv(
        self, kartea_phase_id: int
    ) -> Optional[KarteaPhase]:
        # PathConfig resolve a prioridade: Disco > Recurso
        content = KarteaPathConfig.read_phase_data(kartea_phase_id)
        if not content:
            return None

        phase_data = self.csv_handler.read_csv(content=content, as_dict=True)
        if not phase_data:
            return None

        levels = []
        temp_phase = KarteaPhase(id=kartea_phase_id, level_list=[])
        level_fields = {f.name: f.type for f in fields(KarteaPhaseLevel)}

        for row in phase_data:
            if "phase" in row and int(row["phase"]) != kartea_phase_id:
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
                level = KarteaPhaseLevel(**level_kwargs)
                levels.append(level)

        if not levels:
            return None

        phase = KarteaPhase(id=kartea_phase_id, level_list=levels)
        for level in levels:
            level.phase = phase
        return phase

    def select(self, obj_id: int) -> Optional[KarteaPhase]:
        """Retrieve a single KarteaPhase by ID, including its levels.

        Parameters
        ----------
        obj_id : int
            The ID of the phase to retrieve.

        Returns
        -------
        Optional[KarteaPhase]
            The KarteaPhase object if found, None otherwise.

        Notes
        -----
        Calls _load_phase_from_csv to read the CSV file.
        """
        return self.load_phase_from_csv(obj_id)

    def list(self) -> List[KarteaPhase]:
        phase_ids: Set[int] = set()

        # 1. Busca IDs no Disco (AppData)
        for file in KarteaPathConfig.KARTEA_PHASES_DIR.glob("*.csv"):
            if file.stem.isdigit():
                phase_ids.add(int(file.stem))

        # 2. Busca IDs nos Recursos (:/phases) [cite: 1, 9]
        it = QDirIterator(":/phases", QDir.Files)
        while it.hasNext():
            it.next()
            name = it.fileName().replace(".csv", "")
            if name.isdigit():
                phase_ids.add(int(name))

        phases = []
        for p_id in sorted(list(phase_ids)):
            phase = self.load_phase_from_csv(p_id)
            if phase:
                phases.append(phase)
        return phases

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
