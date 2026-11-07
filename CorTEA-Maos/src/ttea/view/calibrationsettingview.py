from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QDoubleSpinBox,
                               QRadioButton, QSpinBox)

# Local module import
from ttea.controller import CalibrationSettingController
from ttea.ui import Ui_CalibrationSettingView
from ttea.util import MessageService
from ttea.window import WindowConfig

if TYPE_CHECKING:
    from ttea.model import CalibrationSetting


class CalibrationSettingView(QDialog, Ui_CalibrationSettingView, WindowConfig):
    """
    A modal dialog window calibration T-TEA project.

    This class creates a modal dialog that provides calibration the T-TEA
    project.
    It inherits from `QDialog` for dialog functionality and `WindowConfig`
    for window configuration.

    Methods
    -------
    __init__(parent=None)
        Initializes the AboutView dialog with the specified parent.
    """

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
            WindowConfig.INCREMENT_SIZE_PERCENT,  # status
            5,  # width
            75,  # height
            parent,  # parent
        )
        # Initialize controller
        self.controller = CalibrationSettingController(self)

        self.pb_ok.clicked.connect(self.controller.handle_ok)
        self.pb_cancel.clicked.connect(self.controller.handle_cancel)

        self.chk_custom_camera.toggled.connect(self.grp_camera_info.setEnabled)
        self.chk_custom_camera.toggled.connect(self.grp_fps.setEnabled)
        self.chk_enable_filter.toggled.connect(self.grp_filter.setEnabled)

        self.grp_camera_info.setEnabled(self.chk_custom_camera.isChecked())
        self.cbx_ratio.setEnabled(self.chk_custom_camera.isChecked())
        self.grp_fps.setEnabled(self.chk_custom_camera.isChecked())
        self.grp_filter.setEnabled(self.chk_enable_filter.isChecked())

    def get_data(self) -> Dict[str, Any]:
        # Busca todos os widgets genéricos da árvore
        from PySide6.QtWidgets import QWidget

        data: Dict[str, Any] = {}

        widgets_to_scan = self.findChildren(QWidget)

        for widget in widgets_to_scan:  # self.findChildren(widgets_to_scan):

            # Alinhado com o nome configurado no Qt Designer
            prop_name = widget.property("dataclass_property")
            if not prop_name:
                continue  # Ignora componentes sem o mapeamento configurado

            # Trata os widgets padrão
            if isinstance(widget, QCheckBox):
                data[prop_name] = 1 if widget.isChecked() else 0
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                data[prop_name] = widget.value()
            elif isinstance(widget, QComboBox):
                data[prop_name] = widget.currentText()
            elif isinstance(widget, QRadioButton):
                # Atribui o valor apenas se o Radio Button específico estiver selecionado
                if widget.isChecked():
                    prop_value = widget.property("dataclass_property_value")

                    if prop_value is None:
                        prop_value = widget.text()
                    data[prop_name] = prop_value

        return data

    def set_data(
        self, data: Union[Dict[str, Any], "CalibrationSetting"]
    ) -> None:
        from PySide6.QtWidgets import QWidget

        # Converte para dicionário caso receba a instância de CalibrationSetting
        if hasattr(data, "get_data"):
            data_dict = data.get_data()[0]
        elif isinstance(data, dict):
            data_dict = data
        else:
            return

        # Varrer todos os widgets procurando a propriedade 'dataclass_property'
        for widget in self.findChildren(QWidget):
            prop_name = widget.property("dataclass_property")
            if not prop_name or prop_name not in data_dict:
                continue

            value = data_dict[prop_name]

            # Ignora valores nulos ou em branco
            if value is None or str(value).strip() == "":
                continue

            if isinstance(widget, QCheckBox):
                # Converte 1/0 ou bool para o checkbox
                widget.setChecked(bool(int(value)))

            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.setValue(
                    float(value)
                    if isinstance(widget, QDoubleSpinBox)
                    else int(value)
                )

            elif isinstance(widget, QComboBox):
                # Busca e seleciona a opção correspondente pelo texto do ComboBox
                index = widget.findText(str(value))
                if index >= 0:
                    widget.setCurrentIndex(index)

            elif isinstance(widget, QRadioButton):
                prop_value = widget.property("dataclass_property_value")

                # Se prop_value existir, compara com ele; caso contrário, compara com widget.text()
                target_value = (
                    str(prop_value)
                    if prop_value is not None
                    else widget.text()
                )
                # Marca o RadioButton cujo texto coincida com o valor carregado
                # if widget.text() == str(value):
                if target_value == str(value):
                    widget.setChecked(True)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Override close event to confirm exit.

        Shows a confirmation dialog before allowing the window to close.

        Parameters
        ----------
        event : QCloseEvent
            The close event to accept or ignore.
        """
        if self.msg.question(
            self.tr("Deseja sair da configuração da calibração?"), None, True
        ):
            event.accept()
        else:
            event.ignore()
