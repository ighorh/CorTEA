from typing import Optional

import cv2
from PySide6.QtGui import QCloseEvent, QKeyEvent
from PySide6.QtWidgets import QDialog

# Local module import
from ttea.controller import ManualCalibrationController
from ttea.model import CalibrationSetting
from ttea.ui import Ui_ManualCalibrationView
from ttea.util import MessageService
from ttea.window import WindowConfig


class ManualCalibrationView(QDialog, Ui_ManualCalibrationView, WindowConfig):

    def __init__(
        self,
        parent: Optional[QDialog] = None,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.msg = MessageService(self)

        self.setup_window(
            None,
            None,
            WindowConfig.STAY_SIZE,  # status
            0,  # width
            0,  # height
            parent,  # parent
        )

        camera_idx = (
            self.parent().cbx_camera.currentIndex() if self.parent() else 0
        )

        monitor_idx = (
            self.parent().cbx_monitor.currentIndex() if self.parent() else 0
        )

        # Initialize controller
        self.controller = ManualCalibrationController(
            self, camera_index=camera_idx, monitor_index=monitor_idx
        )

        if self.controller.service.is_manual_open_projector():
            screen_geometry = self.controller.get_available_geometry_of_screen(
                monitor_idx
            )
        else:
            monitor_idx = 0
            screen_geometry = self.controller.get_available_geometry_of_screen(
                monitor_idx
            )

        position_name = self.controller.service.get_manual_window_position()

        position_func = getattr(screen_geometry, position_name, None)

        if callable(position_func):
            target_point = position_func()
        else:
            target_point = screen_geometry.topLeft()

        self.move(target_point)

        mode = self.controller.service.get_manual_window_open_mode()

        if mode == CalibrationSetting.FULLSCREEN:
            self.showFullScreen()
        elif mode == CalibrationSetting.MAXIMIZED:
            self.showMaximized()
            self.setFixedSize(
                screen_geometry.width(),
                screen_geometry.height(),
            )
        elif mode == CalibrationSetting.MAXIMIZED_UTIL:
            screen_geometry = self.controller.get_available_geometry_of_screen(
                monitor_idx
            )
            self.showMaximized()
            self.setFixedSize(
                screen_geometry.width(),
                screen_geometry.height(),
            )

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Encaminha o evento de teclado para o controller"""
        self.controller.keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Override close event to confirm exit.

        Shows a confirmation dialog before allowing the window to close.

        Parameters
        ----------
        event : QCloseEvent
            The close event to accept or ignore.
        """
        if self.msg.question(
            self.tr("Deseja sair da calibração manual?"), None, True
        ):
            if self.controller.camera is not None:
                self.controller.camera.release()
                cv2.destroyAllWindows()
                self.controller.camera_timer.stop()
                self.controller.create_calibration_point()
            event.accept()
        else:
            event.ignore()
