from src.core._shared.application.use_cases.delete import DeleteRequest, DeleteUseCase
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository import GenreRepository


class DeleteGenre(DeleteUseCase):
    """
    Delete a genre by its ID.
    """

    def __init__(self, repository: GenreRepository):
        """
        Initialize the DeleteGenre use case.

        Args:
            repository (GenreRepository): The genre repository.
        """

        super().__init__(
            repository=repository,
            not_found_exception=GenreNotFound,
            not_found_message="Genre with ID {id} not found",
        )

    def execute(self, request: DeleteRequest) -> None:
        """
        Deletes a genre by its ID.

        Args:
            request (DeleteRequest): The request with the ID of the genre to be deleted.

        Raises:
            GenreNotFound: If the genre is not found.
        """

        super().execute(request)
