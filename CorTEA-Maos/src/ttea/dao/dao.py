from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class DAO(ABC, Generic[T]):
    """Generic interface for CRUD operations on persistent entities.

    This abstract base class defines the standard data access object (DAO)
    pattern with type-safe operations for any entity type ``T``.

    Attributes
    ----------
    None
        This is an interface; concrete implementations may define attributes.

    Methods
    -------
    insert(obj)
        Inserts a new object and returns its generated identifier.
    update(obj)
        Updates an existing object in the persistent storage.
    delete(obj_id)
        Deletes the object identified by the given identifier.
    select(obj_id)
        Retrieves an object by its identifier.
    list()
        Retrieves all objects of type ``T``.
    """

    @abstractmethod
    def insert(self, obj: T) -> int:
        """Insere a new object and returns its generated ID.

        Parameters
        ----------
        obj : T
            The object instance to be persisted.

        Returns
        -------
        int
            The identifier (usually primary key) assigned to the new object.
        """

    @abstractmethod
    def update(self, obj: T) -> bool:
        """Updates an existing object in the persistent storage.

        Parameters
        ----------
        obj : T
            The object with updated values. Its identifier must correspond
            to an existing record.

        Returns
        -------
        bool
            True if the object was successfully updated, False otherwise
            (e.g., if the object does not exist).
        """

    @abstractmethod
    def delete(self, obj_id: int) -> bool:
        """Removes the object identified by the given ID.

        Parameters
        ----------
        obj_id : int
            Identifier of the object to be deleted.

        Returns
        -------
        bool
            True if the object was successfully deleted, False otherwise
            (e.g., if no object with the given ID exists).
        """
        pass

    @abstractmethod
    def select(self, obj_id: int) -> Optional[T]:
        """Retrieves an object by its identifier.

        Parameters
        ----------
        obj_id : int
            Identifier of the object to retrieve.

        Returns
        -------
        Optional[T]
            The object if found, or None if no object matches the ID.
        """

    @abstractmethod
    def list(self) -> List[T]:
        """Returns all persisted objects of type T.

        Returns
        -------
        List[T]
            A list containing all objects currently stored.
        """
