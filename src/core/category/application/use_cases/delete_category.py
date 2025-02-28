import uuid
from dataclasses import dataclass

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class DeleteCategoryRequest:
    """
    Represents the request to delete a category by its ID.
    """

    id: uuid.UUID


class DeleteCategory:
    """
    Delete a category by its ID.
    """

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: DeleteCategoryRequest) -> None:
        """
        Deletes a category by its ID.

        Args:
            request (DeleteCategoryRequest): The request with the category ID.

        """
        category = self.repository.get_by_id(category_id=request.id)

        if category is None:
            raise CategoryNotFound(f"Category with ID {request.id} not found")

        self.repository.delete(category_id=request.id)
        return None
