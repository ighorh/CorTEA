from typing import Optional

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog

# Local module import
from ttea.controller import CalibrationController
from ttea.ui import Ui_CalibrationView
from ttea.util import MessageService
from ttea.window import WindowConfig


class CalibrationView(QDialog, Ui_CalibrationView, WindowConfig):
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
        self.controller = CalibrationController(self)
        self.pb_camera.clicked.connect(self.controller.control_camera)

        self.pb_calibrate_auto.clicked.connect(
            self.controller.handle_calibrate_auto
        )
        self.pb_calibrate_semi.clicked.connect(
            self.controller.handle_calibrate_semi
        )
        self.pb_calibrate_semi.setVisible(False)

        self.pb_calibrate_manual.clicked.connect(
            self.controller.handle_calibrate_manual
        )

        self.pb_ok.clicked.connect(self.controller.handle_ok)
        self.pb_cancel.clicked.connect(self.controller.handle_cancel)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Override close event to confirm exit.

        Shows a confirmation dialog before allowing the window to close.

        Parameters
        ----------
        event : QCloseEvent
            The close event to accept or ignore.
        """
        if self.msg.question(
            self.tr("Deseja sair da calibração?"), None, True
        ):
            if self.controller.thread:
                self.controller.thread.stop()
            event.accept()
        else:
            event.ignore()
