from typing import TYPE_CHECKING, Callable, List, Optional

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem

# Local module import
from ttea.controller import PlayerListController
from ttea.ui import Ui_PlayerListView  # Assuming generated UI class
from ttea.util import MessageService, QtDateFormat
from ttea.window import WindowConfig

# Type checking to prevent circular import on run time
if TYPE_CHECKING:
    from ttea.model import Player
    from ttea.view import PlayerEditView


class PlayerListView(QDialog, Ui_PlayerListView, WindowConfig):
    """Dialog for displaying and managing the list of players.

    Modal window that shows a searchable table of players with quick actions
    for creating, editing and deleting records. Follows the MVC pattern:
    all business logic and data access are delegated to PlayerListController.

    Attributes
    ----------
    msg : MessageService
        Helper service used to show info/warning/question dialogs.
    controller : PlayerListController
        Controller that handles all CRUD operations and data flow.
    table : QTableWidget
        Table displaying ID and name of each player.
    new_button : QPushButton
        Button that opens the player creation dialog.
    edit_button : QPushButton
        Button that opens the edit dialog for the selected player.
    delete_button : QPushButton
        Button that removes the selected player after confirmation.
    search_input : QLineEdit
        Line edit used to filter players by ID or name.

    Methods
    -------
    __init__(parent=None, player_edit_view_factory=None)
        Initialise the dialog, UI, controller and signal connections.
    on_new_button_clicked()
        Delegate the "New" action to the controller.
    on_edit_button_clicked()
        Delegate the "Edit" action to the controller.
    on_delete_button_clicked()
        Delegate the "Delete" action to the controller.
    on_search_input_textChanged(text)
        Forward search text changes to the controller for filtering.
    on_table_selection_changed()
        Notify the controller when the table selection changes.
    closeEvent(event)
        Ask for confirmation before closing the dialog.
    """

    def __init__(
        self,
        parent: Optional[QDialog] = None,
        player_edit_view_factory: Optional[
            Callable[[Optional[QDialog], Optional["Player"]], "PlayerEditView"]
        ] = None,
    ) -> None:
        """Initialise the PlayerListView dialog.

        Parameters
        ----------
        parent : Optional[QDialog], default None
            Parent widget; used for translator and icon inheritance.
        player_edit_view_factory : Optional[Callable], default None
            Factory function that creates PlayerEditView instances.
            Enables dependency injection (useful for testing).
        """

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
        self.controller = PlayerListController(self, player_edit_view_factory)

        # Perfect column widths
        self.tbl_player.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.tbl_player.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )

    # =====================================================================
    # High-level methods used by the Controller (required for decoupling)
    # =====================================================================

    def populate_table(self, players: List["Player"]) -> None:
        """Fill the table with a list of players."""
        self.tbl_player.blockSignals(True)
        self.tbl_player.setRowCount(0)

        for player in players:
            row = self.tbl_player.rowCount()
            self.tbl_player.insertRow(row)
            self.tbl_player.setItem(row, 0, QTableWidgetItem(str(player.id)))
            self.tbl_player.setItem(row, 1, QTableWidgetItem(player.name))

        self.tbl_player.blockSignals(False)

    def clear_details(self) -> None:
        """Clear all fields in the details panel."""
        self.lbl_id_value.setText("")
        self.lbl_name_value.setText("")
        self.lbl_birth_date_value.setText("")
        self.lbl_observation_value.setText("")

    def display_details(self, player: Optional["Player"]) -> None:
        """Show the selected player's details in the right panel."""
        if not player:
            self.clear_details()
            return

        self.lbl_id_value.setText(str(player.id))
        self.lbl_name_value.setText(player.name)
        self.lbl_birth_date_value.setText(
            QtDateFormat.format_python_date(player.birth_date)
        )
        self.lbl_observation_value.setWordWrap(True)
        self.lbl_observation_value.setMaximumWidth(
            int(self.size().width()) / 2
        )
        self.lbl_observation_value.setText(player.observation or "—")

    def get_selected_id(self) -> Optional[int]:
        """Return the ID of the currently selected player or None."""
        items = self.tbl_player.selectedItems()
        if not items:
            return None
        try:
            return int(items[0].text())
        except (ValueError, AttributeError):
            return None

    def select_row_by_id(self, player_id: int) -> None:
        """Programmatically select the row with the given player ID."""
        if player_id <= 0:
            return

        self.tbl_player.blockSignals(True)
        for row in range(self.tbl_player.rowCount()):
            item = self.tbl_player.item(row, 0)
            if item and int(item.text()) == player_id:
                self.tbl_player.selectRow(row)
                self.tbl_player.scrollToItem(item)
                break
        self.tbl_player.blockSignals(False)
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
