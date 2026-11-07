import threading
from typing import Optional

import cv2
from PySide6.QtGui import QCloseEvent, QPainter, QPaintEvent, QShowEvent
from PySide6.QtWidgets import QDialog

# Local module import
from ttea.controller import AutomaticCalibrationController
from ttea.model import CalibrationSetting
from ttea.ui import Ui_AutomaticCalibrationView
from ttea.util import MessageService
from ttea.window import WindowConfig


class AutomaticCalibrationView(
    QDialog, Ui_AutomaticCalibrationView, WindowConfig
):

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

        self.is_finished = False

        # Initialize controller
        self.controller = AutomaticCalibrationController(
            self, camera_index=camera_idx, monitor_index=monitor_idx
        )

        self.controller.msg_info_signal.connect(self.handle_info_then_close)
        self.controller.msg_warning_signal.connect(self.msg.warning)
        self.controller.msg_critical_signal.connect(self.msg.critical)

        if self.controller.service.is_automatic_open_projector():
            screen_geometry = self.controller.get_available_geometry_of_screen(
                monitor_idx
            )
        else:
            monitor_idx = 0
            screen_geometry = self.controller.get_available_geometry_of_screen(
                monitor_idx
            )

        position_name = self.controller.service.get_automatic_window_position()

        position_func = getattr(screen_geometry, position_name, None)

        if callable(position_func):
            target_point = position_func()
        else:
            target_point = screen_geometry.topLeft()

        self.move(target_point)

        mode = self.controller.service.get_automatic_window_open_mode()

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

            # Guardamos a imagem gerada em um atributo da View
        self.board_pixmap = self.controller.generate_board_pixmap()

    def handle_info_then_close(self, message: str) -> None:
        """
        Exibe a caixa de OK na thread principal.
        Como self.msg.info é síncrono, a execução PAUSA aqui até o usuário clicar em 'OK'.
        Somente depois do clique no 'OK', é chamado o self.close().
        """
        self.msg.info(message)

        if not self.isVisible():
            return

        msg_sucesso = self.tr("Calibração automática cadastrada com sucesso!")
        msg_sem_salvar = self.tr("Fechando sem salvar.")

        if message in (msg_sucesso, msg_sem_salvar):
            self.is_finished = True
            self.close()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Desenha o tabuleiro no fundo do Dialog preenchendo toda a tela."""
        super().paintEvent(event)
        if hasattr(self, "board_pixmap") and not self.board_pixmap.isNull():
            painter = QPainter(self)
            # Desenha a imagem cobrindo toda a área da janela
            painter.drawPixmap(self.rect(), self.board_pixmap)

    def showEvent(self, event: QShowEvent) -> None:
        """
        Gatilho acionado automaticamente assim que a janela é exibida no projetor.
        Inicia a thread de captura e calibração para não travar a interface.
        """
        super().showEvent(event)

        # Executa o loop do OpenCV em uma Thread separada para a janela do PySide6 continuar respondendo
        calib_thread = threading.Thread(
            target=self.controller.run_auto_calibration, daemon=True
        )
        calib_thread.start()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Override close event to confirm exit.

        Shows a confirmation dialog before allowing the window to close.

        Parameters
        ----------
        event : QCloseEvent
            The close event to accept or ignore.
        """
        if self.is_finished:
            if self.controller.camera is not None:
                self.controller.camera.release()
                cv2.destroyAllWindows()
            event.accept()
            return

        if self.msg.question(
            self.tr("Deseja sair da calibração automática?"), None, True
        ):
            if self.controller.camera is not None:
                self.controller.camera.release()
                cv2.destroyAllWindows()
            event.accept()
        else:
            event.ignore()
