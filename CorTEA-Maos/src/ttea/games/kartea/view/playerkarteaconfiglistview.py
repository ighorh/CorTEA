from typing import TYPE_CHECKING, Callable, List, Optional

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QHeaderView, QTableWidgetItem

# Local module import
from ttea.games.kartea.controller import PlayerKarteaConfigListController
from ttea.games.kartea.ui import \
    Ui_PlayerKarteaConfigListView  # Assuming generated UI class
from ttea.util import MessageService
from ttea.window import WindowConfig

# Type checking to prevent circular import on run time
if TYPE_CHECKING:
    from ttea.games.kartea.model import PlayerKarteaConfig
    from ttea.games.kartea.view import PlayerKarteaConfigEditView


class PlayerKarteaConfigListView(
    QDialog, Ui_PlayerKarteaConfigListView, WindowConfig
):
    """Dialog for displaying and managing the list of PlayerKarteaConfig.

    Modal window that shows a searchable table of configs with quick actions
    for creating, editing and deleting records. Follows the MVC pattern:
    all business logic and data access are delegated to PlayerKarteaConfigListController.

    Attributes
    ----------
    msg : MessageService
        Helper service used to show info/warning/question dialogs.
    controller : PlayerKarteaConfigListController
        Controller that handles all CRUD operations and data flow.
    tbl_config : QTableWidget
        Table displaying ID and name of each player config.
    pb_new : QPushButton
        Button that opens the config creation dialog.
    pb_edit : QPushButton
        Button that opens the edit dialog for the selected config.
    pb_delete : QPushButton
        Button that removes the selected config after confirmation.
    led_search : QLineEdit
        Line edit used to filter configs by ID or name.

    Methods
    -------
    __init__(parent=None, player_kartea_config_edit_view_factory=None)
        Initialise the dialog, UI, controller and signal connections.
    closeEvent(event)
        Ask for confirmation before closing the dialog.
    """

    def __init__(
        self,
        parent: Optional[QDialog] = None,
        player_kartea_config_edit_view_factory: Optional[
            Callable[
                [Optional[QDialog], Optional["PlayerKarteaConfig"]],
                "PlayerKarteaConfigEditView",
            ]
        ] = None,
    ) -> None:
        """Initialise the PlayerKarteaConfigListView dialog.

        Parameters
        ----------
        parent : Optional[QDialog], default None
            Parent widget; used for translator and icon inheritance.
        player_kartea_config_edit_view_factory : Optional[Callable], default None
            Factory function that creates PlayerKarteaConfigEditView instances.
            Enables dependency injection (useful for testing).
        """
        super().__init__(parent)

        # Setup UI interface Ui_PlayerKarteaConfigListView
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
        self.controller = PlayerKarteaConfigListController(
            self, player_kartea_config_edit_view_factory
        )

        # Events signals and slots
        self.pb_new.clicked.connect(self.controller.handle_new_config)
        self.pb_edit.clicked.connect(self.controller.handle_edit_config)
        self.pb_delete.clicked.connect(self.controller.delete_config)
        self.led_search.textChanged.connect(self.controller.filter_configs)
        self.tbl_config.selectionModel().selectionChanged.connect(
            self.controller.on_table_selection
        )

        # Load initial data
        self.controller.load_configs()

        # Perfect column widths
        self.tbl_config.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.tbl_config.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )

    # =====================================================================
    # High-level methods used by the Controller (required for decoupling)
    # =====================================================================

    def populate_table(self, configs: List["PlayerKarteaConfig"]) -> None:
        """Fill the table with a list of configs."""
        self.tbl_config.blockSignals(True)
        self.tbl_config.setRowCount(0)

        for config in configs:
            row = self.tbl_config.rowCount()
            self.tbl_config.insertRow(row)
            self.tbl_config.setItem(
                row, 0, QTableWidgetItem(str(config.player.id))
            )
            self.tbl_config.setItem(
                row, 1, QTableWidgetItem(config.player.name)
            )

        self.tbl_config.blockSignals(False)

    def clear_details(self) -> None:
        """Clear all fields in the details panel."""
        self.lbl_id_value.setText("")
        self.lbl_name_value.setText("")
        self.lbl_phase_value.setText("")
        self.lbl_level_value.setText("")
        self.lbl_time_value.setText("")

    def display_config_details(
        self, config: Optional["PlayerKarteaConfig"]
    ) -> None:
        """Show the selected config's details in the right panel."""
        if not config:
            self.clear_details()
            return

        self.lbl_id_value.setText(str(config.player.id))
        self.lbl_name_value.setText(config.player.name)
        self.lbl_phase_value.setText(
            str(config.phase.id) if config.phase else ""
        )
        self.lbl_level_value.setText(
            str(config.level.id) if config.level else ""
        )
        self.lbl_time_value.setText(str(config.level_time))

    def get_selected_player_id(self) -> Optional[int]:
        """Return the ID of the currently selected config or None."""
        items = self.tbl_config.selectedItems()
        if not items:
            return None
        try:
            return int(items[0].text())
        except (ValueError, AttributeError):
            return None

    def select_row_by_id(self, player_id: int) -> None:
        """Programmatically select the row with the given player ID."""
        self.tbl_config.blockSignals(True)
        for row in range(self.tbl_config.rowCount()):
            item = self.tbl_config.item(row, 0)
            if item and int(item.text()) == player_id:
                self.tbl_config.selectRow(row)
                self.tbl_config.scrollToItem(item)
                break
        self.tbl_config.blockSignals(False)

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
