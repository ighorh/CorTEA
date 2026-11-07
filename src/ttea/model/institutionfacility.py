from dataclasses import dataclass, fields
from typing import ClassVar, Dict, List

from PySide6.QtCore import QT_TRANSLATE_NOOP


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
class InstitutionFacility:
    """Health institution / facility entity.

    Represents a service location with contact information.

    Attributes
    ----------
    id : int
        Unique identifier for the facility.
    name : str
        Facility name.
    address : str
        Physical address.
    phone : str
        Contact phone number.
    email : str
        Contact email address.
    website : str
        Website URL.
    social_network : str
        Social network or messaging endpoint.
    type : int
        Integer key into TYPE_MAP describing facility type.

    CLASS VARIABLES
    ---------------
    TYPE_MAP : ClassVar[dict[int, str]]
        Mapping of facility type codes to translated names.
        Used for internationalization via QCoreApplication.
    PROPERTIES : ClassVar[list[str]]
        List of property names for serialization.
    DATA_PROPERTIES : ClassVar[list]
        List of data property defaults for serialization.

    Methods
    -------
    is_valid() -> bool
        Validate required fields.
    set_data(data: Dict) -> None
        Populate properties from a dict.
    get_data() -> List[Dict]
        Export properties as a list containing one dict.

    Notes
    -----
    TYPE_MAP is used for localization via QCoreApplication.translate.
    """

    id: int
    name: str
    address: str
    phone: str
    email: str
    website: str
    social_network: str
    type: int

    # Mapping type with translation support using QT_TRANSLATE_NOOP
    # for deferred translation. The translation will be applied when
    # the type is accessed in the UI, allowing for dynamic language changes.
    TYPE_MAP: ClassVar[dict[int, str]] = {
        0: "",
        1: QT_TRANSLATE_NOOP("InstitutionFacility", "Clínica"),
        2: QT_TRANSLATE_NOOP("InstitutionFacility", "Consultório"),
        3: QT_TRANSLATE_NOOP("InstitutionFacility", "Hospital"),
        4: QT_TRANSLATE_NOOP("InstitutionFacility", "Instituição Comunitária"),
        5: QT_TRANSLATE_NOOP("InstitutionFacility", "Instituição de Ensino"),
        6: QT_TRANSLATE_NOOP("InstitutionFacility", "Outro"),
        7: QT_TRANSLATE_NOOP("InstitutionFacility", "Posto de Saúde"),
    }

    PROPERTIES: ClassVar[list[str]] = []
    DATA_PROPERTIES: ClassVar[list] = []

    def is_valid(self) -> bool:
        """Validate the facility object.

        Ensures required fields are present and non-empty, and all other
        fields are not None.

        Returns
        -------
        bool
            True if the object is valid, False otherwise.

        Examples
        --------
        >>> inst = InstitutionFacility(1, 'A', '', '', '', '', '', 0)
        >>> inst.is_valid()
        True
        >>> inst = InstitutionFacility(None, '', '', '', '', '', '', 0)
        >>> inst.is_valid()
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
        """Set object attributes from a dictionary.

        Parameters
        ----------
        data : Dict
            Dictionary mapping property names to their values.

        Examples
        --------
        >>> inst = InstitutionFacility(1, 'A', '', '', '', '', '', 0)
        >>> inst.set_data({'name': 'B', 'type': 1})
        """

        for prop in self.PROPERTIES:
            if prop in data:
                setattr(self, prop, data[prop])

    def get_data(self) -> List[Dict]:
        """Retrieve facility data as a list containing a dict.

        Returns
        -------
        List[Dict]
            List with a single dict containing all property values.

        Examples
        --------
        >>> inst = InstitutionFacility(1, 'A', '', '', '', '', '', 0)
        >>> inst.get_data()[0]['name']
        'A'
        """

        info = {prop: getattr(self, prop) for prop in self.PROPERTIES}
        return [info]
