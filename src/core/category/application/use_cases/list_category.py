import uuid
from dataclasses import dataclass

from src.core._shared.application.use_cases.list import (
    ListRequest,
    ListResponse,
    ListUseCase,
)
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class CategoryOutput:
    """
    Represents the output of a category.
    """

    id: uuid.UUID
    name: str
    description: str
    is_active: bool


class ListCategory(ListUseCase):
    """
    List a category by its ID.
    """

    def __init__(self, repository: CategoryRepository):
        """
        Initialize the ListCategory use case.

        Args:
            repository (CategoryRepository): The category repository.
        """

        super().__init__(repository)

    def execute(self, request: ListRequest) -> ListResponse:
        """
        Executes the ListCategory use case to list categories based on request parameters.

        Args:
            request (ListRequest): The request object containing sorting and pagination details.

        Returns:
            ListResponse: A response containing the list of categories and pagination metadata.
        """

        return super().execute(request)
