from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, ClassVar, Dict, List

if TYPE_CHECKING:
    from ttea.games.kartea.model.karteaphase import KarteaPhase


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
class KarteaPhaseLevel:
    """Summary model for Kartea game phase level data.

    Attributes
    ----------
    id : int
        Unique identifier for the level.
    phase : KarteaPhase
        The phase associated with this level.
    interval : float
        Time interval between objects (in seconds).
    num_obj : int
        Number of objects in the level.
    obj_type : List[int]
        List of object types (parsed from space-separated string).
    PROPERTIES : ClassVar[list[str]]
        Static list of the class's field names.
    DATA_PROPERTIES : ClassVar[list]
        Static list of default values for initializable fields.

    Methods
    -------
    set_data(data)
        Updates level data from a dictionary.
    get_data()
        Returns level data as a list of dictionaries.

    Examples
    --------
    >>> from ttea.games.kartea.model.karteaphase import KarteaPhase
    >>> phase = KarteaPhase(id=1, level_list=[])
    >>> level = KarteaPhaseLevel(id=1, phase=phase, interval=1.5, num_obj=10,
    ...                          obj_type=[1, 2, 3])
    >>> level.get_data()
    [{'id': 1, 'phase': 1, 'interval': 1.5, 'num_obj': 10,
      'obj_type': [1, 2, 3]}]
    """

    id: int
    phase: "KarteaPhase"
    interval: float
    num_obj: int
    obj_type: List[int]
    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []

    def set_data(self, data: Dict) -> None:
        """Update level data from a dictionary.

        Parameters
        ----------
        data : Dict
            Dictionary with level data. Expected keys:
            - 'id': int
            - 'phase': KarteaPhase
            - 'interval': float
            - 'num_obj': int
            - 'obj_type': List[int]

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
        """Return level data as a list of dictionaries.

        Returns
        -------
        List[Dict]
            List with a dictionary containing level data:
            - 'id': int
            - 'phase': int (or None, extracted from phase.id)
            - 'interval': float
            - 'num_obj': int
            - 'obj_type': List[int]

        Notes
        -----
        - Uses PROPERTIES to dynamically build the data dictionary.
        - Extracts 'phase' as the phase's ID for serialization.
        - Returns a list for consistency with potential multi-record returns.
        """
        info = {
            prop: getattr(self, prop)
            for prop in self.PROPERTIES
            if prop != "phase"
        }
        info["phase"] = self.phase.id if self.phase else None
        return [info]
