import uuid
from dataclasses import dataclass

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class GetCategoryRequest:
    """
    Represents the request to get a category by its ID.
    """

    id: uuid.UUID


@dataclass
class GetCategoryResponse:
    """
    Represents the response of getting a category by its ID.
    """

    id: uuid.UUID
    name: str
    description: str
    is_active: bool


class GetCategory:
    """
    Get a category by its ID.
    """

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        """
        Gets a category by its ID.

        Args:
            request (GetCategoryRequest): The request with the category ID.

        Returns:
            GetCategoryResponse: The response with the category data.
        """
        category = self.repository.get_by_id(category_id=request.id)

        if category is None:
            raise CategoryNotFound(f"Category with ID {request.id} not found")

        return GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
