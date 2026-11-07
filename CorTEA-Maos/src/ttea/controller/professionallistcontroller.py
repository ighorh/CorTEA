from typing import TYPE_CHECKING, Callable, Dict

from PySide6.QtCore import QObject

# Local module import
from ttea.service import ProfessionalService
from ttea.util import MessageService

if TYPE_CHECKING:
    from ttea.view import ProfessionalEditView, ProfessionalListView


class ProfessionalListController(QObject):
    """
    Lightweight controller that orchestrates InstitutionFacilityListView
    and InstitutionFacilityService.

    Follows MVCS pattern: mediates between view and service layer,
    handling user interactions and updating the UI accordingly.

    Attributes
    ----------
    view : InstitutionFacilityListView
        Main view displaying the list and details of professionals.
    factory : Callable
        Factory function that creates a ``InstitutionFacilityEditView`` dialog,
        receiving the parent view and an optional professional to edit.
    service : InstitutionFacilityService
        Business logic layer for professional CRUD operations.
    msg : MessageService
        Helper for showing info, warning, and error messages.

    Methods
    -------
    __init__(view, professional_edit_view_factory)
        Initializes the controller with view and edit dialog factory.
    load_professionals(query="")
        Loads and displays professionals, optionally filtered
        by search term.
    filter_professionals(text)
        Filters the professional list based on the search input text.
    on_table_selection()
        Updates details panel when a table row is selected.
    select_and_show_professional(professional_id)
        Selects a professional row and shows its details.
    handle_new_professional()
        Opens dialog to create a new professional.
    handle_edit_professional()
        Opens dialog to edit the selected professional.
    delete_professional()
        Deletes the selected professional after confirmation.
    """

    def __init__(
        self, view: "ProfessionalListView", factory: Callable
    ) -> None:
        """
        Initialize the controller.

        Parameters
        ----------
        view : ProfessionalListView
            The main list view instance to control.
        professional_edit_view_factory : Callable
            Function that returns a ``ProfessionalEditView`` dialog.
            Signature: (parent_view, professional)
            -> ProfessionalEditView.
        """
        self.view = view
        self.factory = factory
        self.service = ProfessionalService()
        self.msg = MessageService(self.view)

        # ------------------------------------------------------------------
        # OBSERVER PATTERN: Conexão reativa
        # ------------------------------------------------------------------
        # Sempre que o serviço emitir que os dados mudaram, a lista recarrega.
        self.service.professional_change.connect(self.reload_data)

        # Events signals and slots
        self.view.pb_new.clicked.connect(self.create_professional)
        self.view.pb_edit.clicked.connect(self.update_professional)
        self.view.pb_delete.clicked.connect(self.delete_professional)
        self.view.led_search.textChanged.connect(self.filter_professionals)
        self.view.tbl_professional.selectionModel().selectionChanged.connect(
            self.on_table_selection
        )

        # Carga inicial
        self.load_professionals()

    def reload_data(self, target_id: int = 0) -> None:
        """
        Slot que reage ao sinal do Service.
        Mantém o filtro atual ao recarregar.
        """
        if target_id == 0:
            target_id = self.view.get_selected_id() or 0

        query = self.view.led_search.text()
        self.load_professionals(query)

        if target_id > 0:
            self.view.select_row_by_id(target_id)

    def load_professionals(self, query: str = "") -> None:
        """
        Load load_professionals from service
        and populate the table view.

        Parameters
        ----------
        query : str, optional
            Search term to filter professionals
            (default is empty string).
        """
        load_professionals = self.service.search_professionals(query)
        self.view.populate_table(load_professionals)
        self.view.clear_details()

    def filter_professionals(self, text: str) -> None:
        """Filter professional list based on search input text."""
        self.load_professionals(text.strip())

    def on_table_selection(self) -> None:
        """Update details pane when a professional
        is selected in the table."""
        professional_id = self.view.get_selected_id()
        if professional_id:
            professional = self.service.find_by_id(professional_id)

            if professional:
                self.view.display_details(professional)
        else:
            self.view.clear_details()

    def create_professional(self) -> None:
        """Open dialog to create a new professional
        and save if accepted."""
        dialog: "ProfessionalEditView" = self.factory(self.view, None)
        if dialog.exec():
            data = dialog.controller.get_data()
            if self.service.create_professional(data):
                self.msg.info(self.tr("Profissional cadastrado com sucesso!"))
            else:
                self.msg.critical(self.tr("Erro ao salvar profissional."))

    def update_professional(self) -> None:
        """Open dialog to edit the selected professional
        and update if accepted."""
        professional_id = self.view.get_selected_id()
        if not professional_id:
            self.msg.warning(self.tr("Selecione um professional para editar."))
            return

        professional = self.service.find_by_id(professional_id)
        if not professional:
            self.msg.critical(self.tr("Profissional não encontrado."))
            return

        dialog: "ProfessionalEditView" = self.factory(self.view, professional)
        if dialog.exec():
            data = dialog.controller.get_data()
            if self.service.update_professional(professional_id, data):
                self.msg.info(self.tr("Profissional atualizado com sucesso."))
            else:
                self.msg.critical(self.tr("Erro ao atualizar profissional."))

    def delete_professional(self) -> None:
        """Delete the selected professional after user confirmation."""

        professional_id = self.view.get_selected_id()
        if not professional_id:
            self.msg.warning(
                self.tr("Selecione um profissional para excluir.")
            )
            return

        professional = self.service.find_by_id(professional_id)
        if not professional:
            return

        if self.msg.question(
            self.tr("Deseja excluir?\n{0}").format(professional.name)
        ):
            if self.service.delete_professional(professional_id):
                self.view.clear_details()
                self.msg.info(self.tr("Profissional excluído com sucesso."))
            else:
                self.msg.critical(self.tr("Erro ao excluir profissional."))

    def get_professional_types(self) -> Dict[int, str]:
        return self.service.get_professional_types()
