# /service/institutionfacilityservice.py
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QCoreApplication, QObject, Signal

# Local module import
from ttea.dao import InstitutionFacilityCsvDAO
from ttea.exception import BusinessRuleException
from ttea.model import InstitutionFacility


class InstitutionFacilityService(QObject):
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
    get_all_institutionfacilities()
        Returns all registered institutionfacilities.
    create_institutionfacility(data)
        Creates a new institutionfacility from the provided data dictionary.
    update_institutionfacility(institutionfacility_id, data)
        Updates an existing institutionfacility with the given data.
    delete_institutionfacility(institutionfacility_id)
        Deletes a institutionfacility by its ID.
    find_by_id(institutionfacility_id)
        Retrieves a institutionfacility by its ID.
    search_institutionfacilities(query="")
        Searches institutionfacilities by name or ID (case-insensitive).
    """

    _instance = None
    # Sinal que avisa: "Se os dados mudaram"
    institutionfacility_change = Signal(int)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dao: Optional[InstitutionFacilityCsvDAO] = None):
        """
        Initialize the service with a data access object.

        Parameters
        ----------
        dao : InstitutionFacilityCsvDAO, optional
            Instance used for persistence. If ``None``, a default
            ``InstitutionFacilityCsvDAO`` is created.
        """
        if not hasattr(self, "_initialized"):
            super().__init__()
            self.dao = dao or InstitutionFacilityCsvDAO()
            self._initialized = True

    def get_all_institutionfacilities(self) -> List[InstitutionFacility]:
        """Return a list of all registered institutionfacilities.

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

    def create_institutionfacility(
        self, data: Dict[str, Any]
    ) -> Optional[InstitutionFacility]:
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
        institutionfacility = InstitutionFacility(**data)

        if not institutionfacility.is_valid():
            return None

        new_id = self.dao.insert(institutionfacility)
        if new_id:
            self.institutionfacility_change.emit(new_id)
        return self.dao.select(new_id) if new_id > 0 else None

    def update_institutionfacility(
        self, institutionfacility_id: int, data: Dict[str, Any]
    ) -> bool:
        """
        Update an existing institutionfacility with new values.

        Parameters
        ----------
        institutionfacility_id : int
            Identifier of the institutionfacility to update.
        data : dict
            Dictionary containing updated fields. Missing keys keep the
            current value.

        Returns
        -------
        bool
            ``True`` if the institutionfacility was found, validated,
            and updated successfully; ``False`` otherwise.
        """
        institutionfacility = self.dao.select(institutionfacility_id)
        if not institutionfacility:
            return False

        institutionfacility.set_data(data)

        if not institutionfacility.is_valid():
            return False

        success = self.dao.update(institutionfacility)

        if success:
            self.institutionfacility_change.emit(institutionfacility_id)

        return success

    def delete_institutionfacility(self, institutionfacility_id: int) -> bool:
        """Delete a institutionfacility by its identifier.

        Parameters
        ----------
        institutionfacility_id : int
            Identifier of the institutionfacility to be removed.

        Returns
        -------
        bool
            ``True`` if the institutionfacility was successfully deleted,
            ``False`` otherwise (e.g., institutionfacility not found).
        """
        from ttea.service import ProfessionalService

        # Validação de integridade referencial (Negócio)
        professional_service = ProfessionalService()
        professionals = professional_service.get_all_professionals()
        if any(
            professional.institutionfacility.id == institutionfacility_id
            for professional in professionals
        ):
            raise BusinessRuleException(
                self.tr(
                    "Exclusão negada: A instituição possui profissional vinculado."
                )
            )

        success = self.dao.delete(institutionfacility_id)

        if success:
            self.institutionfacility_change.emit(0)

        return success

    def find_by_id(
        self, institutionfacility_id: int
    ) -> Optional[InstitutionFacility]:
        """Retrieve a institutionfacility by its unique identifier.

        Parameters
        ----------
        institutionfacility_id : int
            The institutionfacility's ID.

        Returns
        -------
        InstitutionFacility or None
            The matching ``InstitutionFacility`` instance
            or ``None`` if not found.
        """
        return self.dao.select(institutionfacility_id)

    def search_institutionfacilities(
        self, query: str = ""
    ) -> List[InstitutionFacility]:
        """
        Search institutionfacilities by name or ID (case-insensitive).

        Parameters
        ----------
        query : str, optional
            Search term. If empty or whitespace-only, returns all
            institutionfacilities.

        Returns
        -------
        List[InstitutionFacility]
            List of institutionfacilities whose ID (as string)
            or name contain the query term.
        """
        return self.dao.search_institutionfacilities(query)

    def get_institutionfacility_types(self) -> Dict[int, str]:
        # return InstitutionFacility.TYPE_MAP
        return {
            key: QCoreApplication.translate("InstitutionFacility", value)
            for key, value in InstitutionFacility.TYPE_MAP.items()
        }

    def get_dao(self) -> InstitutionFacilityCsvDAO:
        """Return the DAO instance used by this service.

        Returns
        -------
        InstitutionFacilityCsvDAO
            The data access object instance responsible for persistence.
        """
        return self.dao
