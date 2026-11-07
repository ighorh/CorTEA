from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QButtonGroup

from ttea.service import CalibrationSettingService

if TYPE_CHECKING:
    from ttea.view import CalibrationSettingView


class CalibrationSettingController(QObject):

    def __init__(
        self,
        view: "CalibrationSettingView",
        service: Optional[CalibrationSettingService] = None,
    ):
        self.view = view
        self.service = service or CalibrationSettingService()
        self._initialize_view()
        self._setup_calibration_group()

    def _setup_calibration_group(self) -> None:
        """Agrupa os checkboxes de calibração para garantir exclusividade mútua."""
        self.calibration_group = QButtonGroup(self.view)
        self.calibration_group.setExclusive(True)

        self.calibration_group.addButton(
            self.view.chk_default_calibration_automatic
        )
        self.calibration_group.addButton(
            self.view.chk_default_calibration_manual
        )
        self.calibration_group.addButton(
            self.view.chk_default_calibration_semiautomatic
        )

    def _initialize_view(self):
        self.list_proportions()
        self._load_saved_settings()

    def _load_saved_settings(self):
        calibration_setting = self.service.dao.select(0)

        if calibration_setting:
            self.view.set_data(calibration_setting)

    def list_proportions(self) -> None:
        for text, value in self.service.get_proportions():
            self.view.cbx_ratio.addItem(text, value)

    def handle_ok(self) -> None:
        data = self.view.get_data()

        # O Service cria o objeto, valida e salva via DAO
        calibration = self.service.create_calibration_setting(data)

        if calibration:
            self.view.msg.info(
                self.tr("Configuração de calibração cadastrada com sucesso!")
            )
            self.view.accept()
        else:
            self.view.msg.critical(
                self.tr("Erro ao salvar a configuração de calibração.")
            )

    def handle_cancel(self) -> None:
        self.view.reject()
