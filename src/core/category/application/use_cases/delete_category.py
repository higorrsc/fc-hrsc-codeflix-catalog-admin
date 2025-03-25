from src.core._shared.application.use_cases.delete import DeleteRequest, DeleteUseCase
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository


class DeleteCategory(DeleteUseCase):
    """
    Delete a category by its ID.
    """

    def __init__(self, repository: CategoryRepository):
        """
        Initialize the DeleteCategory use case.

        Args:
            repository (CategoryRepository): The category repository.
        """

        super().__init__(
            repository=repository,
            not_found_exception=CategoryNotFound,
            not_found_message="Category with ID {id} not found",
        )

    def execute(self, request: DeleteRequest) -> None:
        """
        Deletes a category by its ID.

        Args:
            request (DeleteRequest): The request with the ID of the category to be deleted.

        Raises:
            CategoryNotFound: If the category is not found.
        """

        super().execute(request)
