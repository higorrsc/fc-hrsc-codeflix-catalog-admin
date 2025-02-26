import uuid
from dataclasses import dataclass

from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.application.use_cases.category_repository import (
    CategoryRepository,
)
from src.core.category.domain.category import Category


@dataclass
class CreateCategoryRequest:
    """
    Represents the request to create a new category.
    """

    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateCategoryResponse:
    """
    Represents the response of creating a new category.
    """

    id: uuid.UUID


class CreateCategory:
    """
    Create a new category.
    """

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        """
        Create a new category.

        Args:
            name (str): The name of the category.
            description (str): The description of the category.
            is_active (bool): Whether the category is active or not. Defaults to True.

        Returns:
            uuid.UUID: The identifier of the created category.
        """
        try:
            category = Category(
                name=request.name,
                description=request.description,
                is_active=request.is_active,
            )
        except ValueError as err:
            raise InvalidCategoryData(err) from err

        self.repository.save(category)

        return CreateCategoryResponse(id=category.id)
