from typing import TYPE_CHECKING, Callable, Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QDialog

from ttea.games.kartea.model import PlayerKarteaConfig
from ttea.games.kartea.service import PlayerKarteaConfigService
from ttea.util import MessageService

if TYPE_CHECKING:
    from ttea.games.kartea.view import (PlayerKarteaConfigEditView,
                                        PlayerKarteaConfigListView)


class PlayerKarteaConfigListController(QObject):
    """
    Lightweight controller that orchestrates PlayerKarteaConfigListView
    and PlayerKarteaConfigService.

    Follows MVCS pattern: mediates between view and service layer,
    handling user interactions and updating the UI accordingly.

    Attributes
    ----------
    view : PlayerKarteaConfigListView
        Main view displaying the list and details of configs.
    factory : Callable
        Factory function that creates a ``PlayerKarteaConfigEditView`` dialog,
        receiving the parent view and an optional player to edit.
    service : PlayerKarteaConfigService
        Business logic layer for player CRUD operations.
    msg : MessageService
        Helper for showing info, warning, and error messages.

    Methods
    -------
    __init__(view, player_edit_view_factory)
        Initializes the controller with view and edit dialog factory.
    load_configs(query="")
        Loads and displays configs, optionally filtered by search term.
    filter_configs(text)
        Filters the config list based on the search input text.
    on_table_selection()
        Updates details panel when a table row is selected.
    select_and_show_config(player_id)
        Selects a config row and shows its details.
    handle_new_config()
        Opens dialog to create a new config.
    handle_edit_config()
        Opens dialog to edit the selected config.
    delete_config()
        Deletes the selected config after confirmation.
    """

    def __init__(
        self,
        view: "PlayerKarteaConfigListView",
        player_kartea_config_edit_view_factory: Callable[
            [Optional[QDialog], Optional[PlayerKarteaConfig]],
            "PlayerKarteaConfigEditView",
        ],
    ) -> None:
        """
        Initialize the controller.

        Parameters
        ----------
        view : PlayerKarteaConfigListView
            The main list view instance to control.
        player_kartea_config_edit_view_factory : Callable
            Function that returns a ``PlayerKarteaConfigEditView`` dialog.
            Signature: (parent_view, playerkarteaconfig) -> PlayerKarteaConfigEditView.
        """
        self.view = view
        self.factory = player_kartea_config_edit_view_factory
        self.service = PlayerKarteaConfigService()
        self.msg = MessageService(view)

    def load_configs(self, search_query: str = "") -> None:
        """
        Load players configs from service and populate the table view.

        Parameters
        ----------
        query : str, optional
            Search term to filter players (default is empty string).
        """
        configs = self.service.search_configs(search_query)
        self.view.populate_table(configs)
        self.view.clear_details()

    def filter_configs(self, text: str) -> None:
        """Filter player config list based on search input text."""
        self.load_configs(text.strip())

    def on_table_selection(self) -> None:
        """Update details pane when a player config is selected in the table."""
        player_id = self.view.get_selected_player_id()
        if player_id is not None:
            config = self.service.find_config_by_player_id(player_id)
            self.view.display_config_details(config)
        else:
            self.view.clear_details()

    def select_and_show_config(self, player_id: int) -> None:
        """
        Select a player config row by ID and display its details.

        Parameters
        ----------
        player_id : int
            The ID of the player config to select and show.
        """
        config = self.service.find_config_by_player_id(player_id)
        if config:
            self.view.display_config_details(config)
            self.view.select_row_by_id(player_id)

    def handle_new_config(self) -> None:
        """Open dialog to create a new player config and save if accepted."""
        dialog = self.factory(self.view, None)
        if not dialog.exec():
            return

        data = dialog.controller.get_data()
        config = self.service.create_config(data)
        if config:
            self.load_configs(self.view.led_search.text())
            self.select_and_show_config(config.player.id)
            self.msg.info(self.tr("Configuração cadastrada com sucesso!"))
        else:
            self.msg.critical(self.tr("Erro ao salvar configuração."))

    def handle_edit_config(self) -> None:
        """Open dialog to edit the selected player config
        and update if accepted."""
        player_id = self.view.get_selected_player_id()
        if not player_id:
            self.msg.warning(
                self.tr("Selecione uma configuração para editar.")
            )
            return

        config = self.service.find_config_by_player_id(player_id)
        if not config:
            self.msg.critical(self.tr("Configuração não encontrada."))
            return

        dialog = self.factory(self.view, config)
        if not dialog.exec():
            return

        data = dialog.controller.get_data()
        if self.service.update_config(player_id, data):
            self.load_configs(self.view.led_search.text())
            self.select_and_show_config(player_id)
            self.msg.info(self.tr("Configuração atualizada com sucesso."))
        else:
            self.msg.critical(self.tr("Erro ao atualizar configuração."))

    def delete_config(self) -> None:
        """Delete the selected player config after user confirmation."""
        player_id = self.view.get_selected_player_id()
        if not player_id:
            self.msg.warning(
                self.tr("Selecione uma configuração para excluir.")
            )
            return

        config = self.service.find_config_by_player_id(player_id)
        if not config:
            return

        if self.msg.question(
            self.tr(
                "Tem certeza que seja excluir a configuração do jogador?\n{0}"
            ).format(config.player.name)
        ):
            if self.service.delete_config(player_id):
                self.load_configs(self.view.led_search.text())
                self.view.clear_details()
                self.msg.info(self.tr("Configuração excluída com sucesso."))
            else:
                self.msg.critical(self.tr("Erro ao excluir configuração."))
