import sys
from typing import TYPE_CHECKING, Any, Dict, Optional

import cv2
from mediapipe.tasks.python import vision
from PySide6.QtCore import QSettings

from ttea.dao import CalibrationSettingIniDAO
from ttea.model import CalibrationSetting
from ttea.util import PathConfig

if TYPE_CHECKING:
    from ttea.service import CalibrationService


class CalibrationSettingService:
    def __init__(
        self,
        dao: Optional[CalibrationSettingIniDAO] = None,
        calibration_service: Optional["CalibrationService"] = None,
    ):

        self.settings = QSettings(
            PathConfig.calibration_setting(), QSettings.IniFormat
        )
        self.dao = dao or CalibrationSettingIniDAO()
        self._calibration_service = calibration_service

    @property
    def calibration_service(self):
        """Inicialização Lazy caso não tenha sido injetado"""
        if self._calibration_service is None:
            from ttea.service import CalibrationService

            self._calibration_service = CalibrationService(
                calibration_setting_service=self
            )
        return self._calibration_service

    def create_calibration_setting(
        self, data: Dict[str, Any]
    ) -> Optional[CalibrationSetting]:
        calibration_setting = CalibrationSetting(**data)

        new_id = self.dao.insert(calibration_setting)
        return self.dao.select(new_id) if new_id > 0 else None

    def get_proportions(self) -> Dict[str, tuple[int, int]]:
        """Retorna o dicionário completo de proporções."""
        return CalibrationSetting.PROPORTIONS.items()

    def is_raspberry_pi(self) -> bool:
        return self.calibration_service.is_raspberry_pi()

    # ======================
    # MEDIAPIPE
    # ======================

    def get_mediapipe_model_desktop(self) -> str:
        return str(
            self.settings.value(
                "mediapipe/mediapipe_model_desktop",
                "pose_landmarker_full.task",
            )
            .strip()
            .lower()
        )

    def get_mediapipe_model_embedded(self) -> str:
        return str(
            self.settings.value(
                "mediapipe/mediapipe_model_embedded",
                "pose_landmarker_lite.task",
            )
            .strip()
            .lower()
        )

    def get_mediapipe_embedded_processing(self) -> str:
        return str(
            self.settings.value(
                "mediapipe/mediapipe_embedded_processing", "cpu"
            )
            .strip()
            .lower()
        )

    def get_mediapipe_linux_processing(self) -> str:
        return str(
            self.settings.value("mediapipe/mediapipe_linux_processing", "cpu")
            .strip()
            .lower()
        )

    def get_mediapipe_mac_processing(self) -> str:
        return str(
            self.settings.value("mediapipe/mediapipe_mac_processing", "cpu")
            .strip()
            .lower()
        )

    def get_mediapipe_windows_processing(self) -> str:
        return str(
            self.settings.value(
                "mediapipe/mediapipe_windows_processing", "cpu"
            )
            .strip()
            .lower()
        )

    def get_mediapipe_execution_mode(self) -> any:
        value = "vision.RunningMode." + str(
            self.settings.value(
                "mediapipe/mediapipe_execution_mode", "VIDEO"
            ).strip()
        )

        return getattr(cv2, value, vision.RunningMode.VIDEO)

    def is_mediapipe_enable_pose(self) -> bool:
        value = str(
            self.settings.value(
                "mediapipe/mediapipe_enable_mediapipe_pose", "1"
            )
        ).strip()

        return int(value)

    def get_mediapipe_detection_position(self) -> float:
        value = str(
            self.settings.value(
                "mediapipe/mediapipe_detection_position", "0.5"
            )
        ).strip()

        return float(value)

    def get_mediapipe_detection_presence(self) -> float:
        value = str(
            self.settings.value(
                "mediapipe/mediapipe_detection_presence", "0.5"
            )
        ).strip()

        return float(value)

    def get_mediapipe_detection_tracking(self) -> float:
        value = str(
            self.settings.value(
                "mediapipe/mediapipe_detection_tracking", "0.5"
            )
        ).strip()

        return float(value)

    def get_mediapipe_num_position(self) -> int:
        value = str(
            self.settings.value("mediapipe/mediapipe_num_position", "1")
        ).strip()

        return int(value)

    # ======================
    # OPENCV
    # ======================

    def get_opencv_capture_backend(self) -> int:
        if sys.platform.startswith("win"):
            key_name = "opencv/opencv_windows_capture"
        elif sys.platform.startswith("darwin"):
            key_name = "opencv/opencv_mac_capture"
        elif self.is_raspberry_pi():
            key_name = "opencv/opencv_embedded_capture"
        else:  # Linux convencional
            key_name = "opencv/opencv_linux_capture"

        value = str(self.settings.value(key_name, "CAP_ANY")).strip()

        return getattr(cv2, value, cv2.CAP_ANY)

    def get_opencv_buffer_size(self) -> int:
        value = str(
            self.settings.value("opencv/opencv_buffer_size", "1")
        ).strip()

        return int(value)

    def is_opencv_custom_camera(self) -> int:
        value = str(
            self.settings.value("opencv/opencv_custom_camera", "0")
        ).strip()

        return int(value)

    def get_opencv_ratio(self) -> str:
        value = str(self.settings.value("opencv/opencv_ratio")).strip()

        return value

    def get_opencv_width(self) -> int:
        value = str(self.settings.value("opencv/opencv_width", "640")).strip()

        return int(value)

    def get_opencv_height(self) -> int:
        value = str(self.settings.value("opencv/opencv_height", "480")).strip()

        return int(value)

    def get_opencv_fps(self) -> int:
        value = str(self.settings.value("opencv/opencv_fps", "30")).strip()

        return int(value)

    # ======================
    # FILTER
    # ======================
    def is_filter_enable_filter(self) -> int:
        value = str(
            self.settings.value("filter/filter_enable_filter", "0")
        ).strip()

        return int(value)

    def get_filter_average_smooth_frames(self) -> int:
        value = str(
            self.settings.value("filter/filter_average_smooth_frames", "5")
        ).strip()

        return int(value)

    def get_filter_clahe_clip(self) -> int:
        value = str(
            self.settings.value("filter/filter_clahe_clip", "2")
        ).strip()

        return int(value)

    def get_filter_clahe_grid(self) -> tuple[int, int]:
        value = str(
            self.settings.value("filter/filter_clahe_grid", "8:8")
        ).strip()

        grid = tuple(map(int, value.split(":")))

        return grid

    def get_filter_clahe_lum_below(self) -> int:
        value = str(
            self.settings.value("filter/filter_clahe_lum_below", "100")
        ).strip()

        return int(value)

    def get_filter_gamma_factor(self) -> float:
        value = str(
            self.settings.value("filter/filter_gamma_factor", "1.2")
        ).strip()

        return float(value)

    def get_filter_gamma_lum_above(self) -> int:
        value = str(
            self.settings.value("filter/filter_gamma_lum_above", "100")
        ).strip()

        return int(value)

    def get_filter_landmark_limit(self) -> float:
        value = str(
            self.settings.value("filter/filter_landmark_limit", "0.15")
        ).strip()

        return float(value)

    # ======================
    # TELEMETRY
    # ======================
    def is_telemetry_enable_panel(self) -> bool:
        value = str(
            self.settings.value(
                "telemetry/telemetry_enable_telemetry_panel", "1"
            )
        ).strip()

        return int(value)

    # ======================
    # AUTOMATIC CALIBRATION
    # ======================
    def get_automatic_window_position(self) -> str:
        key_name = "automatic/automatic_window_position_automatic"

        method_name = str(
            self.settings.value(
                key_name,
            )
        ).strip()

        return method_name

    def get_automatic_window_open_mode(self) -> int:
        value = str(
            self.settings.value(
                "automatic/automatic_window_open_automatic", "1"
            )
        ).strip()

        return int(value)

    def is_automatic_open_projector(self) -> bool:
        value = str(
            self.settings.value(
                "automatic/automatic_open_projector_automatic", "0"
            )
        ).strip()

        return int(value)

    def is_automatic_default_calibration(self) -> bool:
        value = str(
            self.settings.value(
                "automatic/automatic_default_calibration_automatic", "0"
            )
        ).strip()

        return int(value)

    def is_automatic_mirror_mode(self) -> bool:
        value = str(
            self.settings.value(
                "automatic/automatic_mirror_mode_automatic", "1"
            )
        ).strip()

        return int(value)

    def get_automatic_num_columns(self) -> int:
        value = str(
            self.settings.value(
                "automatic/automatic_num_columns_automatic", "6"
            )
        ).strip()

        return int(value)

    def get_automatic_num_rows(self) -> int:
        value = str(
            self.settings.value("automatic/automatic_num_rows_automatic", "4")
        ).strip()

        return int(value)

    def get_automatic_multiplier(self) -> float:
        value = str(
            self.settings.value(
                "automatic/automatic_multiplier_automatic", "0.75"
            )
        ).strip()

        return float(value)

    def get_automatic_dictionary(self) -> int:
        value = str(
            self.settings.value(
                "automatic/automatic_dictionary_automatic", "DICT_4X4_250"
            )
        ).strip()

        return getattr(cv2.aruco, value, cv2.aruco.DICT_4X4_250)

    def get_automatic_width(self) -> int:
        value = str(
            self.settings.value("automatic/automatic_width_automatic", "100")
        ).strip()

        return int(value)

    def get_automatic_height(self) -> int:
        value = str(
            self.settings.value("automatic/automatic_height_automatic", "100")
        ).strip()

        return int(value)

    def get_automatic_margin(self) -> int:
        value = str(
            self.settings.value("automatic/automatic_margin_automatic", "0")
        ).strip()

        return int(value)

    # ======================
    # SEMIAUTOMATIC CALIBRATION
    # ======================

    def get_semiautomatic_window_position(self) -> str:
        key_name = "semiautomatic/semiautomatic_window_position_semiautomatic"

        method_name = str(
            self.settings.value(
                key_name,
            )
        ).strip()

        return method_name

    def get_semiautomatic_window_open_mode(self) -> int:
        value = str(
            self.settings.value(
                "semiautomatic/semiautomatic_window_open_semiautomatic", "1"
            )
        ).strip()

        return int(value)

    def is_semiautomatic_open_projector(self) -> bool:
        value = str(
            self.settings.value(
                "semiautomatic/semiautomatic_open_projector_semiautomatic", "0"
            )
        ).strip()

        return int(value)

    def is_semiautomatic_default_calibration(self) -> bool:
        value = str(
            self.settings.value(
                "semiautomatic/semiautomatic_default_calibration_semiautomatic",
                "0",
            )
        ).strip()

        return int(value)

    def is_semiautomatic_mirror_mode(self) -> bool:
        value = str(
            self.settings.value(
                "semiautomatic/semiautomatic_mirror_mode_semiautomatic", "1"
            )
        ).strip()

        return int(value)

    # ======================
    # MANUAL CALIBRATION
    # ======================

    def get_manual_window_position(self) -> str:
        key_name = "manual/manual_window_position_manual"

        method_name = str(
            self.settings.value(
                key_name,
            )
        ).strip()

        return method_name

    def get_manual_window_open_mode(self) -> int:
        value = str(
            self.settings.value("manual/manual_window_open_manual", "1")
        ).strip()

        return int(value)

    def is_manual_open_projector(self) -> bool:
        value = str(
            self.settings.value("manual/manual_open_projector_manual", "0")
        ).strip()

        return int(value)

    def is_manual_default_calibration(self) -> bool:
        value = str(
            self.settings.value(
                "manual/manual_default_calibration_manual", "0"
            )
        ).strip()

        return int(value)

    def is_manual_mirror_mode(self) -> bool:
        value = str(
            self.settings.value("manual/manual_mirror_mode_manual", "1")
        ).strip()

        return int(value)
