# mainview.py
from datetime import date, datetime
from typing import Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel, QMainWindow, QStatusBar, QWidget

from ttea.app import AppConfig
from ttea.controller import MainController
from ttea.model import AppModel
from ttea.ui import Ui_MainView
from ttea.util import MessageService
from ttea.window import WindowConfig


class MainView(QMainWindow, Ui_MainView, WindowConfig):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
    ):

        super().__init__(parent)
        self.setupUi(self)

        self.setup_window(
            AppConfig.get_title(),
            None,
            WindowConfig.DECREMENT_SIZE_PERCENT,
            5,
            5,
            parent,
        )

        self.controller = MainController(
            self, AppModel.get_instance(), MessageService(self)
        )

        # === CONEXÕES DIRETAS DOS WIDGETS/ACTIONS AO CONTROLLER ===
        self.act_exit.triggered.connect(self.controller.handle_exit)
        self.act_professional.triggered.connect(
            self.controller.open_professional_list
        )
        self.act_institutionfacility.triggered.connect(
            self.controller.open_institutionfacility_list
        )
        self.act_player.triggered.connect(self.controller.open_player_list)
        self.act_kartea.triggered.connect(
            self.controller.open_kartea_player_config
        )
        self.act_calibration.triggered.connect(
            self.controller.open_calibration
        )

        self.act_calibration_setting.triggered.connect(
            self.controller.open_calibration_setting
        )

        self.act_language.triggered.connect(self.controller.open_language)
        self.act_help.triggered.connect(self.controller.open_help)
        self.act_about.triggered.connect(self.controller.open_about)

        self.act_player_game.triggered.connect(
            self.controller.open_playergamelaunch
        )

        self.msg = MessageService(self)
        self.setup_status_bar()

    def setup_status_bar(self):
        """Cria o QLabel com versão e data e adiciona permanentemente na status bar"""

        # Atualização inicial
        self.update_status_info_time()

        # Timer que atualiza a cada 1 segundo
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status_info_time)
        self.status_timer.start(1000)

    def update_status_info_time(self):
        """Atualiza data + hora na status bar (chamado automaticamente pelo timer)"""
        version = self.tr("Versão da plataforma: {0}")
        version = version.format(AppConfig.VERSION)

        date_mask = AppConfig.get_geral_date_mask()
        hour_mask = AppConfig.get_geral_hour_minute_mask()

        current_date = self.tr("Data atual: {0}").format(
            date.today().strftime(date_mask)
        )
        current_hour = datetime.now().strftime(hour_mask)

        status_text = version + " | " + current_date + " - " + current_hour
        status_bar_label = QLabel(status_text)
        status_bar_label.setAlignment(Qt.AlignRight)
        status_bar_label.setStyleSheet("border: 1px sunken; padding: 2px;")
        status_bar = QStatusBar()
        status_bar.addPermanentWidget(status_bar_label)
        self.setStatusBar(status_bar)

    def update_status_message(self, message: str, timeout: int = 6000):
        self.statusBar().showMessage(message, timeout)

    def show_critical_error(self, title: str, text: str):
        self.msg.critical(text, title)

    def closeEvent(self, event: QCloseEvent) -> None:
        if hasattr(self, "status_timer"):
            self.status_timer.stop()
        if self.controller.try_close():
            event.accept()
        else:
            event.ignore()
