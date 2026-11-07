from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, ClassVar, Dict, List

if TYPE_CHECKING:
    from ttea.games.kartea.model.karteaphaselevel import KarteaPhaseLevel


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
class KarteaPhase:
    """Summary model for Kartea game phase data.

    Attributes
    ----------
    id : int
        Unique identifier for the phase.
    level_list : list[KarteaPhaseLevel]
        List of KarteaPhaseLevel objects for the phase.
    PROPERTIES : ClassVar[list[str]]
        Static list of field names of the class.
    DATA_PROPERTIES : ClassVar[list]
        Static list of default values for initializable fields.

    Methods
    -------
    set_data(data)
        Updates phase data from a dictionary.
    get_data()
        Returns phase data as a list of dictionaries.

    Examples
    --------
    >>> from ttea.games.kartea.model.karteaphaselevel import \
    ...     KarteaPhaseLevel
    >>> phase = KarteaPhase(id=1, level_list=[])
    >>> phase.get_data()
    [{'id': 1, 'level_list': []}]
    """

    id: int
    level_list: list["KarteaPhaseLevel"]
    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []

    def set_data(self, data: Dict) -> None:
        """Update phase data from a dictionary.

        Parameters
        ----------
        data : Dict
            Dictionary with phase data. Expected keys:
            - 'id': int
            - 'level_list': list[KarteaPhaseLevel]

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
        """Return phase data as a list of dictionaries.

        Returns
        -------
        List[Dict]
            List with a dictionary containing phase data:
            - 'id': int
            - 'level_list': list[KarteaPhaseLevel]

        Notes
        -----
        - Uses PROPERTIES to dynamically build the data dictionary.
        - Returns a list for consistency with potential multi-record returns.
        """
        info = {prop: getattr(self, prop) for prop in self.PROPERTIES}
        return [info]
