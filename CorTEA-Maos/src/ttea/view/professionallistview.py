from typing import TYPE_CHECKING, Callable, List, Optional

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem

# Local module import
from ttea.controller import ProfessionalListController
from ttea.ui import Ui_ProfessionalListView  # Assuming generated UI class
from ttea.util import MessageService
from ttea.window import WindowConfig

# Type checking to prevent circular import on run time
if TYPE_CHECKING:
    from ttea.model import Professional
    from ttea.view import ProfessionalEditView


class ProfessionalListView(QDialog, Ui_ProfessionalListView, WindowConfig):
    def __init__(
        self,
        parent: Optional[QDialog] = None,
        professional_edit_view_factory: Optional[
            Callable[
                [Optional[QDialog], Optional["Professional"]],
                "ProfessionalEditView",
            ]
        ] = None,
    ) -> None:

        super().__init__(parent)
        # Setup UI interface Ui_PlayerListView
        self.setupUi(self)
        self.msg = MessageService(self)

        # Set up window properties
        self.setup_window(
            self.windowTitle(),
            self.windowIcon(),
            WindowConfig.DECREMENT_SIZE_PERCENT,
            10,
            5,
            parent,
        )

        # Initialize controller
        self.controller = ProfessionalListController(
            self, professional_edit_view_factory
        )

        # Perfect column widths
        self.tbl_professional.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.tbl_professional.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )

    # =====================================================================
    # High-level methods used by the Controller (required for decoupling)
    # =====================================================================
    def populate_table(self, professionals: List["Professional"]) -> None:
        """Fill the table with a list of professionals."""
        self.tbl_professional.blockSignals(True)
        self.tbl_professional.setRowCount(0)

        for professional in professionals:
            row = self.tbl_professional.rowCount()
            self.tbl_professional.insertRow(row)
            self.tbl_professional.setItem(
                row, 0, QTableWidgetItem(str(professional.id))
            )
            self.tbl_professional.setItem(
                row, 1, QTableWidgetItem(professional.name)
            )

        self.tbl_professional.blockSignals(False)

    def clear_details(self) -> None:
        """Clear all fields in the details panel."""
        self.lbl_id_value.setText("")
        self.lbl_name_value.setText("")
        self.lbl_type_value.setText("")

    def display_details(self, professional: Optional["Professional"]) -> None:
        """Show the selected professional's
        details in the right panel."""

        if not professional:
            self.clear_details()
            return

        self.lbl_id_value.setText(str(professional.id))
        self.lbl_name_value.setText(professional.name)
        self.lbl_type_value.setText(
            str(self.controller.get_professional_types()[professional.type])
        )

    def get_selected_id(self) -> Optional[int]:
        """Return the ID of the currently selected professional
        or None."""
        items = self.tbl_professional.selectedItems()
        if not items:
            return None
        try:
            return int(items[0].text())
        except (ValueError, AttributeError):
            return None

    def select_row_by_id(self, professional_id: int) -> None:
        """Programmatically select the row with
        the given professional ID."""
        if professional_id <= 0:
            return

        self.tbl_professional.blockSignals(True)
        for row in range(self.tbl_professional.rowCount()):
            item = self.tbl_professional.item(row, 0)
            if item and int(item.text()) == professional_id:
                self.tbl_professional.selectRow(row)
                self.tbl_professional.scrollToItem(item)
                break
        self.tbl_professional.blockSignals(False)
        self.controller.on_table_selection()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Override close event to confirm exit.

        Shows a confirmation dialog before allowing the window to close.

        Parameters
        ----------
        event : QCloseEvent
            The close event to accept or ignore.
        """
        if self.msg.question(self.tr("Deseja sair do cadastro?"), None, True):
            event.accept()
        else:
            event.ignore()
