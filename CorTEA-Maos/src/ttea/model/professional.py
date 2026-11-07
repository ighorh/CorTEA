from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, ClassVar, Dict, List

from PySide6.QtCore import QT_TRANSLATE_NOOP

if TYPE_CHECKING:
    from ttea.model import InstitutionFacility


def initialize_reflexive(cls):
    """
    Initialize class with reflexive properties metadata.

    Populates PROPERTIES with all field names and DATA_PROPERTIES with
    default values of initializable fields.

    Parameters
    ----------
    cls : type
        Class to decorate with reflexive properties.

    Returns
    -------
    type
        The decorated class with PROPERTIES and DATA_PROPERTIES attributes.
    """
    cls.PROPERTIES = [field.name for field in fields(cls)]
    cls.DATA_PROPERTIES = [
        field.default for field in fields(cls) if field.init
    ]
    return cls


@initialize_reflexive
@dataclass
class Professional:
    """
    Professional entity representing a professional.
    A Professional instance encapsulates information about a
    worker, including their identifier, name, professional type,
    and associated institution or facility.

    Attributes
    ----------
    id : int
        Unique identifier for the professional.
    name : str
        Full name of the professional.
    type : int
        Professional type code mapping to TYPE_MAP dictionary.
    institutionfacility : InstitutionFacility
        Reference to the institution or facility where professional works.

    CLASS VARIABLES
    ---------------
    TYPE_MAP : ClassVar[dict[int, str]]
        Mapping of professional type codes to translated type names.
        Used for internationalization via QCoreApplication.
    PROPERTIES : ClassVar[list[str]]
        List of property names for serialization.
    DATA_PROPERTIES : ClassVar[list]
        List of data property definitions.

    Methods
    -------
    is_valid() -> bool
        Validates that all required fields are properly set.
    set_data(data: Dict) -> None
        Sets properties from a dictionary.
    get_data() -> List[Dict]
        Retrieves property data as a list of dictionaries.

    Notes
    -----
    Type codes range from 0-20 representing different professions
    including nurses, psychologists, physiotherapists, and others.
    """

    id: int
    name: str
    type: int
    institutionfacility: "InstitutionFacility"

    # Mapping type with translation support using QT_TRANSLATE_NOOP
    # for deferred translation. The translation will be applied when
    # the type is accessed in the UI, allowing for dynamic language changes.
    TYPE_MAP: ClassVar[dict[int, str]] = {
        0: "",
        1: QT_TRANSLATE_NOOP("Professional", "Arteterapeuta"),
        2: QT_TRANSLATE_NOOP("Professional", "Assistente Social"),
        3: QT_TRANSLATE_NOOP("Professional", "Cuidador Especializado"),
        4: QT_TRANSLATE_NOOP("Professional", "Educador Físico"),
        5: QT_TRANSLATE_NOOP("Professional", "Enfermeiro"),
        6: QT_TRANSLATE_NOOP("Professional", "Fisioterapeuta"),
        7: QT_TRANSLATE_NOOP("Professional", "Fonoaudiólogo"),
        8: QT_TRANSLATE_NOOP("Professional", "Geneticista"),
        9: QT_TRANSLATE_NOOP("Professional", "Mediador Escolar"),
        10: QT_TRANSLATE_NOOP("Professional", "Musicoterapeuta"),
        11: QT_TRANSLATE_NOOP("Professional", "Neuropediatra"),
        12: QT_TRANSLATE_NOOP("Professional", "Neurologista"),
        13: QT_TRANSLATE_NOOP("Professional", "Nutricionista"),
        14: QT_TRANSLATE_NOOP("Professional", "Pediatra"),
        15: QT_TRANSLATE_NOOP("Professional", "Professor Educação Especial"),
        16: QT_TRANSLATE_NOOP("Professional", "Psicopedagogo"),
        17: QT_TRANSLATE_NOOP("Professional", "Psicólogo"),
        18: QT_TRANSLATE_NOOP("Professional", "Psiquiatra"),
        19: QT_TRANSLATE_NOOP("Professional", "Terapeuta Ocupacional"),
        20: QT_TRANSLATE_NOOP("Professional", "Voluntário"),
    }

    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []

    def is_valid(self) -> bool:
        """
        Validate the professional object.

        Checks that id is a valid integer, name is non-empty, type is a valid
        integer mapped in TYPE_MAP, and all non-strong properties are not None.

        Returns
        -------
        bool
            True if the professional object is valid, False otherwise.

        Examples
        --------
        >>> hp = Professional(id=1, name="Dr. Smith",
        ...     type=5, institutionfacility=None)
        >>> hp.is_valid()
        True

        >>> hp_invalid = Professional(id=None, name="",
        ...     type=99, institutionfacility=None)
        >>> hp_invalid.is_valid()
        False
        """

        if self.id is None or not isinstance(self.id, int):
            return False

        if not self.name or not self.name.strip():
            return False

        if not isinstance(self.type, int) or self.type not in self.TYPE_MAP:
            return False

        strong_fields = {"id", "name", "type"}

        for prop in self.PROPERTIES:
            if prop not in strong_fields:
                value = getattr(self, prop)
                if value is None:
                    return False

        return True

    def set_data(self, data: Dict) -> None:
        """
        Set object attributes from a dictionary.
        Iterates through defined properties and assigns corresponding
        values from the input dictionary to the object instance.

        Parameters
        ----------
        data : Dict
            Dictionary containing property names as keys and their
            respective values to be assigned to the object.
        """
        for prop in self.PROPERTIES:
            if prop in data:
                setattr(self, prop, data[prop])

    def get_data(self) -> List[Dict]:
        """
        Retrieve professional data as a list containing a dictionary.

        Extracts all properties except 'institutionfacility', which is
        converted to its ID if present, otherwise None.

        Returns
        -------
        List[Dict]
            A list containing a single dictionary with professional
            attributes and facility ID.

        Examples
        --------
        >>> hp = Professional(id=1, name="Dr. Smith",
        ...     type=5, institutionfacility=None)
        >>> data = hp.get_data()
        >>> data[0]['id']
        1
        >>> data[0]['name']
        'Dr. Smith'
        """
        info = {
            prop: getattr(self, prop)
            for prop in self.PROPERTIES
            if prop not in ["institutionfacility"]
        }
        info["institutionfacility"] = (
            self.institutionfacility.id if self.institutionfacility else None
        )
        return [info]
