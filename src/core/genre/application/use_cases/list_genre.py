import uuid
from dataclasses import dataclass
from typing import List

from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    """
    Represents the output of a genre.
    """

    id: uuid.UUID
    name: str
    is_active: bool
    categories: set[uuid.UUID]


class ListGenre:
    """
    List a genre by its ID.
    """

    @dataclass
    class Input:
        """
        Represents the request to list a genre by its ID.
        """

    @dataclass
    class Output:
        """
        Represents the output of a genre.
        """

        data: List[GenreOutput]

    def __init__(self, repository: GenreRepository):
        """
        Initialize the ListGenre use case.

        Args:
            repository (GenreRepository): The genre repository.
        """
        self.repository = repository

    def execute(self, input: Input) -> Output:
        """
        List all genres.

        Returns:
            ListGenre.Output: A list of genres.
        """
        genres = self.repository.list()
        mapped_genres: List[GenreOutput] = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories,
            )
            for genre in genres
        ]

        return self.Output(data=mapped_genres)
