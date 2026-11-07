from typing import TYPE_CHECKING, Callable, List, Optional

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem

# Local module import
from ttea.controller import InstitutionFacilityListController
from ttea.ui import \
    Ui_InstitutionFacilityListView  # Assuming generated UI class
from ttea.util import MessageService
from ttea.window import WindowConfig

# Type checking to prevent circular import on run time
if TYPE_CHECKING:
    from ttea.model import InstitutionFacility
    from ttea.view import InstitutionFacilityEditView


class InstitutionFacilityListView(
    QDialog, Ui_InstitutionFacilityListView, WindowConfig
):
    def __init__(
        self,
        parent: Optional[QDialog] = None,
        institutionfacility_edit_view_factory: Optional[
            Callable[
                [Optional[QDialog], Optional["InstitutionFacility"]],
                "InstitutionFacilityEditView",
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
        self.controller = InstitutionFacilityListController(
            self, institutionfacility_edit_view_factory
        )

        # Perfect column widths
        self.tbl_institution.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.tbl_institution.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )

    # =====================================================================
    # High-level methods used by the Controller (required for decoupling)
    # =====================================================================
    def populate_table(
        self, institutionfacilities: List["InstitutionFacility"]
    ) -> None:
        """Fill the table with a list of institutionfacilities."""
        self.tbl_institution.blockSignals(True)
        self.tbl_institution.setRowCount(0)

        for institutionfacility in institutionfacilities:
            row = self.tbl_institution.rowCount()
            self.tbl_institution.insertRow(row)
            self.tbl_institution.setItem(
                row, 0, QTableWidgetItem(str(institutionfacility.id))
            )
            self.tbl_institution.setItem(
                row, 1, QTableWidgetItem(institutionfacility.name)
            )

        self.tbl_institution.blockSignals(False)

    def clear_details(self) -> None:
        """Clear all fields in the details panel."""
        self.lbl_id_value.setText("")
        self.lbl_name_value.setText("")
        self.lbl_type_value.setText("")
        self.lbl_address_value.setText("")

    def display_details(
        self, institutionfacility: Optional["InstitutionFacility"]
    ) -> None:
        """Show the selected institutionfacility's
        details in the right panel."""

        if not institutionfacility:
            self.clear_details()
            return

        self.lbl_id_value.setText(str(institutionfacility.id))
        self.lbl_name_value.setText(institutionfacility.name)
        self.lbl_type_value.setText(
            str(
                self.controller.get_institutionfacility_types()[
                    institutionfacility.type
                ]
            )
        )
        self.lbl_address_value.setText(institutionfacility.address or "—")

    def get_selected_id(self) -> Optional[int]:
        """Return the ID of the currently selected institutionfacility
        or None."""
        items = self.tbl_institution.selectedItems()
        if not items:
            return None
        try:
            return int(items[0].text())
        except (ValueError, AttributeError):
            return None

    def select_row_by_id(self, institutionfacility_id: int) -> None:
        """Programmatically select the row with
        the given institutionfacility ID."""

        if institutionfacility_id <= 0:
            return

        self.tbl_institution.blockSignals(True)
        for row in range(self.tbl_institution.rowCount()):
            item = self.tbl_institution.item(row, 0)
            if item and int(item.text()) == institutionfacility_id:
                self.tbl_institution.selectRow(row)
                self.tbl_institution.scrollToItem(item)
                break
        self.tbl_institution.blockSignals(False)
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
