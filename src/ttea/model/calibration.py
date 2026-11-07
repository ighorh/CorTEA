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
class Calibration:
    camera_description: str
    camera_id: str
    camera_position: int
    camera_width: int
    camera_height: int
    camera_max_fps: int
    camera_min_fps: int

    screen_manufacturer: str
    screen_model: str
    screen_position: int
    screen_serial_number: str
    screen_width: int
    screen_height: int
    screen_available_width: int
    screen_available_height: int

    # Available width and height for projection and aspect ratio 16:9 or 4:3
    content_width: int
    content_height: int
    content_width_ratio: int
    content_height_ratio: int
    content_proportion: str

    calibration_date: str
    calibration_hour: str

    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []
    ID_VALUE: ClassVar[int] = 1  # Static ID for all calibration settings
    PROPORTIONS: ClassVar[dict[str, tuple[int, int]]] = {
        "4:3": (4, 3),
        "16:9": (16, 9),
    }

    # Mapping prefixes to .ini sections
    SECTIONS_MAP: ClassVar[dict[str, str]] = {
        "camera_": "camera",
        "screen_": "screen",
        "content_": "content",
        "calibration_": "info",
    }

    # Constant to identify properties that should not be saved
    IGNORED_PROPERTIES: ClassVar[list[str]] = [
        "PROPERTIES",
        "DATA_PROPERTIES",
        "ID_VALUE",
        "PROPORTIONS",
        "SECTIONS_MAP",
    ]

    def is_valid(self) -> bool:
        for prop in self.PROPERTIES:
            value = getattr(self, prop)

            # Generic validation for None
            if value is None:
                return False

        return True

    def set_data(self, data: Dict) -> None:
        for prop in self.PROPERTIES:
            if prop in data:
                setattr(self, prop, data[prop])

    def get_data(self) -> List[Dict]:
        info = {prop: getattr(self, prop) for prop in self.PROPERTIES}
        return [info]

    def get_proportion_tuple(self, proportion: str) -> tuple[int, int]:
        return self.PROPORTIONS.get(proportion, (0, 0))

    def get_section_for_property(self, prop_name: str) -> str:
        """Returns the section name for a given property."""
        for prefix, section in self.SECTIONS_MAP.items():
            if prop_name.startswith(prefix):
                return section
        return "geral"
