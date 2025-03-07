import uuid
from typing import List

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class InMemoryGenreRepository(GenreRepository):
    """
    In memory genre repository
    """

    def __init__(self, genres=None):
        """
        Initialize the in-memory genre repository.

        Args:
            genres (list, optional): A list of genres to initialize the repository with.
            Defaults to an empty list if not provided.
        """

        self.genres = genres or []

    def save(self, genre: Genre) -> None:
        """
        Save a genre to the in-memory repository.

        Args:
            genre (Genre): The genre to be saved.
        """

        self.genres.append(genre)

    def get_by_id(self, genre_id: uuid.UUID) -> Genre | None:
        """
        Retrieve a genre by its ID from the in-memory repository.

        Args:
            id (uuid.UUID): The ID of the genre to be retrieved.

        Returns:
            Genre | None: The genre with the given ID, or None if it doesn't exist.
        """

        for genre in self.genres:
            if genre.id == genre_id:
                return genre

        return None

    def delete(self, genre_id: uuid.UUID) -> None:
        """
        Delete a genre by its ID from the in-memory repository.

        Args:
            id (uuid.UUID): The ID of the genre to be deleted.
        """

        self.genres = [genre for genre in self.genres if genre.id != genre_id]

        return None

    def update(self, genre: Genre) -> None:
        """
        Update a genre in the in-memory repository.

        Args:
            genre (Genre): The genre to be updated.
        """

        for idx, gen in enumerate(self.genres):
            if gen.id == genre.id:
                self.genres[idx] = genre

        return None

    def list(self) -> List[Genre]:
        """
        List all genres in the in-memory repository.

        Returns:
            list[Genre]: A list of all genres in the repository.
        """

        return [genre for genre in self.genres]
