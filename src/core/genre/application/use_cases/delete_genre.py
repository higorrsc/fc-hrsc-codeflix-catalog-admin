import uuid
from dataclasses import dataclass

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository import GenreRepository


class DeleteGenre:
    """
    Delete a genre by its ID.
    """

    @dataclass
    class Input:
        """
        Input for the DeleteGenre use case.
        """

        id: uuid.UUID

    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> None:
        """
        Deletes a genre by its ID.

        Args:
            input (Input): The input with the genre ID.

        """

        genre = self.repository.get_by_id(genre_id=input.id)

        if genre is None:
            raise GenreNotFound(f"Genre with ID {input.id} not found")

        self.repository.delete(genre_id=input.id)
