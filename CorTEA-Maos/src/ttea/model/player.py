from dataclasses import dataclass, fields
from datetime import datetime
from typing import ClassVar, Dict, List


def initialize_reflexive(cls):
    """Decorator to statically initialize player reflection data.

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
    - Adds the list of field names to `PROPERTIES`.
    - Adds default values of initializable fields to `DATA_PROPERTIES`.
    """
    cls.PROPERTIES = [field.name for field in fields(cls)]
    cls.DATA_PROPERTIES = [
        field.default for field in fields(cls) if field.init
    ]
    return cls


@initialize_reflexive
@dataclass
class Player:
    """Model for player data.

    Attributes
    ----------
    id : int
        Unique identifier for the player.
    name : str
        Name of the player.
    birth_date : datetime
        Player's birth date.
    observation : str, optional
        Additional observations about the player (default is "").
    PROPERTIES : ClassVar[list[str]]
        Static list of the class's field names.
    DATA_PROPERTIES : ClassVar[list]
        Static list of default values for initializable fields.

    Methods
    -------
    is_valid()
        Checks if the player's data is valid.
    set_data(data)
        Updates the player's data from a dictionary.
    get_data()
        Returns the player's data as a list of dictionaries.

    Examples
    --------
    >>> from datetime import datetime
    >>> player = Player(id=1, name="John", birth_date=datetime(2000, 1, 1))
    >>> player.is_valid()
    True
    >>> player.get_data()
    [{'id': 1, 'name': 'John', 'birth_date': datetime(2000, 1, 1),
      'observation': ''}]
    """

    id: int
    name: str
    birth_date: datetime
    observation: str

    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []

    def is_valid(self) -> bool:
        """Checks if the player's data is valid.

        Returns
        -------
        bool
            True if the player's id, name and birth date are provided, False
            otherwise.

        Notes
        -----
        - A player is considered valid if id is not None and int,
          `name` is not an empty string and `birth_date` is not None.
        """
        if self.id is None or not isinstance(self.id, int):
            return False

        if not self.name or not self.name.strip():
            return False

        if self.birth_date is None:
            return False

        strong_fields = {"id", "name", "birth_date"}

        for prop in self.PROPERTIES:
            if prop not in strong_fields:
                value = getattr(self, prop)
                if value is None:
                    return False

        return True

    def set_data(self, data: Dict) -> None:
        """Updates the player's data from a dictionary.

        Parameters
        ----------
        data : Dict
            Dictionary containing player data with keys:
            - 'id': int
            - 'name': str
            - 'birth_date': datetime
            - 'observation': str

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
        """Returns the player's data as a list of dictionaries.

        Returns
        -------
        List[Dict]
            List containing a dictionary with player data:
            - 'id': int
            - 'name': str
            - 'birth_date': datetime
            - 'observation': str

        Notes
        -----
        - Uses PROPERTIES to dynamically build the data dictionary.
        - Returns a list for consistency with potential multi-record returns.
        """
        info = {prop: getattr(self, prop) for prop in self.PROPERTIES}
        return [info]
