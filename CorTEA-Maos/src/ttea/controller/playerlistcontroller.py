from typing import TYPE_CHECKING, Callable

from PySide6.QtCore import QObject

# Local module import
from ttea.exception import BusinessRuleException
from ttea.service import PlayerService
from ttea.util import MessageService

if TYPE_CHECKING:
    from ttea.view import PlayerEditView, PlayerListView


class PlayerListController(QObject):
    """
    Controller que orquestra a PlayerListView usando o Observer Pattern.

    Agora, este controller reage automaticamente a mudanças no Service.
    """

    def __init__(self, view: "PlayerListView", factory: Callable):
        self.view = view
        self.factory = factory
        self.service = PlayerService()
        self.msg = MessageService(self.view)

        # ------------------------------------------------------------------
        # OBSERVER PATTERN: Conexão reativa
        # ------------------------------------------------------------------
        # Sempre que o serviço emitir que os dados mudaram, a lista recarrega.
        self.service.player_change.connect(self.reload_data)

        # Events signals and slots
        self.view.pb_new.clicked.connect(self.create_player)
        self.view.pb_edit.clicked.connect(self.update_player)
        self.view.pb_delete.clicked.connect(self.delete_player)
        self.view.led_search.textChanged.connect(self.filter_players)
        self.view.tbl_player.itemSelectionChanged.connect(
            self.on_table_selection
        )

        # Carga inicial
        self.load_players()

    def reload_data(self, target_id: int = 0) -> None:
        """
        Slot que reage ao sinal do Service.
        Mantém o filtro atual ao recarregar.
        """
        if target_id == 0:
            target_id = self.view.get_selected_id() or 0

        query = self.view.led_search.text()
        self.load_players(query)

        if target_id > 0:
            self.view.select_row_by_id(target_id)

    def load_players(self, query: str = "") -> None:
        """Busca os jogadores no serviço e popula a tabela da View."""
        players = self.service.search_players(query)
        self.view.populate_table(players)
        self.view.clear_details()

    def filter_players(self, text: str) -> None:
        """Filtra a lista conforme o usuário digita."""
        self.load_players(text.strip())

    def on_table_selection(self) -> None:
        """Atualiza o painel de detalhes ao selecionar uma linha."""
        player_id = self.view.get_selected_id()
        if player_id:
            player = self.service.find_by_id(player_id)
            if player:
                self.view.display_details(player)
        else:
            self.view.clear_details()

    def create_player(self) -> None:
        """Abre o diálogo de criação."""
        dialog: "PlayerEditView" = self.factory(self.view)
        if dialog.exec():
            data = dialog.controller.get_data()
            if self.service.create_player(data):
                # O Observer (Signal) cuidará do load_players automaticamente
                self.msg.info(self.tr("Jogador cadastrado com sucesso!"))
            else:
                self.msg.critical(self.tr("Erro ao salvar jogador."))

    def update_player(self) -> None:
        """Abre o diálogo de edição para o jogador selecionado."""
        player_id = self.view.get_selected_id()
        if not player_id:
            self.msg.warning(self.tr("Selecione um jogador para editar."))
            return

        player = self.service.find_by_id(player_id)
        if not player:
            self.msg.critical(self.tr("Jogador não encontrado."))
            return

        dialog: "PlayerEditView" = self.factory(self.view, player)
        if dialog.exec():
            data = dialog.controller.get_data()
            if self.service.update_player(player_id, data):
                # O Observer cuidará da atualização da lista
                self.msg.info(self.tr("Jogador atualizado com sucesso."))
            else:
                self.msg.critical(self.tr("Erro ao atualizar jogador."))

    def delete_player(self) -> None:
        """Exclui o jogador selecionado após confirmação."""
        player_id = self.view.get_selected_id()
        if not player_id:
            self.msg.warning(self.tr("Selecione um jogador para excluir."))
            return

        player = self.service.find_by_id(player_id)
        if not player:
            return

        if self.msg.question(
            self.tr("Deseja excluir?\n{0}").format(player.name)
        ):
            try:
                if self.service.delete_player(player_id):
                    self.view.clear_details()
                    self.msg.info(self.tr("Jogador excluído com sucesso."))
                else:
                    self.msg.critical(self.tr("Erro ao excluir jogador."))
            except BusinessRuleException as e:
                self.msg.warning(str(e))
