import os
import sys
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from PySide6.QtCore import QRect
from PySide6.QtGui import QGuiApplication, QScreen
from PySide6.QtMultimedia import QCameraDevice, QMediaDevices

from ttea.dao import CalibrationIniDAO, CalibrationPointCsvDAO
from ttea.model import Calibration, CalibrationPoint

if TYPE_CHECKING:
    from ttea.service import CalibrationSettingService


class CalibrationService:
    def __init__(
        self,
        dao: Optional[CalibrationIniDAO] = None,
        dao_calibration_point: Optional[CalibrationPointCsvDAO] = None,
        calibration_setting_service: Optional[
            "CalibrationSettingService"
        ] = None,
    ):
        # Cache opcional se os monitores não mudarem durante a execução
        self._screens = QGuiApplication.screens()
        self.dao = dao or CalibrationIniDAO()
        self.dao_calibration_point = (
            dao_calibration_point or CalibrationPointCsvDAO()
        )

        self._calibration_setting_service = calibration_setting_service

    @property
    def calibration_setting_service(self):
        """Inicialização Lazy caso não tenha sido injetado"""
        if self._calibration_setting_service is None:
            from ttea.service import CalibrationSettingService

            self._calibration_setting_service = CalibrationSettingService(
                calibration_service=self
            )
        return self._calibration_setting_service

    def get_proportions(self) -> Dict[str, tuple[int, int]]:
        """Retorna o dicionário completo de proporções."""
        return Calibration.PROPORTIONS.items()

    def get_screens(self) -> List[QScreen]:
        """Atualiza e retorna a lista de monitores disponíveis."""
        return QGuiApplication.screens()

    def get_video_inputs(self) -> List[QCameraDevice]:
        """Retorna os inputs de vídeo disponíveis."""
        return QMediaDevices.videoInputs()

    def _get_screen(self, index: int) -> Optional[QScreen]:
        """Método privado para validar e recuperar um monitor com segurança."""
        screens = self.get_screens()
        if 0 <= index < len(screens):
            return screens[index]
        return None

    def get_geometry_of_screen(self, index: int) -> Optional[QRect]:
        screen = self._get_screen(index)
        return screen.geometry() if screen else None

    def get_available_geometry_of_screen(self, index: int) -> Optional[QRect]:
        screen = self._get_screen(index)
        return screen.availableGeometry() if screen else None

    def is_raspberry_pi(self) -> bool:
        """Verifica centralizadamente se o hardware é um Raspberry Pi."""
        if not sys.platform.startswith("lin"):
            return False
        try:
            if os.path.exists("/proc/device-tree/model"):
                with open("/proc/device-tree/model", "r") as f:
                    return "raspberry pi" in f.read().lower()
            return False
        except Exception:
            return False

    def is_windows(self) -> bool:
        """Verifica se o sistema operacional é Windows."""
        return sys.platform.startswith("win")

    def create_calibration_hardware(
        self, data: Dict[str, Any]
    ) -> Optional[Calibration]:
        calibration = Calibration(**data)
        calibration.set_data(data)

        if not calibration.is_valid():
            return None

        return self.dao.insert(calibration)

    def create_calibration_point(
        self, data: Dict[str, Any]
    ) -> Optional[CalibrationPoint]:
        """
        Create a new calibration point from a dictionary of attributes.

        Parameters
        ----------
        data : dict
            Must contain the key ``id`` (int),  ``name`` (str),
            ``birth_date`` (date) and optionally ``observation`` (str).

        Returns
        -------
        CalibrationPoint or None
            The created ``CalibrationPoint`` instance if validation and insertion
            succeed; ``None`` otherwise.
        """
        calibration_point = CalibrationPoint(**data)

        new_id = self.dao_calibration_point.insert(calibration_point)
        return (
            self.dao_calibration_point.select(new_id) if new_id > 0 else None
        )

    # ======================
    # MEDIAPIPE
    # ======================

    def get_mediapipe_model_desktop(self) -> str:
        return self.calibration_setting_service.get_mediapipe_model_desktop()

    def get_mediapipe_model_embedded(self) -> str:
        return self.calibration_setting_service.get_mediapipe_model_embedded()

    def get_mediapipe_embedded_processing(self) -> str:
        return (
            self.calibration_setting_service.get_mediapipe_embedded_processing()
        )

    def get_mediapipe_linux_processing(self) -> str:
        return (
            self.calibration_setting_service.get_mediapipe_linux_processing()
        )

    def get_mediapipe_mac_processing(self) -> str:
        return self.calibration_setting_service.get_mediapipe_mac_processing()

    def get_mediapipe_windows_processing(self) -> str:
        return (
            self.calibration_setting_service.get_mediapipe_windows_processing()
        )

    def get_mediapipe_execution_mode(self) -> any:
        return self.calibration_setting_service.get_mediapipe_execution_mode()

    def is_enable_mediapipe_pose(self) -> bool:
        return self.calibration_setting_service.is_mediapipe_enable_pose()

    def get_mediapipe_detection_position(self) -> float:
        return (
            self.calibration_setting_service.get_mediapipe_detection_position()
        )

    def get_mediapipe_detection_presence(self) -> float:
        return (
            self.calibration_setting_service.get_mediapipe_detection_presence()
        )

    def get_mediapipe_detection_tracking(self) -> float:
        return (
            self.calibration_setting_service.get_mediapipe_detection_tracking()
        )

    def get_mediapipe_num_position(self) -> int:
        return self.calibration_setting_service.get_mediapipe_num_position()

    # ======================
    # OPENCV
    # ======================

    def get_opencv_capture_backend(self) -> int:
        return self.calibration_setting_service.get_opencv_capture_backend()

    def get_opencv_buffer_size(self) -> int:
        return self.calibration_setting_service.get_opencv_buffer_size()

    def is_opencv_custom_camera(self) -> int:
        return self.calibration_setting_service.is_opencv_custom_camera()

    def get_opencv_ratio(self) -> str:
        return self.calibration_setting_service.get_opencv_ratio()

    def get_opencv_width(self) -> int:
        return self.calibration_setting_service.get_opencv_width()

    def get_opencv_height(self) -> int:
        return self.calibration_setting_service.get_opencv_height()

    def get_opencv_fps(self) -> int:
        return self.calibration_setting_service.get_opencv_fps()

    # ======================
    # FILTER
    # ======================

    def is_filter_enable_filter(self) -> int:
        return self.calibration_setting_service.is_filter_enable_filter()

    def get_filter_average_smooth_frames(self) -> int:
        return (
            self.calibration_setting_service.get_filter_average_smooth_frames()
        )

    def get_filter_clahe_clip(self) -> int:
        return self.calibration_setting_service.get_filter_clahe_clip()

    def get_filter_clahe_grid(self) -> tuple[int, int]:
        return self.calibration_setting_service.get_filter_clahe_grid()

    def get_filter_clahe_lum_below(self) -> int:
        return self.calibration_setting_service.get_filter_clahe_lum_below()

    def get_filter_gamma_factor(self) -> float:
        return self.calibration_setting_service.get_filter_gamma_factor()

    def get_filter_gamma_lum_above(self) -> int:
        return self.calibration_setting_service.get_filter_gamma_lum_above()

    def get_filter_landmark_limit(self) -> float:
        return self.calibration_setting_service.get_filter_landmark_limit()

    # ======================
    # TELEMETRY
    # ======================
    def is_telemetry_enable_panel(self) -> bool:
        return self.calibration_setting_service.is_telemetry_enable_panel()

    # ======================
    # AUTOMATIC CALIBRATION
    # ======================

    def get_automatic_window_position(self) -> str:
        return self.calibration_setting_service.get_automatic_window_position()

    def get_automatic_window_open_mode(self) -> int:
        return (
            self.calibration_setting_service.get_automatic_window_open_mode()
        )

    def is_automatic_open_projector(self) -> bool:
        return self.calibration_setting_service.is_automatic_open_projector()

    def is_automatic_default_calibration(self) -> bool:
        return (
            self.calibration_setting_service.is_automatic_default_calibration()
        )

    def is_automatic_mirror_mode(self) -> bool:
        return self.calibration_setting_service.is_automatic_mirror_mode()

    def get_automatic_num_columns(self) -> int:
        return self.calibration_setting_service.get_automatic_num_columns()

    def get_automatic_num_rows(self) -> int:
        return self.calibration_setting_service.get_automatic_num_rows()

    def get_automatic_multiplier(self) -> int:
        return self.calibration_setting_service.get_automatic_multiplier()

    def get_automatic_dictionary(self) -> int:
        return self.calibration_setting_service.get_automatic_dictionary()

    def get_automatic_width(self) -> int:
        return self.calibration_setting_service.get_automatic_width()

    def get_automatic_height(self) -> int:
        return self.calibration_setting_service.get_automatic_height()

    def get_automatic_margin(self) -> int:
        return self.calibration_setting_service.get_automatic_margin()

    # ======================
    # SEMIAUTOMATIC CALIBRATION
    # ======================

    def get_semiautomatic_window_position(self) -> str:
        return (
            self.calibration_setting_service.get_semiautomatic_window_position()
        )

    def get_semiautomatic_window_open_mode(self) -> int:
        return (
            self.calibration_setting_service.get_semiautomatic_window_open_mode()
        )

    def is_semiautomatic_open_projector(self) -> bool:
        return (
            self.calibration_setting_service.is_semiautomatic_open_projector()
        )

    def is_semiautomatic_default_calibration(self) -> bool:
        return (
            self.calibration_setting_service.is_semiautomatic_default_calibration()
        )

    def is_semiautomatic_mirror_mode(self) -> bool:
        return self.calibration_setting_service.is_semiautomatic_mirror_mode()

    # ======================
    # MANUAL CALIBRATION
    # ======================

    def get_manual_window_position(self) -> str:
        return self.calibration_setting_service.get_manual_window_position()

    def get_manual_window_open_mode(self) -> int:
        return self.calibration_setting_service.get_manual_window_open_mode()

    def is_manual_open_projector(self) -> bool:
        return self.calibration_setting_service.is_manual_open_projector()

    def is_manual_default_calibration(self) -> bool:
        return self.calibration_setting_service.is_manual_default_calibration()

    def is_manual_mirror_mode(self) -> bool:
        return self.calibration_setting_service.is_manual_mirror_mode()
