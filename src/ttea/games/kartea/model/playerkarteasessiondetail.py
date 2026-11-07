from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, ClassVar, Dict, List

if TYPE_CHECKING:
    from ttea.games.kartea.model import PlayerKarteaSession


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
class PlayerKarteaSessionDetail:
    """Detailed model for Kartea player session event data.

    Attributes
    ----------
    id : int
        Unique identifier for the session detail.
    session : PlayerKarteaSession
        The session associated with this detail.
    event_time : str
        Time of the event in the game (format TBD).
    phase : int
        Phase number where the event occurred.
    level : int
        Level number where the event occurred.
    player_position : int
        Player's position during the event.
    event_position : int
        Position of the event in the game.
    event_type : str
        Type of the event (e.g., collision, movement).
    PROPERTIES : ClassVar[list[str]]
        Static list of the class's field names.
    DATA_PROPERTIES : ClassVar[list]
        Static list of default values for initializable fields.

    Methods
    -------
    set_data(data)
        Updates session detail data from a dictionary.
    get_data()
        Returns session detail data as a list of dictionaries.

    Examples
    --------
    >>> from ttea.games.kartea.model import PlayerKarteaSession
    >>> from ttea.model.player import Player
    >>> from datetime import datetime
    >>> session = PlayerKarteaSession(id=1, player=Player(id=1, name="John",
    ...                                                  birth_date=datetime(2000, 1, 1)),
    ...                               date="17-09-2025", start_time="10:00:00",
    ...                               end_time="10:30:00", phase_reached=2,
    ...                               level_reached=3, general_score=100,
    ...                               q_movement=50, q_collided_target=10,
    ...                               q_avoided_target=20,
    ...                               q_collided_obstacle=5,
    ...                               q_avoided_obstacle=15)
    >>> detail = PlayerKarteaSessionDetail(id=1, session=session,
    ...                                    event_time="10:05:00", phase=2,
    ...                                    level=3, player_position=100,
    ...                                    event_position=150,
    ...                                    event_type="collision")
    >>> detail.get_data()
    [{'id': 1, 'session': 1, 'event_time': '10:05:00', 'phase': 2,
      'level': 3, 'player_position': 100, 'event_position': 150,
      'event_type': 'collision'}]
    """

    id: int
    session: "PlayerKarteaSession"
    event_time: str
    phase: int
    level: int
    player_position: int
    event_position: int
    event_type: str
    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []

    def set_data(self, data: Dict) -> None:
        """Update session detail data from a dictionary.

        Parameters
        ----------
        data : Dict
            Dictionary with session detail data. Expected keys:
            - 'id': int
            - 'session': PlayerKarteaSession
            - 'event_time': str
            - 'phase': int
            - 'level': int
            - 'player_position': int
            - 'event_position': int
            - 'event_type': str

        Returns
        -------
        None

        Notes
        -----
        - Updates attributes using PROPERTIES for dynamic assignment.
        - For 'session', expects a full PlayerKarteaSession object.
        - No validation is performed on the input data.
        """
        for prop in self.PROPERTIES:
            if prop in data:
                setattr(self, prop, data[prop])

    def get_data(self) -> List[Dict]:
        """Return session detail data as a list of dictionaries.

        Returns
        -------
        List[Dict]
            List with a dictionary containing session detail data:
            - 'id': int
            - 'session': int (or None, extracted from session.id)
            - 'event_time': str
            - 'phase': int
            - 'level': int
            - 'player_position': int
            - 'event_position': int
            - 'event_type': str

        Notes
        -----
        - Uses PROPERTIES to dynamically build the data dictionary.
        - Extracts 'session' as the session's ID for serialization.
        - Returns a list for consistency with potential multi-record returns.
        """
        info = {
            prop: getattr(self, prop)
            for prop in self.PROPERTIES
            if prop != "session"
        }
        info["session"] = self.session.id if self.session else None
        return [info]
