from dataclasses import fields
from typing import Dict, List, Optional

import portalocker

from ttea.model import CalibrationPoint
# Direct import de DAO to avoid circular import
from ttea.util import CSVHandler, PathConfig

from .dao import DAO


class CalibrationPointCsvDAO(DAO[CalibrationPoint]):

    def __init__(self) -> None:
        self.csv_handler = CSVHandler()
        self.calibration_points: Dict[int, CalibrationPoint] = {}
        self.file_map: Dict[int, str] = {}
        self.int_properties = [
            f.name for f in fields(CalibrationPoint) if f.type == int
        ]

        self.load_all_calibration_points()

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

    def insert(self, obj: CalibrationPoint) -> int:
        self.calibration_points[CalibrationPoint.ID_VALUE] = obj
        filename = PathConfig.calibration_point(
            PathConfig.CALIBRATION_POINT_FILENAME
        )
        self.file_map[CalibrationPoint.ID_VALUE] = filename
        self.write_with_lock(
            filename, obj.get_data(), CalibrationPoint.PROPERTIES
        )
        return CalibrationPoint.ID_VALUE

    def update(self, obj: CalibrationPoint) -> bool:
        raise NotImplementedError

    def delete(self, obj_id: int) -> bool:
        raise NotImplementedError

    def select(self, obj_id: int) -> Optional[CalibrationPoint]:
        """Retrieve a calibration point by ID from the in-memory cache.

        Parameters
        ----------
        obj_id : int
            The calibration point ID to look up.

        Returns
        -------
        Optional[CalibrationPoint]
            The CalibrationPoint instance if found, None otherwise.
        """
        return self.calibration_points.get(obj_id)

    def list(self) -> List[CalibrationPoint]:
        raise NotImplementedError

    def load_all_calibration_points(self) -> None:
        """Load every calibration point CSV file from disk into memory.

        Scans the calibration points from calibration directory, parses each
        matching CSV file, converts data types appropriately,
        and populates the cache.
        """
        PathConfig.ensure_dirs()
        for file_path in PathConfig.CALIBRATION_DIR.glob(
            PathConfig.CALIBRATION_POINT_FILENAME
        ):
            calibration_point_data = self.csv_handler.read_csv(
                str(file_path), as_dict=True
            )
            if not calibration_point_data:
                continue

            row = calibration_point_data[0]
            # Build calibration point kwargs with type conversions
            calibration_point_kwargs = {}
            for prop in CalibrationPoint.PROPERTIES:
                if prop in row:
                    if prop in self.int_properties:
                        calibration_point_kwargs[prop] = (
                            int(row[prop]) if row[prop].isdigit() else 0
                        )
                    else:
                        calibration_point_kwargs[prop] = row[prop]

            calibration_point = CalibrationPoint(**calibration_point_kwargs)
            self.calibration_points[calibration_point.ID_VALUE] = (
                calibration_point
            )
            self.file_map[calibration_point.ID_VALUE] = str(file_path)
