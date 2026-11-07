from typing import TYPE_CHECKING, Callable, Dict

from PySide6.QtCore import QObject

# Local module import
from ttea.exception import BusinessRuleException
from ttea.service import InstitutionFacilityService
from ttea.util import MessageService

if TYPE_CHECKING:
    from ttea.view import (InstitutionFacilityEditView,
                           InstitutionFacilityListView)


class InstitutionFacilityListController(QObject):
    """
    Lightweight controller that orchestrates InstitutionFacilityListView
    and InstitutionFacilityService.

    Follows MVCS pattern: mediates between view and service layer,
    handling user interactions and updating the UI accordingly.

    Attributes
    ----------
    view : InstitutionFacilityListView
        Main view displaying the list and details of institutionfacilities.
    factory : Callable
        Factory function that creates a ``InstitutionFacilityEditView`` dialog,
        receiving the parent view and an optional institutionfacility to edit.
    service : InstitutionFacilityService
        Business logic layer for institutionfacility CRUD operations.
    msg : MessageService
        Helper for showing info, warning, and error messages.

    Methods
    -------
    __init__(view, institutionfacility_edit_view_factory)
        Initializes the controller with view and edit dialog factory.
    load_institutionfacilities(query="")
        Loads and displays institutionfacilities, optionally filtered
        by search term.
    filter_institutionfacilities(text)
        Filters the institutionfacility list based on the search input text.
    on_table_selection()
        Updates details panel when a table row is selected.
    select_and_show_institutionfacility(institutionfacility_id)
        Selects a institutionfacility row and shows its details.
    handle_new_institutionfacility()
        Opens dialog to create a new institutionfacility.
    handle_edit_institutionfacility()
        Opens dialog to edit the selected institutionfacility.
    delete_institutionfacility()
        Deletes the selected institutionfacility after confirmation.
    """

    def __init__(
        self, view: "InstitutionFacilityListView", factory: Callable
    ) -> None:
        """
        Initialize the controller.

        Parameters
        ----------
        view : InstitutionFacilityListView
            The main list view instance to control.
        institutionfacility_edit_view_factory : Callable
            Function that returns a ``InstitutionFacilityEditView`` dialog.
            Signature: (parent_view, institutionfacility)
            -> InstitutionFacilityEditView.
        """
        self.view = view
        self.factory = factory
        self.service = InstitutionFacilityService()
        self.msg = MessageService(self.view)

        # ------------------------------------------------------------------
        # OBSERVER PATTERN: Conexão reativa
        # ------------------------------------------------------------------
        # Sempre que o serviço emitir que os dados mudaram, a lista recarrega.
        self.service.institutionfacility_change.connect(self.reload_data)

        # Events signals and slots
        self.view.pb_new.clicked.connect(self.create_institutionfacility)
        self.view.pb_edit.clicked.connect(self.update_institutionfacility)
        self.view.pb_delete.clicked.connect(self.delete_institutionfacility)
        self.view.led_search.textChanged.connect(
            self.filter_institutionfacilities
        )
        self.view.tbl_institution.itemSelectionChanged.connect(
            self.on_table_selection
        )

        # Carga inicial
        self.load_institutionfacilities()

    def reload_data(self, target_id: int = 0) -> None:
        """
        Slot que reage ao sinal do Service.
        Mantém o filtro atual ao recarregar.
        """
        if target_id == 0:
            target_id = self.view.get_selected_id() or 0

        query = self.view.led_search.text()
        self.load_institutionfacilities(query)

        if target_id > 0:
            self.view.select_row_by_id(target_id)

    def load_institutionfacilities(self, query: str = "") -> None:
        """
        Load load_institutionfacilities from service
        and populate the table view.

        Parameters
        ----------
        query : str, optional
            Search term to filter institutionfacilities
            (default is empty string).
        """
        institutionfacilities = self.service.search_institutionfacilities(
            query
        )
        self.view.populate_table(institutionfacilities)
        self.view.clear_details()

    def filter_institutionfacilities(self, text: str) -> None:
        """Filter institutionfacility list based on search input text."""
        self.load_institutionfacilities(text.strip())

    def on_table_selection(self) -> None:
        """Update details pane when a institutionfacility
        is selected in the table."""
        institutionfacility_id = self.view.get_selected_id()
        if institutionfacility_id:
            institutionfacility = self.service.find_by_id(
                institutionfacility_id
            )

            if institutionfacility:
                self.view.display_details(institutionfacility)
        else:
            self.view.clear_details()

    def create_institutionfacility(self) -> None:
        """Open dialog to create a new institutionfacility
        and save if accepted."""
        dialog: "InstitutionFacilityEditView" = self.factory(self.view, None)
        if dialog.exec():
            data = dialog.controller.get_data()
            if self.service.create_institutionfacility(data):
                self.msg.info(
                    self.tr(
                        "Instituição/Estabelecimento cadastrada com sucesso!"
                    )
                )
            else:
                self.msg.critical(
                    self.tr("Erro ao salvar instuição/estabelecimento.")
                )

    def update_institutionfacility(self) -> None:
        """Open dialog to edit the selected institutionfacility
        and update if accepted."""
        institutionfacility_id = self.view.get_selected_id()
        if not institutionfacility_id:
            self.msg.warning(
                self.tr(
                    "Selecione uma instituição/estabelecimento para editar."
                )
            )
            return

        institutionfacility = self.service.find_by_id(institutionfacility_id)
        if not institutionfacility:
            self.msg.critical(
                self.tr("Instituição/Estabelecimento não encontrada.")
            )
            return

        dialog: "InstitutionFacilityEditView" = self.factory(
            self.view, institutionfacility
        )
        if dialog.exec():
            data = dialog.controller.get_data()
            if self.service.update_institutionfacility(
                institutionfacility_id, data
            ):
                self.msg.info(
                    self.tr(
                        "Instituição/Estabelecimento atualizada com sucesso."
                    )
                )
            else:
                self.msg.critical(
                    self.tr("Erro ao atualizar instituição/estabelecimento.")
                )

    def delete_institutionfacility(self) -> None:
        """Delete the selected institutionfacility after user confirmation."""
        institutionfacility_id = self.view.get_selected_id()
        if not institutionfacility_id:
            self.msg.warning(
                self.tr(
                    "Selecione uma instituição/estabelecimento para excluir."
                )
            )
            return

        institutionfacility = self.service.find_by_id(institutionfacility_id)
        if not institutionfacility:
            return

        if self.msg.question(
            self.tr("Deseja excluir?\n{0}").format(institutionfacility.name)
        ):
            try:
                if self.service.delete_institutionfacility(
                    institutionfacility_id
                ):
                    self.view.clear_details()
                    self.msg.info(
                        self.tr(
                            "Instituição/Estabelecimento excluída com sucesso."
                        )
                    )
                else:
                    self.msg.critical(
                        self.tr("Erro ao excluir instituição/estabelecimento.")
                    )
            except BusinessRuleException as e:
                self.msg.warning(str(e))

    def get_institutionfacility_types(self) -> Dict[int, str]:
        return self.service.get_institutionfacility_types()
