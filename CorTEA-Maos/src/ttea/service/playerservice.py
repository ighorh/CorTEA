# /service/player_service.py
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QObject, Signal

from ttea.dao import PlayerCsvDAO
from ttea.exception import BusinessRuleException
from ttea.model import Player


class PlayerService(QObject):
    """
    Service layer (MVCS) handling all business rules related to players.

    Attributes
    ----------
    dao : PlayerCsvDAO
        Data access object responsible for persistence operations.
        Defaults to a new ``PlayerCsvDAO`` instance if not provided.

    Methods
    -------
    __init__(dao=None)
        Initializes the service with a DAO instance.
    get_all_players()
        Returns all registered players.
    create_player(data)
        Creates a new player from the provided data dictionary.
    update_player(player_id, data)
        Updates an existing player with the given data.
    delete_player(player_id)
        Deletes a player by its ID.
    find_by_id(player_id)
        Retrieves a player by its ID.
    search_players(query="")
        Searches players by name or ID (case-insensitive).
    """

    _instance = None
    # Sinal que avisa: "Os dados do jagador mudaram"
    player_change = Signal(int)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dao: Optional[PlayerCsvDAO] = None):
        """
        Initialize the service with a data access object.

        Parameters
        ----------
        dao : PlayerCsvDAO, optional
            Instance used for persistence. If ``None``, a default
            ``PlayerCsvDAO`` is created.
        """
        if not hasattr(self, "_initialized"):
            super().__init__()
            self.dao = dao or PlayerCsvDAO()
            self._initialized = True

    def get_all_players(self) -> List[Player]:
        """Return a list of all registered players.

        Returns
        -------
        List[Player]
            Complete list of ``Player`` instances stored in the DAO.
        """
        return self.dao.list()

    def validate_data(self, data: Dict[str, Any]) -> List[str]:
        """
        Valida as regras de negócio para os dados de um jogador.
        Retorna uma lista de mensagens de erro (vazia se estiver tudo ok).
        """
        errors = []
        if data.get("id") is None:
            errors.append(self.tr("ID é obrigatório!\n"))
        elif not isinstance(data.get("id"), int):
            errors.append(self.tr("ID deve ser do tipo inteiro!\n"))

        if not data.get("name") or not data.get("name").strip():
            errors.append(self.tr("Nome é obrigatório!\n"))

        if not data.get("birth_date"):
            errors.append(self.tr("Data de nascimento é obrigatória!\n"))

        return errors

    def create_player(self, data: Dict[str, Any]) -> Optional[Player]:
        """
        Create a new player from a dictionary of attributes.

        Parameters
        ----------
        data : dict
            Must contain the key ``id`` (int),  ``name`` (str),
            ``birth_date`` (date) and optionally ``observation`` (str).

        Returns
        -------
        Player or None
            The created ``Player`` instance if validation and insertion
            succeed; ``None`` otherwise.
        """
        player = Player(**data)

        if not player.is_valid():
            return None

        new_id = self.dao.insert(player)
        if new_id:
            self.player_change.emit(new_id)  # Notifica observadores
        return self.dao.select(new_id) if new_id > 0 else None

    def update_player(self, player_id: int, data: Dict[str, Any]) -> bool:
        """
        Update an existing player with new values.

        Parameters
        ----------
        player_id : int
            Identifier of the player to update.
        data : dict
            Dictionary containing updated fields (``name``,
            ``birth_date``, ``observation``). Missing keys keep the
            current value.

        Returns
        -------
        bool
            ``True`` if the player was found, validated, and updated
            successfully; ``False`` otherwise.
        """
        player = self.dao.select(player_id)
        if not player:
            return False

        player.set_data(data)

        if not player.is_valid():
            return False

        success = self.dao.update(player)

        if success:
            self.player_change.emit(player_id)

        return success

    def delete_player(self, player_id: int) -> bool:
        """Delete a player by its identifier.

        Parameters
        ----------
        player_id : int
            Identifier of the player to be removed.

        Returns
        -------
        bool
            ``True`` if the player was successfully deleted,
            ``False`` otherwise (e.g., player not found).
        """
        from ttea.games.kartea.service import PlayerKarteaConfigService

        # Validação de integridade referencial (Negócio)
        karteaconfig = PlayerKarteaConfigService()
        if karteaconfig.find_config_by_player_id(player_id):
            raise BusinessRuleException(
                self.tr(
                    "Exclusão negada: O jogador possui uma configuração do KarTEA ativa."
                )
            )

        success = self.dao.delete(player_id)

        if success:
            self.player_change.emit(0)

        return success

    def find_by_id(self, player_id: int) -> Optional[Player]:
        """Retrieve a player by its unique identifier.

        Parameters
        ----------
        player_id : int
            The player's ID.

        Returns
        -------
        Player or None
            The matching ``Player`` instance or ``None`` if not found.
        """
        return self.dao.select(player_id)

    def search_players(self, query: str = "") -> List[Player]:
        """
        Search players by name or ID (case-insensitive).

        Parameters
        ----------
        query : str, optional
            Search term. If empty or whitespace-only, returns all
            players.

        Returns
        -------
        List[Player]
            List of players whose ID (as string) or name contain the
            query term.
        """
        return self.dao.search_players(query)
