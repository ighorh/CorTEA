from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, ClassVar, Dict, List

# Type checking to prevent circular import on run time
if TYPE_CHECKING:
    from ttea.games.kartea.model import (KarteaPhase, KarteaPhaseLevel,
                                         PlayerKarteaSession)
    from ttea.model import Player


def initialize_reflexive(cls):
    """Decorator to initialize class reflection data statically.

    Parameters
    ----------
    cls : type
        The class to be decorated.

    Returns
    -------
    type
        The decorated class with initialized PROPERTIES and DATA_PROPERTIES.

    Notes
    -----
    - Adds field names to `PROPERTIES`.
    - Adds default values of initializable fields to `DATA_PROPERTIES`.
    """
    cls.PROPERTIES = [field.name for field in fields(cls)]
    cls.DATA_PROPERTIES = [
        field.default for field in fields(cls) if field.init
    ]
    return cls


@initialize_reflexive
@dataclass
class PlayerKarteaConfig:
    """Model for player configuration in the Kartea game.

    Attributes
    ----------
    player : Player
        The player associated with this configuration.
    session : PlayerKarteaSession
        The session associated with this configuration.
    phase : KarteaPhase
        The game phase for this configuration.
    level : KarteaPhaseLevel
        The level within the phase for this configuration.
    level_time : int
        Time allocated for the level (in seconds).
    car_image : str
        Path or identifier for the car image.
    environment_image : str
        Path or identifier for the environment image.
    target_image : str
        Path or identifier for the target image.
    obstacle_image : str
        Path or identifier for the obstacle image.
    positive_feedback_image : str
        Path or identifier for the positive feedback image.
    neutral_feedback_image : str
        Path or identifier for the neutral feedback image.
    negative_feedback_image : str
        Path or identifier for the negative feedback image.
    positive_feedback_sound : str
        Path or identifier for the positive feedback sound.
    neutral_feedback_sound : str
        Path or identifier for the neutral feedback sound.
    negative_feedback_sound : str
        Path or identifier for the negative feedback sound.
    palette : int
        Identifier for the color palette used in the interface.
    hud : bool
        Whether the heads-up display (HUD) is enabled.
    sound : bool
        Whether sound effects are enabled.
    PROPERTIES : ClassVar[list[str]]
        Static list of the class's field names.
    DATA_PROPERTIES : ClassVar[list]
        Static list of default values for initializable fields.

    Methods
    -------
    set_data(data)
        Updates configuration data from a dictionary.
    get_data()
        Returns configuration data as a list of dictionaries.

    Examples
    --------
    >>> from datetime import datetime
    >>> from ttea.model import Player
    >>> from ttea.games.kartea.model import (KarteaPhase,
    ...                                                  KarteaPhaseLevel,
    ...                                                  PlayerKarteaSession)
    >>> config = PlayerKarteaConfig(player=Player(id=1, name="John",
    ...                                          birth_date=datetime(2000, 1, 1)),
    ...                             session=PlayerKarteaSession(id=1,
    ...                                                         player=Player(id=1,
    ...                                                         name="John",
    ...                                                         birth_date=datetime(2000, 1, 1)),
    ...                                                         date="17-09-2025",
    ...                                                         start_time="10:00:00",
    ...                                                         end_time="10:30:00",
    ...                                                         phase_reached=2,
    ...                                                         level_reached=3,
    ...                                                         general_score=100,
    ...                                                         q_movement=50,
    ...                                                         q_collided_target=10,
    ...                                                         q_avoided_target=20,
    ...                                                         q_collided_obstacle=5,
    ...                                                         q_avoided_obstacle=15),
    ...                             phase=KarteaPhase(id=1, level_list=[]),
    ...                             level=KarteaPhaseLevel(id=1,
    ...                                                    phase=KarteaPhase(id=1,
    ...                                                                level_list=[]),
    ...                                                    interval=1.5, num_obj=10,
    ...                                                    obj_type=[1, 2, 3]),
    ...                             level_time=60, car_image="car.png",
    ...                             environment_image="env.png",
    ...                             target_image="target.png",
    ...                             obstacle_image="obstacle.png",
    ...                             positive_feedback_image="positive.png",
    ...                             neutral_feedback_image="neutral.png",
    ...                             negative_feedback_image="negative.png",
    ...                             positive_feedback_sound="positive.wav",
    ...                             neutral_feedback_sound="neutral.wav",
    ...                             negative_feedback_sound="negative.wav",
    ...                             palette=1, hud=True, sound=True)
    >>> config.get_data()
    [{'player': 1, 'session': 1, 'phase': 1, 'level': 1, 'level_time': 60,
      'car_image': 'car.png', 'environment_image': 'env.png',
      'target_image': 'target.png', 'obstacle_image': 'obstacle.png',
      'positive_feedback_image': 'positive.png',
      'neutral_feedback_image': 'neutral.png',
      'negative_feedback_image': 'negative.png',
      'positive_feedback_sound': 'positive.wav',
      'neutral_feedback_sound': 'neutral.wav',
      'negative_feedback_sound': 'negative.wav', 'palette': 1, 'hud': True,
      'sound': True}]
    """

    player: "Player"
    session: "PlayerKarteaSession"
    update_session_id: bool
    phase: "KarteaPhase"
    level: "KarteaPhaseLevel"
    level_time: int
    car_image: str
    environment_image: str
    target_image: str
    obstacle_image: str
    positive_feedback_image: str
    neutral_feedback_image: str
    negative_feedback_image: str
    positive_feedback_sound: str
    neutral_feedback_sound: str
    negative_feedback_sound: str
    palette: int
    hud: bool
    sound: bool
    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []
    UPDATE_SESSION_ID_NO = False
    UPDATE_SESSION_ID_YES = True

    def is_valid(self) -> bool:
        """Checks if the configs's data is valid.

        Returns
        -------
        bool
            True if the data are provided, False otherwise.

        Notes
        -----
        - A player is considered valid if `player`, `phase` and `level`
        is not None.
        """
        return bool(self.player and self.phase and self.level)

    def set_data(self, data: Dict) -> None:
        """Update configuration data from a dictionary.

        Parameters
        ----------
        data : Dict
            Dictionary with configuration data. Expected keys:
            - 'player': Player
            - 'session': PlayerKarteaSession
            - 'phase': KarteaPhase
            - 'level': KarteaPhaseLevel
            - 'level_time': int
            - 'car_image': str
            - 'environment_image': str
            - 'target_image': str
            - 'obstacle_image': str
            - 'positive_feedback_image': str
            - 'neutral_feedback_image': str
            - 'negative_feedback_image': str
            - 'positive_feedback_sound': str
            - 'neutral_feedback_sound': str
            - 'negative_feedback_sound': str
            - 'palette': int
            - 'hud': bool
            - 'sound': bool

        Returns
        -------
        None

        Notes
        -----
        - Updates attributes using PROPERTIES for dynamic assignment.
        - No validation is performed on the input data.
        """
        for prop in self.PROPERTIES:
            if prop in data:
                setattr(self, prop, data[prop])

    def get_data(self) -> List[Dict]:
        """Return configuration data as a list of dictionaries.

        Returns
        -------
        List[Dict]
            List with a dictionary containing configuration data:
            - 'player': int (or None, extracted from player.id)
            - 'session': int (or None, extracted from session.id)
            - 'phase': int (or None, extracted from phase.id)
            - 'level': int (or None, extracted from level.id)
            - 'level_time': int
            - 'car_image': str
            - 'environment_image': str
            - 'target_image': str
            - 'obstacle_image': str
            - 'positive_feedback_image': str
            - 'neutral_feedback_image': str
            - 'negative_feedback_image': str
            - 'positive_feedback_sound': str
            - 'neutral_feedback_sound': str
            - 'negative_feedback_sound': str
            - 'palette': int
            - 'hud': bool
            - 'sound': bool

        Notes
        -----
        - Uses PROPERTIES to dynamically build the data dictionary.
        - Extracts IDs for 'player', 'session', 'phase', and 'level' for serialization.
        - Returns a list for consistency with potential multi-record returns.
        """
        info = {
            prop: getattr(self, prop)
            for prop in self.PROPERTIES
            if prop not in ["player", "session", "phase", "level"]
        }
        info["player"] = self.player.id if self.player else None
        info["session"] = self.session.id if self.session else None
        info["phase"] = self.phase.id if self.phase else None
        info["level"] = self.level.id if self.level else None
        return [info]
