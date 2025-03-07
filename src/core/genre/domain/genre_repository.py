import uuid
from abc import ABC, abstractmethod
from typing import List

from src.core.genre.domain.genre import Genre


class GenreRepository(ABC):
    """
    Interface for a genre repository.
    """

    @abstractmethod
    def save(self, genre: Genre):
        """
        Save a genre to the repository.

        Args:
            genre (Genre): The genre to be saved.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, genre_id: uuid.UUID) -> Genre | None:
        """
        Retrieve a genre by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the genre to be retrieved.

        Returns:
            Genre: The genre with the given ID, or None if it doesn't exist.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, genre_id: uuid.UUID):
        """
        Delete a genre by its ID from the repository.

        Args:
            id (uuid.UUID): The ID of the genre to be deleted.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, genre: Genre):
        """
        Update a genre in the repository.

        Args:
            genre (Genre): The genre to be updated.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Genre]:
        """
        List all categories from the repository.

        Returns:
            list[Genre]: A list of all categories.
        """
        raise NotImplementedError
