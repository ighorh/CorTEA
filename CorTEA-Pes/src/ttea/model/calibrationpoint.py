from dataclasses import dataclass, fields
from typing import ClassVar, Dict, List


def initialize_reflexive(cls):
    """Decorator to statically initialize player reflection data.

    Parameters
    ----------
    cls : type
        The class to be decorated.

    Returns
    -------
    type
        The decorated class with initialized PROPERTIES and DATA_PROPERTIES.

    Notes
    -----
    - Adds the list of field names to `PROPERTIES`.
    - Adds default values of initializable fields to `DATA_PROPERTIES`.
    """
    cls.PROPERTIES = [field.name for field in fields(cls)]
    cls.DATA_PROPERTIES = [
        field.default for field in fields(cls) if field.init
    ]
    return cls


@initialize_reflexive
@dataclass
class CalibrationPoint:
    pointx1: int
    pointy1: int
    pointx2: int
    pointy2: int
    pointx3: int
    pointy3: int
    pointx4: int
    pointy4: int

    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []
    ID_VALUE: ClassVar[int] = 1  # Static ID for all calibration points

    def set_data(self, data: Dict) -> None:
        for prop in self.PROPERTIES:
            if prop in data:
                setattr(self, prop, data[prop])

    def get_data(self) -> List[Dict]:
        info = {prop: getattr(self, prop) for prop in self.PROPERTIES}
        return [info]
