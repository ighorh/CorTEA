from typing import List, Optional

from PySide6.QtCore import QSettings

from ttea.model import Calibration
from ttea.util import PathConfig

# Direct import de DAO to avoid circular import
from .dao import DAO


class CalibrationIniDAO(DAO[Calibration]):

    def __init__(self) -> None:
        self.settings = QSettings(
            PathConfig.calibration_hardware(), QSettings.IniFormat
        )

    def insert(self, obj: Calibration) -> int:
        if not obj.is_valid():
            return 0

        for prop in obj.PROPERTIES:
            if prop in obj.IGNORED_PROPERTIES:
                continue

            value = getattr(obj, prop)
            group_name = obj.get_section_for_property(prop)

            self.settings.beginGroup(group_name)
            self.settings.setValue(prop, value)
            self.settings.endGroup()

        self.settings.sync()
        return Calibration.ID_VALUE

    def update(self, obj: Calibration) -> bool:
        raise NotImplementedError

    def delete(self, obj_id: int) -> bool:
        raise NotImplementedError

    def select(self, obj_id: int) -> Optional[Calibration]:
        import typing

        data = {}
        type_hints = typing.get_type_hints(Calibration)

        # Create a temporary instance to access the section helper
        # or access it via a class if it's static
        temp_obj = Calibration.__new__(Calibration)

        for prop in Calibration.PROPERTIES:
            if prop in Calibration.IGNORED_PROPERTIES:
                continue

            group_name = temp_obj.get_section_for_property(prop)
            val = self.settings.value(f"{group_name}/{prop}")

            if val is not None:
                target_type = type_hints.get(prop)
                if target_type == int:
                    data[prop] = int(val)
                elif target_type == float:
                    data[prop] = float(val)
                else:
                    data[prop] = val

        if not data.get("camera_id"):
            return None

        return Calibration(**data)

    def list(self) -> List[Calibration]:
        raise NotImplementedError
