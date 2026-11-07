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
class CalibrationSetting:
    """Represents the calibration settings for the application."""

    mediapipe_model_desktop: str
    mediapipe_model_embedded: str
    mediapipe_embedded_processing: str
    mediapipe_linux_processing: str
    mediapipe_mac_processing: str
    mediapipe_windows_processing: str
    mediapipe_execution_mode: str
    mediapipe_enable_mediapipe_pose: int
    mediapipe_detection_position: float
    mediapipe_detection_presence: float
    mediapipe_detection_tracking: float
    mediapipe_num_position: int

    opencv_embedded_capture: str
    opencv_linux_capture: str
    opencv_mac_capture: str
    opencv_windows_capture: str
    opencv_buffer_size: int
    opencv_custom_camera: int
    opencv_ratio: str
    opencv_width: int
    opencv_height: int
    opencv_fps: int

    filter_enable_filter: int
    filter_average_smooth_frames: int
    filter_clahe_clip: int
    filter_clahe_grid: str
    filter_clahe_lum_below: int
    filter_gamma_factor: float
    filter_gamma_lum_above: int
    filter_landmark_limit: float

    telemetry_enable_telemetry_panel: int

    automatic_window_position_automatic: str
    automatic_window_open_automatic: str
    automatic_open_projector_automatic: int
    automatic_default_calibration_automatic: int
    automatic_mirror_mode_automatic: int
    automatic_num_columns_automatic: int
    automatic_num_rows_automatic: int
    automatic_multiplier_automatic: float
    automatic_dictionary_automatic: str
    automatic_width_automatic: int
    automatic_height_automatic: int
    automatic_margin_automatic: int

    semiautomatic_window_position_semiautomatic: str
    semiautomatic_window_open_semiautomatic: str
    semiautomatic_open_projector_semiautomatic: int
    semiautomatic_default_calibration_semiautomatic: int
    semiautomatic_mirror_mode_semiautomatic: int

    manual_window_position_manual: str
    manual_window_open_manual: str
    manual_open_projector_manual: int
    manual_default_calibration_manual: int
    manual_mirror_mode_manual: int

    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []
    ID_VALUE: ClassVar[int] = 1  # Static ID for all calibration settings
    PROPORTIONS: ClassVar[dict[str, tuple[int, int]]] = {
        "4:3": (4, 3),
        "16:9": (16, 9),
    }

    FULLSCREEN = 1
    MAXIMIZED = 2
    MAXIMIZED_UTIL = 3

    # Mapping prefixes to .ini sections
    SECTIONS_MAP: ClassVar[dict[str, str]] = {
        "mediapipe_": "mediapipe",
        "opencv_": "opencv",
        "filter_": "filter",
        "telemetry_": "telemetry",
        "automatic_": "automatic",
        "semiautomatic_": "semiautomatic",
        "manual_": "manual",
    }

    # Constant to identify properties that should not be saved
    IGNORED_PROPERTIES: ClassVar[list[str]] = [
        "PROPERTIES",
        "DATA_PROPERTIES",
        "FULLSCREEN",
        "ID_VALUE",
        "MAXIMIZED",
        "MAXIMIZED_UTIL",
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
