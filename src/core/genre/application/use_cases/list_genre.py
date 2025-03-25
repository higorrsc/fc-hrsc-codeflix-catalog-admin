import uuid
from dataclasses import dataclass

from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListUseCase,
)
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


class ListGenre(ListUseCase):
    """
    List a genre by its ID.
    """

    def __init__(self, repository: GenreRepository):
        """
        Initialize the ListGenre use case.

        Args:
            repository (GenreRepository): The genre repository.
        """

        super().__init__(repository)

    def execute(self, request: ListRequest) -> ListResponse:
        """
        Executes the ListGenre use case to list genres based on request parameters.

        Args:
            request (ListRequest): The request object containing sorting and pagination details.

        Returns:
            ListResponse: A response containing the list of genres and pagination metadata.
        """

        return super().execute(request)
