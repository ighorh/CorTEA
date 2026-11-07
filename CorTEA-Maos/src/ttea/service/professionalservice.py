# /service/professionalservice.py
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QCoreApplication, QObject, Signal

# Local module import
from ttea.dao import ProfessionalCsvDAO
from ttea.model import InstitutionFacility, Professional


class ProfessionalService(QObject):
    """
    Service layer (MVCS) handling all business rules related to insti.

    Attributes
    ----------
    dao : InstitutionFacilityCsvDAO
        Data access object responsible for persistence operations.
        Defaults to a new ``InstitutionFacilityCsvDAO``
        instance if not provided.

    Methods
    -------
    __init__(dao=None)
        Initializes the service with a DAO instance.
    get_all_professionals()
        Returns all registered professionals.
    create_professional(data)
        Creates a new professional from the provided data dictionary.
    update_professional(professional_id, data)
        Updates an existing professional with the given data.
    delete_professional(professional_id)
        Deletes a professional by its ID.
    find_by_id(professional_id)
        Retrieves a professional by its ID.
    search_professionals(query="")
        Searches professionals by name or ID (case-insensitive).
    """

    _instance = None
    # Sinal que avisa: "Se os dados mudaram"
    professional_change = Signal(int)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dao: Optional[ProfessionalCsvDAO] = None):
        """
        Initialize the service with a data access object.

        Parameters
        ----------
        dao : InstitutionFacilityCsvDAO, optional
            Instance used for persistence. If ``None``, a default
            ``InstitutionFacilityCsvDAO`` is created.
        """
        from ttea.service import InstitutionFacilityService

        if not hasattr(self, "_initialized"):
            super().__init__()
            self.institution_service = InstitutionFacilityService()
            self.dao = dao or ProfessionalCsvDAO(
                self.institution_service.get_dao()
            )
            self._initialized = True

    def get_all_professionals(self) -> List[Professional]:
        """Return a list of all registered professionals.

        Returns
        -------
        List[InstitutionFacility]
            Complete list of ``InstitutionFacility`` instances stored
            in the DAO.
        """
        return self.dao.list()

    def validate_data(self, data: Dict[str, Any]) -> List[str]:
        """
        Valida as regras de negócio para os dados de uma instituição.
        Retorna uma lista de mensagens de erro (vazia se estiver tudo ok).
        """
        errors = []
        if data.get("id") is None:
            errors.append(self.tr("ID é obrigatório!\n"))
        elif not isinstance(data.get("id"), int):
            errors.append(self.tr("ID deve ser do tipo inteiro!\n"))

        if not data.get("name") or not data.get("name").strip():
            errors.append(self.tr("Nome é obrigatório!\n"))

        if data.get("type") == 0:
            errors.append(self.tr("Tipo é obrigatório!\n"))

        return errors

    def create_professional(
        self, data: Dict[str, Any]
    ) -> Optional[Professional]:
        """
        Create a new InstitutionFacility from a dictionary of attributes.

        Parameters
        ----------
        data : dict
            Must contain the keys the attributes.

        Returns
        -------
        InstitutionFacility or None
            The created ``InstitutionFacility`` instance if validation
            and insertion succeed; ``None`` otherwise.
        """
        professional = Professional(**data)

        if not professional.is_valid():
            return None

        new_id = self.dao.insert(professional)
        if new_id:
            self.professional_change.emit(new_id)
        return self.dao.select(new_id) if new_id > 0 else None

    def update_professional(
        self, professional_id: int, data: Dict[str, Any]
    ) -> bool:
        """
        Update an existing professional with new values.

        Parameters
        ----------
        professional_id : int
            Identifier of the professional to update.
        data : dict
            Dictionary containing updated fields. Missing keys keep the
            current value.

        Returns
        -------
        bool
            ``True`` if the professional was found, validated,
            and updated successfully; ``False`` otherwise.
        """
        professional = self.dao.select(professional_id)
        if not professional:
            return False

        professional.set_data(data)

        if not professional.is_valid():
            return False

        success = self.dao.update(professional)

        if success:
            self.professional_change.emit(professional_id)

        return success

    def delete_professional(self, professional_id: int) -> bool:
        """Delete a professional by its identifier.

        Parameters
        ----------
        professional_id : int
            Identifier of the professional to be removed.

        Returns
        -------
        bool
            ``True`` if the professional was successfully deleted,
            ``False`` otherwise (e.g., professional not found).
        """
        success = self.dao.delete(professional_id)

        if success:
            self.institutionfacility_change.emit(0)

        return success

    def find_by_id(
        self, professional_id: int
    ) -> Optional[Professional]:
        """Retrieve a professional by its unique identifier.

        Parameters
        ----------
        professional_id : int
            The professional's ID.

        Returns
        -------
        Professional or None
            The matching ``Professional`` instance
            or ``None`` if not found.
        """
        return self.dao.select(professional_id)

    def search_professionals(
        self, query: str = ""
    ) -> List[Professional]:
        """
        Search professionals by name or ID (case-insensitive).

        Parameters
        ----------
        query : str, optional
            Search term. If empty or whitespace-only, returns all
            professionals.

        Returns
        -------
        List[InstitutionFacility]
            List of professionals whose ID (as string)
            or name contain the query term.
        """
        all_professionals = self.get_all_professionals()
        if not query.strip():
            return all_professionals

        q = query.lower().strip()
        return [
            p
            for p in all_professionals
            if q in str(p.id) or q in p.name.lower()
        ]

    def get_professional_types(self) -> Dict[int, str]:
        return {
            key: QCoreApplication.translate("Professional", value)
            for key, value in Professional.TYPE_MAP.items()
        }

    def get_all_institutionfacilities(self) -> List[InstitutionFacility]:
        return sorted(
            self.institution_service.get_all_institutionfacilities(),
            key=lambda p: p.name,
        )

    def get_institutionfacility_by_id(
        self, institution_id: int
    ) -> Optional[InstitutionFacility]:
        return self.institution_service.find_by_id(institution_id)
