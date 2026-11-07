from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, ClassVar, Dict, List

# Type checking to prevent circular import on run time
if TYPE_CHECKING:
    from ttea.model.player import Player


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
class PlayerKarteaSession:
    """Summary model for Kartea player session data.

    Attributes
    ----------
    id : int
        Unique identifier for the session.
    player : Player
        The player associated with this session.
    date : str
        Session date in format "%d-%m-%Y".
    start_time : str
        Session start time in format "%H:%M:%S".
    end_time : str
        Session end time in format "%H:%M:%S".
    phase_reached : int
        Highest phase reached in the session.
    level_reached : int
        Highest level reached in the session.
    general_score : int
        Overall score achieved in the session.
    q_movement : int
        Number of movement events.
    q_collided_target : int
        Number of target collisions.
    q_avoided_target : int
        Number of avoided targets.
    q_collided_obstacle : int
        Number of obstacle collisions.
    q_avoided_obstacle : int
        Number of avoided obstacles.
    PROPERTIES : ClassVar[list[str]]
        Static list of the class's field names.
    DATA_PROPERTIES : ClassVar[list]
        Static list of default values for initializable fields.

    Methods
    -------
    set_data(data)
        Updates session data from a dictionary.
    get_data()
        Returns session data as a list of dictionaries.

    Examples
    --------
    >>> from datetime import datetime
    >>> from ttea.model.player import Player
    >>> session = PlayerKarteaSession(id=1, player=Player(id=1, name="John",
    ...                                                  birth_date=datetime(2000, 1, 1)),
    ...                               date="17-09-2025", start_time="10:00:00",
    ...                               end_time="10:30:00", phase_reached=2,
    ...                               level_reached=3, general_score=100,
    ...                               q_movement=50, q_collided_target=10,
    ...                               q_avoided_target=20,
    ...                               q_collided_obstacle=5,
    ...                               q_avoided_obstacle=15)
    >>> session.get_data()
    [{'id': 1, 'player': 1, 'date': '17-09-2025', 'start_time': '10:00:00',
      'end_time': '10:30:00', 'phase_reached': 2, 'level_reached': 3,
      'general_score': 100, 'q_movement': 50, 'q_collided_target': 10,
      'q_avoided_target': 20, 'q_collided_obstacle': 5,
      'q_avoided_obstacle': 15}]
    """

    id: int
    player: "Player"
    date: str
    start_time: str
    end_time: str
    phase_reached: int
    level_reached: int
    general_score: int
    q_movement: int
    q_collided_target: int
    q_avoided_target: int
    q_collided_obstacle: int
    q_avoided_obstacle: int
    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []

    def set_data(self, data: Dict) -> None:
        """Update session data from a dictionary.

        Parameters
        ----------
        data : Dict
            Dictionary with session data. Expected keys:
            - 'id': int
            - 'player': Player
            - 'date': str
            - 'start_time': str
            - 'end_time': str
            - 'phase_reached': int
            - 'level_reached': int
            - 'general_score': int
            - 'q_movement': int
            - 'q_collided_target': int
            - 'q_avoided_target': int
            - 'q_collided_obstacle': int
            - 'q_avoided_obstacle': int

        Returns
        -------
        None

        Notes
        -----
        - Updates attributes using PROPERTIES for dynamic assignment.
        - For 'player', expects a full Player object.
        - No validation is performed on the input data.
        """
        for prop in self.PROPERTIES:
            if prop in data:
                setattr(self, prop, data[prop])

    def get_data(self) -> List[Dict]:
        """Return session data as a list of dictionaries.

        Returns
        -------
        List[Dict]
            List with a dictionary containing session data:
            - 'id': int
            - 'player': int (or None, extracted from player.id)
            - 'date': str
            - 'start_time': str
            - 'end_time': str
            - 'phase_reached': int
            - 'level_reached': int
            - 'general_score': int
            - 'q_movement': int
            - 'q_collided_target': int
            - 'q_avoided_target': int
            - 'q_collided_obstacle': int
            - 'q_avoided_obstacle': int

        Notes
        -----
        - Uses PROPERTIES to dynamically build the data dictionary.
        - Extracts 'player' as the player's ID for serialization.
        - Returns a list for consistency with potential multi-record returns.
        """
        info = {
            prop: getattr(self, prop)
            for prop in self.PROPERTIES
            if prop != "player"
        }
        info["player"] = self.player.id if self.player else None
        return [info]
