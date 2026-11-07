from typing import Any, Dict, List, Optional, Union

from ttea.games.kartea.dao import PlayerKarteaConfigCsvDAO
from ttea.games.kartea.model import (KarteaPhase, KarteaPhaseLevel,
                                     PlayerKarteaConfig, PlayerKarteaSession)
from ttea.games.kartea.util import KarteaPathConfig
from ttea.model import Player
from ttea.service import PlayerService


class PlayerKarteaConfigService:
    """
    Service layer (MVCS) handling all business rules related to config.

    Attributes
    ----------
    dao : PlayerKarteaConfigCsvDAO
        Data access object responsible for persistence operations.
        Defaults to a new ``PlayerKarteaConfigCsvDAO``
        instance if not provided.

    Methods
    -------
    __init__(dao=None)
        Initializes the service with a DAO instance.
    get_all_configs()
        Returns all registered configs.
    create_config(data)
        Creates a new config from the provided data dictionary.
    update_config(self, player_id: int, data: Dict[str, Any])
        Updates an existing config with the given data.
    delete_config(player_id)
        Deletes a config by its ID.
    find_by_player_id(player_id)
        Retrieves a config by its ID.
    search_configs(query="")
        Searches configs by name or ID (case-insensitive).
    def get_phase(self, phase_id: int) -> Optional[KarteaPhase]
        Searches phase with phase id
    """

    def __init__(
        self,
        dao: Optional[PlayerKarteaConfigCsvDAO] = None,
        player_service: Optional[PlayerService] = None,
    ):
        """
        Initialize the service with a data access object.

        Parameters
        ----------
        dao : PlayerKarteaConfigCsvDAO, optional
            Instance used for persistence. If ``None``, a default
            ``PlayerKarteaConfigCsvDAO`` is created.
        """
        self.dao = dao or PlayerKarteaConfigCsvDAO()
        self.player_service = player_service or PlayerService()

    def get_all_configs(self) -> List[PlayerKarteaConfig]:
        """Return a list of all registered configs.

        Returns
        -------
        List[PlayerKarteaConfig]
            Complete list of ``Config`` instances stored in the DAO.
        """
        return self.dao.list()

    def create_config(
        self, data: Dict[str, Any]
    ) -> Optional[PlayerKarteaConfig]:
        """
        Create a new config from a dictionary of attributes.

        Parameters
        ----------
        data : dict
            Must contain the keys of model.

        Returns
        -------
        PlayerKarteaConfig or None
            The created ``Config`` instance if validation and insertion
            succeed; ``None`` otherwise.
        """
        # Resolve references (e.g., fetch Player, Phase, Level from DAO)
        player = self.dao.player_dao.select(data.get("player_id"))
        session = self.dao.session_dao.select(data.get("session_id"))
        phase = self.dao.phase_dao.select(data.get("phase_id"))
        level = self.dao.level_dao.select(
            data.get("phase_id"), data.get("level_id")
        )

        config = PlayerKarteaConfig(
            player=player,
            session=session,
            update_session_id=data.get(
                "update_session_id", PlayerKarteaConfig.UPDATE_SESSION_ID_YES
            ),
            phase=phase,
            level=level,
            level_time=data.get("level_time", 0),
            car_image=data.get("car_image", ""),
            environment_image=data.get("environment_image", ""),
            target_image=data.get("target_image", ""),
            obstacle_image=data.get("obstacle_image", ""),
            positive_feedback_image=data.get("positive_feedback_image", ""),
            neutral_feedback_image=data.get("neutral_feedback_image", ""),
            negative_feedback_image=data.get("negative_feedback_image", ""),
            positive_feedback_sound=data.get("positive_feedback_sound", ""),
            neutral_feedback_sound=data.get("neutral_feedback_sound", ""),
            negative_feedback_sound=data.get("negative_feedback_sound", ""),
            palette=data.get("palette", 0),
            hud=data.get("hud", False),
            sound=data.get("sound", False),
        )

        if not config.is_valid():
            return None

        player_id = self.dao.insert(config)
        return self.dao.select(player_id) if player_id else None

    def update_config(self, player_id: int, data: Dict[str, Any]) -> bool:
        """
        Update an existing config.
        """
        config = self.dao.select(player_id)
        if not config:
            return False

        # Resolve references (e.g., fetch Player, Phase, Level from DAO)
        player = self.dao.player_dao.select(
            data.get("player_id", config.player.id)
        )
        session = self.dao.session_dao.select(
            data.get(
                "session_id", config.session.id if config.session else None
            )
        )
        phase = self.dao.phase_dao.select(
            data.get("phase_id", config.phase.id)
        )
        level = self.dao.level_dao.select(
            data.get("phase_id", config.phase.id),
            data.get("level_id", config.level.id),
        )

        config.player = player
        config.session = session
        config.update_session_id = data.get(
            "update_session_id", PlayerKarteaConfig.UPDATE_SESSION_ID_YES
        )
        config.phase = phase
        config.level = level

        config.level_time = data.get("level_time", config.level_time)
        config.car_image = data.get("car_image", config.car_image)
        config.environment_image = data.get(
            "environment_image", config.environment_image
        )
        config.target_image = data.get("target_image", config.target_image)
        config.obstacle_image = data.get(
            "obstacle_image", config.obstacle_image
        )
        config.positive_feedback_image = data.get(
            "positive_feedback_image", config.positive_feedback_image
        )
        config.neutral_feedback_image = data.get(
            "neutral_feedback_image", config.neutral_feedback_image
        )
        config.negative_feedback_image = data.get(
            "negative_feedback_image", config.negative_feedback_image
        )
        config.positive_feedback_sound = data.get(
            "positive_feedback_sound", config.positive_feedback_sound
        )
        config.neutral_feedback_sound = data.get(
            "neutral_feedback_sound", config.neutral_feedback_sound
        )
        config.negative_feedback_sound = data.get(
            "negative_feedback_sound", config.negative_feedback_sound
        )
        config.palette = data.get("palette", config.palette)
        config.hud = data.get("hud", config.hud)
        config.sound = data.get("sound", config.sound)

        if not config.is_valid():
            return False

        return self.dao.update(config)

    def delete_config(self, player_id: int) -> bool:
        """Delete a config by player ID."""
        return self.dao.delete(player_id)

    def find_config_by_player_id(
        self, player_id: int
    ) -> Optional[PlayerKarteaConfig]:
        """Find config by player ID."""
        return self.dao.select(player_id)

    def search_configs(self, query: str = "") -> List[PlayerKarteaConfig]:
        """
        Search configs by player name or ID.
        """
        all_configs = self.get_all_configs()
        if not query.strip():
            return all_configs

        q = query.lower().strip()
        return [
            c
            for c in all_configs
            if q in str(c.player.id)
            or (c.player and q in c.player.name.lower())
        ]

    def get_all_players(self) -> List[Player]:
        return sorted(
            self.player_service.get_all_players(),
            key=lambda p: p.name,
        )

    def get_session(self, session_id: int) -> Optional[PlayerKarteaSession]:
        return self.dao.session_dao.select(session_id)

    def get_phase(self, phase_id: int) -> Optional[KarteaPhase]:
        return self.dao.get_phase(phase_id)

    def get_all_phases(self) -> List[KarteaPhase]:
        return self.dao.get_all_phases()

    def get_level_by_ids(
        self, phase_id: int, level_id: int
    ) -> Optional[KarteaPhaseLevel]:
        return self.dao.level_dao.select(phase_id, level_id)

    def get_levels_for_phase(
        self, phase: Union[int, KarteaPhase]
    ) -> List[KarteaPhaseLevel]:
        return self.dao.get_levels_for_phase(phase)

    def get_kartea_ini_config(self) -> Dict[str, str]:
        return KarteaPathConfig.read_config()
