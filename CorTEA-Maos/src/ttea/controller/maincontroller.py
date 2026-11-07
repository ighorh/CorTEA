# /controller/maincontroller.py
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject

from ttea.service import MainService

if TYPE_CHECKING:
    from ttea.model import AppModel
    from ttea.util import MessageService
    from ttea.view.mainview import MainView  # Apenas para type hint


class MainController(QObject):
    def __init__(
        self,
        view: "MainView",
        model: "AppModel",
        message_service: "MessageService",
    ):
        from ttea.factory import ViewFactory

        super().__init__(parent=view)
        self.view = view
        self.model = model
        self.message_service = message_service

        # Serviço principal (recebe MessageService injetado)
        self.app_service = MainService(
            model=model, message_service=message_service
        )

        # Factories
        self.app_factory = ViewFactory.get_app_view_factory()
        self.kartea_factory = ViewFactory.get_kartea_view_factory()

        self._is_quitting = False

    # ------------------------------------------------------------------
    def handle_exit(self) -> None:
        if self._is_quitting:
            return  # já estamos saindo, não faz nada

        if self.app_service.confirm_exit():
            self._is_quitting = True
            self.app_service.quit_application()

    def try_close(self) -> bool:
        if self._is_quitting:
            return True
        if self.app_service.confirm_exit():
            self._is_quitting = True
            self.app_service.quit_application()
            return True
        return False

    def open_player_list(self) -> None:
        dialog = self.app_factory.create_player_list_view(
            self.view,
            self.app_factory.create_player_edit_view,
        )
        dialog.exec()

    def open_professional_list(self) -> None:
        dialog = self.app_factory.create_professional_list_view(
            self.view,
            self.app_factory.create_professional_edit_view,
        )
        dialog.exec()

    def open_institutionfacility_list(self) -> None:
        dialog = self.app_factory.create_institutionfacility_list_view(
            self.view,
            self.app_factory.create_institutionfacility_edit_view,
        )
        dialog.exec()

    def open_kartea_player_config(self) -> None:
        dialog = self.kartea_factory.create_player_kartea_config_list_view(
            self.view,
            self.kartea_factory.create_player_kartea_config_edit_view,
        )
        dialog.exec()

    def open_calibration(self) -> None:
        dialog = self.app_factory.create_calibration_view(parent=self.view)
        dialog.exec()

    def open_calibration_setting(self) -> None:
        dialog = self.app_factory.create_calibrationsetting_view(
            parent=self.view
        )
        dialog.exec()

    def open_help(self) -> None:
        self.view.update_status_message(
            self.tr("Funcionalidade do help em desenvolvimento...")
        )
        """try:
            # open_help()
            pass
        except Exception as e:
            self.view.show_critical_error(
                self.tr("Erro ao abrir ajuda."), str(e)
            )"""

    def open_language(self) -> None:
        dialog = self.app_factory.create_language_view(parent=self.view)
        dialog.exec()

        if hasattr(self.view, "retranslateUi"):
            self.view.retranslateUi(self.view)
            self.view.setup_status_bar()

    def open_about(self) -> None:
        dialog = self.app_factory.create_about_view(parent=self.view)
        dialog.exec()

    def open_playergamelaunch(self) -> None:
        dialog = self.app_factory.create_playergamelauch_view(parent=self.view)
        dialog.exec()
